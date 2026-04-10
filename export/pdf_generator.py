from typing import List
from search.base import SearchResult
from export.citations import CitationFormatter
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from io import BytesIO
import streamlit as st


class PDFReportGenerator:
    """Generate academic PDF reports with proper citations"""

    def __init__(self, title: str, query: str):
        self.title = title
        self.query = query
        self.buffer = BytesIO()

    def generate(self, results: List[SearchResult], style: str = "APA") -> BytesIO:
        """Generate PDF report"""
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1f1f1f"),
            spaceAfter=30,
            alignment=1,
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#333333"),
            spaceAfter=12,
            spaceBefore=12,
        )

        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["BodyText"],
            fontSize=11,
            alignment=4,
        )

        elements.append(Paragraph(self.title, title_style))
        elements.append(Spacer(1, 0.3 * inch))

        meta_text = f"""
        <b>Research Query:</b> {self.query}<br/>
        <b>Generated:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
        <b>Total Results:</b> {len(results)}<br/>
        <b>Citation Format:</b> {style}
        """
        elements.append(Paragraph(meta_text, body_style))
        elements.append(Spacer(1, 0.3 * inch))

        elements.append(Paragraph("Search Results", heading_style))

        for i, result in enumerate(results, 1):
            result_text = f"""
            <b>{i}. {result.title}</b><br/>
            <i>Source: {result.source}</i><br/>
            {result.snippet}
            """
            elements.append(Paragraph(result_text, body_style))
            elements.append(Spacer(1, 0.15 * inch))

        elements.append(PageBreak())
        elements.append(Paragraph("Bibliography", heading_style))

        bibliography = CitationFormatter.format_bibliography(results, style)
        for line in bibliography.split("\n\n"):
            elements.append(Paragraph(line, body_style))
            elements.append(Spacer(1, 0.1 * inch))

        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer

    def get_bytes(self) -> bytes:
        """Get PDF as bytes"""
        return self.buffer.getvalue()
