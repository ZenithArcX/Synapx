"""
Package initialization for insurance claims agent
"""

__version__ = "1.0.0"
__author__ = "Synapx Assessment"

from src.pdf_parser import DocumentParser
from src.field_extractor import FieldExtractor
from src.routing_engine import RoutingEngine

__all__ = [
    "DocumentParser",
    "FieldExtractor",
    "RoutingEngine"
]
