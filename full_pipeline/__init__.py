"""Pipeline library for PII extraction and analysis."""

from .pii_pipeline import (
    DeclarationPipeline,
    GenderAnalyzer,
    SpouseOccupationAnalyzer,
    GenderDiscriminationAnalyzer,
    AgePyramidBuilder,
    ReportFigureGenerator,
)

__all__ = [
    "DeclarationPipeline",
    "GenderAnalyzer",
    "SpouseOccupationAnalyzer",
    "GenderDiscriminationAnalyzer",
    "AgePyramidBuilder",
    "ReportFigureGenerator",
]
