import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

LOG_PATTERN = re.compile(
