"""itemcheck: heuristic detection of common multiple-choice item-writing flaws."""
from .parser import Item, parse_file, parse_item  # noqa: F401
from .rules import Finding, check  # noqa: F401

__version__ = "0.1.0"
