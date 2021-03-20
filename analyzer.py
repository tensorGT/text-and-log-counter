import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

LOG_PATTERN = re.compile(
    r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+.*?"[A-Z]+\s+(?P<path>\S+)[^"]*"\s+(?P<status>\d{3})'
)
WORD_PATTERN = re.compile(r"[a-z0-9']+")


def read_lines_safe(file_path: Path) -> List[str]:
    if not file_path.exists():
        raise FileNotFoundError("cant find file: %s" % file_path)
    try:
