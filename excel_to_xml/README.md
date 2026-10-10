# Excel to XML converter

Converts one worksheet of an `.xlsx` file into XML. The header row sets the
element names, and each following row becomes one `<row>` element.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Print XML to stdout (active sheet)
python excel_to_xml.py data.xlsx

# Write to a file, choosing a sheet and custom element names
python excel_to_xml.py data.xlsx -o out.xml -s Orders --root orders --row order
```

| Option | Meaning |
| --- | --- |
| `-o, --output` | Output file (default: stdout) |
| `-s, --sheet` | Sheet name (default: active sheet) |
| `--root` | Root element name (default: `rows`) |
| `--row` | Element name for each row (default: `row`) |

## Example

| Order ID | Customer    | Total (USD) |
| -------- | ----------- | ----------- |
| 1001     | Acme & Co   | 250.5       |

becomes

```xml
<rows>
  <row>
    <Order_ID>1001</Order_ID>
    <Customer>Acme &amp; Co</Customer>
    <Total_USD>250.5</Total_USD>
  </row>
</rows>
```

## Rules

- Header text is turned into a valid XML name: invalid characters become `_`, and names starting with a digit get a leading `_`.
- Columns with no header are skipped. Duplicate headers become `x`, `x_2`, and so on.
- Blank rows are skipped. Empty cells become empty elements.
- Dates are written in ISO 8601 format. Booleans are written as `true` or `false`.

## Tests

```bash
python -m unittest test_excel_to_xml
```
