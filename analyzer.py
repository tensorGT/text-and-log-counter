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
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        # fallback if file has weird latin1 chars
        with open(file_path, "r", encoding="latin-1", errors="replace") as f:
            return f.readlines()


def analyze_text(lines: List[str], top_n: int) -> Dict:
    words: Counter = Counter()
    for line in lines:
        tokens = WORD_PATTERN.findall(line.lower())
        words.update(tokens)

    return {
        "mode": "text",
        "total_lines": len(lines),
        "total_words": sum(words.values()),
        "unique_words": len(words),
        "top_words": words.most_common(top_n),
    }


def analyze_logs(lines: List[str], top_n: int) -> Dict:
    ips: Counter = Counter()
    statuses: Counter = Counter()
    paths: Counter = Counter()
    matched = 0

    for line in lines:
        m = LOG_PATTERN.search(line)
        if m:
            matched += 1
            ips[m.group("ip")] += 1
            statuses[m.group("status")] += 1
            paths[m.group("path")] += 1

    return {
        "mode": "log",
        "total_lines": len(lines),
        "matched_log_lines": matched,
        "top_ips": ips.most_common(top_n),
        "status_codes": statuses.most_common(top_n),
        "top_paths": paths.most_common(top_n),
    }


def print_report(result: Dict) -> None:
    print("=== Report (%s) ===" % result["mode"])
    if result["mode"] == "text":
        print("Lines:", result["total_lines"], "| Words:", result["total_words"], "| Unique:", result["unique_words"])
        print("\nTop words:")
        for word, cnt in result["top_words"]:
            print("  %-15s %d" % (word, cnt))
    else:
        print("Lines:", result["total_lines"], "| Matched:", result["matched_log_lines"])
        print("\nTop IPs:")
        for ip, cnt in result["top_ips"]:
            print("  %-18s %d" % (ip, cnt))
        print("\nStatus codes:")
        for code, cnt in result["status_codes"]:
