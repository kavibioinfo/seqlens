"""
Pathogenicity prediction using ensemble machine learning.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from ..models.schemas import Variant, ACMGClassification
from ..config import MODEL_PATH, ACMG_THRESHOLDS


class PathogenicityPredictor:
    """Ensemble ML model for predicting variant pathogenicity."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model if exists."""
        if MODEL_PATH.exists():
            try:
                model_data = joblib.load(MODEL_PATH)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.is_trained = True
                print(f"Loaded model from {MODEL_PATH}")
            except Exception as e:
                print(f"Could not load model: {e}")
                self._initialize_model()
        else:
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize a new model."""
        self.model = {
            'rf': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'gb': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        }
        self.is_trained = False
    
    def _extract_features(self, variant: Variant) -> np.ndarray:
        """Convert variant to feature vector."""
        features = []
        
        cadd = variant.cadd_score if variant.cadd_score is not None else 15.0
        features.append(cadd)
        
        sift = variant.sift_score if variant.sift_score is not None else 0.5
        features.append(1 - sift)
        
        polyphen = variant.polyphen_score if variant.polyphen_score is not None else 0.5
        features.append(polyphen)
        
        conservation = variant.conservation_score if variant.conservation_score is not None else 0.5
        features.append(conservation)
        
        af = variant.allele_frequency if variant.allele_frequency is not None else 0.01
        features.append(1 - min(af * 100, 1))
        
        type_scores = {
            'SNV': 0.3,
            'Insertion': 0.5,
            'Deletion': 0.6,
            'Indel': 0.5,
            'CNV': 0.7
        }
        features.append(type_scores.get(variant.variant_type.value, 0.3))
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, variant: Variant) -> Dict:
        """Predict pathogenicity for a single variant."""
        if not self.is_trained:
            return self._rule_based_prediction(variant)
        
        features = self._extract_features(variant)
        features_scaled = self.scaler.transform(features)
        
        rf_prob = self.model['rf'].predict_proba(features_scaled)[0][1]
        gb_prob = self.model['gb'].predict_proba(features_scaled)[0][1]
        
        ensemble_prob = 0.4 * rf_prob + 0.6 * gb_prob
        
        acmg = self._score_to_acmg(ensemble_prob)
        
        return {
            'pathogenicity_score': float(ensemble_prob),
            'acmg_classification': acmg,
            'confidence': abs(ensemble_prob - 0.5) * 2
        }
    
    def _rule_based_prediction(self, variant: Variant) -> Dict:
        """Fallback rule-based prediction when ML model is not trained."""
        score = 0.5
        
        if variant.cadd_score:
            if variant.cadd_score > 25:
                score += 0.2
            elif variant.cadd_score > 20:
                score += 0.1
            elif variant.cadd_score < 10:
                score -= 0.1
        
        if variant.sift_score is not None:
            if variant.sift_score < 0.05:
                score += 0.15
            elif variant.sift_score < 0.1:
                score += 0.05
        
        if variant.polyphen_score is not None:
            if variant.polyphen_score > 0.85:
                score += 0.15
            elif variant.polyphen_score > 0.5:
                score += 0.05
        
        if variant.allele_frequency is not None:
            if variant.allele_frequency < 0.001:
                score += 0.1
            elif variant.allele_frequency > 0.05:
                score -= 0.1
        
        if variant.conservation_score is not None:
            if variant.conservation_score > 0.8:
                score += 0.1
        
        score = max(0, min(1, score))
        
        acmg = self._score_to_acmg(score)
        
        return {
            'pathogenicity_score': float(score),
            'acmg_classification': acmg,
            'confidence': abs(score - 0.5) * 2,
            'method': 'rule-based'
        }
    
    def _score_to_acmg(self, score: float) -> ACMGClassification:
        """Convert pathogenicity score to ACMG classification."""
        if score >= ACMG_THRESHOLDS['pathogenic']:
            return ACMGClassification.PATHOGENIC
        elif score >= ACMG_THRESHOLDS['likely_pathogenic']:
            return ACMGClassification.LIKELY_PATHOGENIC
        elif score >= ACMG_THRESHOLDS['uncertain']:
            return ACMGClassification.UNCERTAIN
        elif score >= ACMG_THRESHOLDS['likely_benign']:
            return ACMGClassification.LIKELY_BENIGN
        return ACMGClassification.BENIGN
    
    def train(self, X: np.ndarray, y: np.ndarray, save: bool = True) -> Dict:
        """Train the ensemble model."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Training Random Forest...")
        self.model['rf'].fit(X_train_scaled, y_train)
        
        print("Training Gradient Boosting...")
        self.model['gb'].fit(X_train_scaled, y_train)
        
        rf_pred = self.model['rf'].predict_proba(X_test_scaled)[:, 1]
        gb_pred = self.model['gb'].predict_proba(X_test_scaled)[:, 1]
        ensemble_pred = 0.4 * rf_pred + 0.6 * gb_pred
        
        metrics = {
            'rf_auc': roc_auc_score(y_test, rf_pred),
            'gb_auc': roc_auc_score(y_test, gb_pred),
            'ensemble_auc': roc_auc_score(y_test, ensemble_pred),
            'test_size': len(y_test)
        }
        
        self.is_trained = True
        
        if save:
            self._save_model()
        
        return metrics
    
    def _save_model(self):
        """Save trained model to disk."""
        model_data = {
            'model': self.model,
            'scaler': self.scaler
        }
        joblib.dump(model_data, MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
    
    def batch_predict(self, variants: List[Variant]) -> List[Dict]:
        """Predict pathogenicity for multiple variants."""
        return [self.predict(v) for v in variants]