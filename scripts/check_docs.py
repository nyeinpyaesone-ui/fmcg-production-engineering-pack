import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

csv_path = ROOT / "plans" / "WORK_ITEMS.csv"
with csv_path.open(newline="") as f:
    rows = list(csv.DictReader(f))

ids = [r["id"] for r in rows]
if len(ids) != len(set(ids)):
    errors.append("duplicate task ids in WORK_ITEMS.csv")
known = set(ids)
for r in rows:
    for dep in r["depends_on"].split(";"):
        dep = dep.strip()
        if dep and dep not in known:
            errors.append(f"{r['id']}: unknown dependency '{dep}'")

readme = (ROOT / "README.md").read_text()
for m in re.findall(r"`((?:docs|plans|config|\.agents|\.github)/[^`]+)`", readme):
    if not (ROOT / m).exists():
        errors.append(f"README references missing path: {m}")

if errors:
    sys.exit("\n".join(errors))
print("docs checks passed")
