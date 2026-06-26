"""
PDF Report Generator for SeqLens analysis results.
"""

from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from ..models.schemas import AnalysisResult


class ReportGenerator:
    """Generate professional PDF reports from analysis results."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5276'),
            spaceAfter=30
        )
    
    def generate(self, result: AnalysisResult) -> Path:
        """Generate PDF report and return file path."""
        
        report_id = f"seqlens_report_{result.job_id}"
        import tempfile
        output_path = Path(tempfile.gettempdir()) / f"{report_id}.pdf"
        
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Title
        story.append(Paragraph("SeqLens Genomic Analysis Report", self.title_style))
        story.append(Spacer(1, 20))
        
        # Metadata
        meta_data = [
            ['Report ID:', result.job_id],
            ['File Analyzed:', result.filename],
            ['Generated:', result.generated_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Processing Time:', f"{result.processing_time_seconds}s"],
            ['Total Variants:', str(result.total_variants)]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#eaf2f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 30))
        
        # Classification Summary
        story.append(Paragraph("Classification Summary", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        summary_data = [
            ['Classification', 'Count', 'Percentage'],
            ['Pathogenic', str(result.pathogenic_count), 
             f"{result.pathogenic_count/result.total_variants*100:.1f}%" if result.total_variants > 0 else "0%"],
            ['Likely Pathogenic', str(result.likely_pathogenic_count),
             f"{result.likely_pathogenic_count/result.total_variants*100:.1f}%" if result.total_variants > 0 else "0%"],
            ['Uncertain Significance', str(result.uncertain_count),
             f"{result.uncertain_count/result.total_variants*100:.1f}%" if result.total_variants > 0 else "0%"],
            ['Likely Benign', str(result.likely_benign_count),
             f"{result.likely_benign_count/result.total_variants*100:.1f}%" if result.total_variants > 0 else "0%"],
            ['Benign', str(result.benign_count),
             f"{result.benign_count/result.total_variants*100:.1f}%" if result.total_variants > 0 else "0%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Variant Details
        story.append(Paragraph("Variant Details", self.styles['Heading2']))
        story.append(Spacer(1, 10))
        
        variant_data = [['Chr', 'Position', 'Ref', 'Alt', 'Gene', 'Type', 'Score', 'ACMG']]
        
        for v in result.variants[:100]:
            variant_data.append([
                v.chrom,
                str(v.pos),
                v.ref,
                v.alt,
                v.gene or '-',
                v.variant_type.value,
                f"{v.pathogenicity_score:.3f}" if v.pathogenicity_score else '-',
                v.acmg_classification.value if v.acmg_classification else '-'
            ])
        
        variant_table = Table(variant_data, colWidths=[0.6*inch, 0.9*inch, 0.5*inch, 0.5*inch, 
                                                      0.9*inch, 0.7*inch, 0.8*inch, 1.1*inch])
        variant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        story.append(variant_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<i>Note: This report is generated for research purposes only. "
            "Clinical decisions should not be based solely on these predictions.</i>",
            self.styles['Italic']
        ))
        
        doc.build(story)
        return output_path