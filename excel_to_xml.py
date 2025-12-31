import sys
import os
import pandas as pd
from lxml import etree as ET
from datetime import datetime

# -------------------------
# Validate input arguments
# -------------------------
if len(sys.argv) < 2:
    print("ERROR: Excel file path not provided")
    sys.exit(1)

excel_file = sys.argv[1]

if not os.path.isfile(excel_file):
    print(f"ERROR: Excel file not found -> {excel_file}")
    sys.exit(1)

print(f"Using Excel file: {excel_file}")

# -------------------------
# Read Excel (FIRST sheet)
# -------------------------
try:
    df = pd.read_excel(excel_file)  # first sheet automatically
except Exception as e:
    print(f"ERROR reading Excel file: {e}")
    sys.exit(1)

# -------------------------
# Clean dataframe
# -------------------------
df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]

print(f"Columns detected: {list(df.columns)}")
print(f"Total rows: {len(df)}")

# -------------------------
# Create XML structure
# -------------------------
root = ET.Element("testcases")

for _, row in df.iterrows():
    testcase = ET.SubElement(root, "testcase")

    for col in df.columns:
        child = ET.SubElement(testcase, col.replace(" ", "_"))
        value = row[col]
        child.text = "" if pd.isna(value) else str(value)

# -------------------------
# Write XML output
# -------------------------
today = datetime.now().strftime("%Y-%m-%d")
base_name = os.path.splitext(os.path.basename(excel_file))[0]
output_file = f"{base_name}_{today}.xml"

tree = ET.ElementTree(root)
tree.write(
    output_file,
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)

print(f"XML successfully created: {output_file}")
