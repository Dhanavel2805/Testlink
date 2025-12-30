import os
import sys
import pandas as pd
from lxml import etree as ET
from datetime import datetime


def main():
    # Read Jenkins environment variables
    workspace = os.environ.get("WORKSPACE")
    upload_file = os.environ.get("UPLOAD_FILE")

    if not workspace or not upload_file:
        print("ERROR: WORKSPACE or UPLOAD_FILE environment variable not found")
        sys.exit(1)

    excel_path = os.path.join(workspace, upload_file)

    if not os.path.exists(excel_path):
        print(f"ERROR: Uploaded Excel file not found: {excel_path}")
        sys.exit(1)

    print(f"Workspace: {workspace}")
    print(f"Processing Excel file: {excel_path}")

    # -----------------------------
    # Load Excel file
    # -----------------------------
    df = pd.read_excel(excel_path, sheet_name="Sheet1")

    # Drop unnamed columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # -----------------------------
    # Create XML structure
    # -----------------------------
    root = ET.Element("testcases")

    for index, row in df.iterrows():
        testcase = ET.SubElement(
            root,
            "testcase",
            {
                "name": str(row.get("Testcase ID", index + 1))
            }
        )

        custom_fields = ET.SubElement(testcase, "custom_fields")

        for col in df.columns:
            name = str(col)
            value = str(row[col]) if pd.notna(row[col]) else ""

            cf = ET.SubElement(custom_fields, "custom_field")

            name_elem = ET.SubElement(cf, "name")
            name_elem.text = ET.CDATA(name)

            value_elem = ET.SubElement(cf, "value")
            value_elem.text = ET.CDATA(value)

    # -----------------------------
    # Write XML file with date
    # -----------------------------
    today_date = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(
        workspace,
        f"OrderSummary_ItemDetails_Page_{today_date}.xml"
    )

    tree = ET.ElementTree(root)
    tree.write(
        output_file,
        encoding="utf-8",
        xml_declaration=True,
        pretty_print=True
    )

    print(f"SUCCESS: XML file created -> {output_file}")


if __name__ == "__main__":
    main()
