"""
VCF (Variant Call Format) file parser.
"""

import gzip
from pathlib import Path
from typing import List, Dict, Optional, Iterator
from ..models.schemas import Variant, VariantType


class VCFParser:
    """Parser for VCF files (.vcf and .vcf.gz)."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.header_lines = []
        self.sample_names = []
        
    def _open_file(self):
        """Open VCF file (handles both .vcf and .vcf.gz)."""
        if str(self.file_path).endswith('.gz'):
            return gzip.open(self.file_path, 'rt')
        return open(self.file_path, 'r')
    
    def _detect_variant_type(self, ref: str, alt: str) -> VariantType:
        """Determine variant type from REF and ALT alleles."""
        if len(ref) == 1 and len(alt) == 1:
            return VariantType.SNV
        elif len(ref) > len(alt):
            return VariantType.DELETION
        elif len(ref) < len(alt):
            return VariantType.INSERTION
        elif len(ref) > 1 and len(alt) > 1:
            return VariantType.INDEL
        return VariantType.SNV
    
    def _parse_info_field(self, info_str: str) -> Dict[str, str]:
        """Parse the INFO column of VCF."""
        info = {}
        if info_str == '.' or not info_str:
            return info
        
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info[key] = value
            else:
                info[item] = True
        return info
    
    def _extract_gene(self, info: Dict[str, str]) -> Optional[str]:
        """Extract gene symbol from INFO field."""
        gene_keys = ['GENE', 'GENE_NAME', 'SYMBOL', 'ANN', 'CSQ']
        
        for key in gene_keys:
            if key in info:
                if key == 'ANN':
                    parts = info[key].split('|')
                    if len(parts) > 3:
                        return parts[3]
                elif key == 'CSQ':
                    parts = info[key].split('|')
                    if len(parts) > 3:
                        return parts[3]
                else:
                    return info[key]
        return None
    
    def _extract_scores(self, info: Dict[str, str]) -> Dict[str, Optional[float]]:
        """Extract prediction scores from INFO field."""
        scores = {
            'cadd_score': None,
            'sift_score': None,
            'polyphen_score': None,
            'conservation_score': None,
            'allele_frequency': None
        }
        
        if 'CADD' in info:
            try:
                scores['cadd_score'] = float(info['CADD'])
            except ValueError:
                pass
        
        if 'SIFT' in info:
            try:
                scores['sift_score'] = float(info['SIFT'])
            except ValueError:
                pass
        
        if 'PolyPhen' in info:
            try:
                scores['polyphen_score'] = float(info['PolyPhen'])
            except ValueError:
                pass
        
        if 'AF' in info:
            try:
                scores['allele_frequency'] = float(info['AF'])
            except ValueError:
                pass
        
        return scores
    
    def parse_header(self) -> List[str]:
        """Parse and store VCF header lines."""
        with self._open_file() as f:
            for line in f:
                if line.startswith('#'):
                    self.header_lines.append(line.strip())
                    if line.startswith('#CHROM'):
                        parts = line.strip().split('\t')
                        if len(parts) > 9:
                            self.sample_names = parts[9:]
                else:
                    break
        return self.header_lines
    
    def parse_variants(self) -> Iterator[Variant]:
        """Parse variants from VCF file."""
        with self._open_file() as f:
            for line in f:
                if line.startswith('#'):
                    continue
                
                parts = line.strip().split('\t')
                if len(parts) < 8:
                    continue
                
                chrom = parts[0].replace('chr', '')
                pos = int(parts[1])
                ref = parts[3]
                alt = parts[4]
                
                info = self._parse_info_field(parts[7])
                gene = self._extract_gene(info)
                scores = self._extract_scores(info)
                variant_type = self._detect_variant_type(ref, alt)
                
                yield Variant(
                    chrom=chrom,
                    pos=pos,
                    ref=ref,
                    alt=alt,
                    gene=gene,
                    variant_type=variant_type,
                    **scores
                )
    
    def count_variants(self) -> int:
        """Count total variants in file."""
        count = 0
        with self._open_file() as f:
            for line in f:
                if not line.startswith('#'):
                    count += 1
        return count
    
    def get_summary(self) -> Dict:
        """Get summary statistics of the VCF file."""
        self.parse_header()
        
        variant_types = {}
        chromosomes = set()
        total = 0
        
        for variant in self.parse_variants():
            total += 1
            chromosomes.add(variant.chrom)
            vt = variant.variant_type.value
            variant_types[vt] = variant_types.get(vt, 0) + 1
        
        return {
            'total_variants': total,
            'chromosomes': sorted(list(chromosomes)),
            'variant_types': variant_types,
            'sample_names': self.sample_names,
            'has_genotype_data': len(self.sample_names) > 0
        }