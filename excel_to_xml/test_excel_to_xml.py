import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import date

from openpyxl import Workbook

from excel_to_xml import convert, to_tag, unique_tags


class ConvertTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def make_xlsx(self, sheets):
        """sheets: dict of sheet name -> list of rows. First sheet is active."""
        wb = Workbook()
        wb.remove(wb.active)
        for name, rows in sheets.items():
            ws = wb.create_sheet(name)
            for row in rows:
                ws.append(row)
        path = os.path.join(self.tmp.name, "data.xlsx")
        wb.save(path)
        return path

    def test_rows_become_elements(self):
        path = self.make_xlsx({"People": [["name", "age"], ["Ada", 36], ["Alan", 41]]})
        root = convert(path)
        rows = root.findall("row")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].findtext("name"), "Ada")
        self.assertEqual(rows[0].findtext("age"), "36")
        self.assertEqual(rows[1].findtext("name"), "Alan")

    def test_headers_are_sanitized_into_valid_tags(self):
        path = self.make_xlsx({"S": [["First Name", "1st", "xml data", "a/b", "Total (USD)"], ["x", "y", "z", "w", "v"]]})
        row = convert(path).find("row")
        self.assertEqual([child.tag for child in row], ["First_Name", "_1st", "_xml_data", "a_b", "Total_USD"])

    def test_special_characters_are_escaped(self):
        path = self.make_xlsx({"S": [["note"], ["Tom & Jerry <3"]]})
        xml_bytes = ET.tostring(convert(path))
        self.assertIn(b"Tom &amp; Jerry &lt;3", xml_bytes)
        self.assertEqual(ET.fromstring(xml_bytes).find("row/note").text, "Tom & Jerry <3")

    def test_empty_cells_and_blank_rows(self):
        path = self.make_xlsx({"S": [["a", "b"], ["1", None], [None, None], ["", "  "], ["2", "3"]]})
        rows = convert(path).findall("row")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].findtext("b"), "")
        self.assertEqual(rows[1].findtext("a"), "2")

    def test_dates_and_booleans(self):
        path = self.make_xlsx({"S": [["when", "ok"], [date(2024, 5, 1), True]]})
        row = convert(path).find("row")
        self.assertEqual(row.findtext("when"), "2024-05-01T00:00:00")
        self.assertEqual(row.findtext("ok"), "true")

    def test_duplicate_headers_are_renamed(self):
        path = self.make_xlsx({"S": [["x", "x", "x"], [1, 2, 3]]})
        row = convert(path).find("row")
        self.assertEqual([child.tag for child in row], ["x", "x_2", "x_3"])

    def test_sheet_selection_and_custom_tags(self):
        path = self.make_xlsx({"One": [["a"], ["1"]], "Two": [["b"], ["2"]]})
        root = convert(path, sheet="Two", root_tag="data", row_tag="record")
        self.assertEqual(root.tag, "data")
        self.assertEqual(root.find("record/b").text, "2")

    def test_unknown_sheet_raises(self):
        path = self.make_xlsx({"One": [["a"], ["1"]]})
        with self.assertRaisesRegex(ValueError, "not found"):
            convert(path, sheet="Missing")

    def test_empty_sheet_gives_empty_root(self):
        path = self.make_xlsx({"S": []})
        root = convert(path)
        self.assertEqual(root.tag, "rows")
        self.assertEqual(len(root), 0)

    def test_header_less_columns_are_skipped(self):
        self.assertEqual(unique_tags(["a", None, "", "b"]), [(0, "a"), (3, "b")])
        self.assertIsNone(to_tag("   "))


if __name__ == "__main__":
    unittest.main()
