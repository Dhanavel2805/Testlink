import pandas as pd
from lxml import etree as ET
from datetime import datetime

# Load Excel file
df = pd.read_excel("DR-2995_Testcases.xlsx", sheet_name="Sheet1")

# Drop unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Create root element
root = ET.Element("testcases")

for index, row in df.iterrows():
    testcase = ET.SubElement(root, "testcase", {
        "name": str(row.get("Testcase ID", index + 1))
    })

    # Add custom fields
    custom_fields = ET.SubElement(testcase, "custom_fields")
    for col in df.columns:
        name = str(col)
        value = str(row[col]) if pd.notna(row[col]) else ""

        cf = ET.SubElement(custom_fields, "custom_field")
        name_elem = ET.SubElement(cf, "name")
        name_elem.text = ET.CDATA(name)

        value_elem = ET.SubElement(cf, "value")
        value_elem.text = ET.CDATA(value)

# Save to XML file
tree = ET.ElementTree(root)
# Get today's date (YYYY-MM-DD)
today_date = datetime.now().strftime("%Y-%m-%d")

tree.write(
    f"OrderSummary_ItemDetails_Page_{today_date}.xml",
    encoding="utf-8",
    xml_declaration=True,
    pretty_print=True
)

print("Success!")


