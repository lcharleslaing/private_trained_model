# Microsoft Office File Support

## Supported Formats

The system now supports the following Microsoft Office file formats:

### Word Documents
- ✅ **DOCX** (Word 2007+) - Full support
  - Extracts all paragraphs
  - Extracts tables with structure preserved
  - Preserves formatting context

- ⚠️ **DOC** (Word 97-2003) - Limited support
  - Uses python-docx which primarily supports .docx
  - May work for some .doc files but not guaranteed
  - **Recommendation**: Convert .doc to .docx for best results

### Excel Spreadsheets
- ✅ **XLSX** (Excel 2007+) - Full support
- ✅ **XLS** (Excel 97-2003) - Full support
  - Extracts data from all sheets
  - Preserves column headers
  - Extracts row data with structure
  - Limits to 1000 rows per sheet (to avoid processing huge files)

## How It Works

### Word Documents (DOCX)
1. **Paragraphs**: All text paragraphs are extracted
2. **Tables**: Tables are extracted with structure preserved
   - Format: `[Table]:` followed by rows with `|` separators
   - Example: `Row 1: Header1 | Header2 | Header3`

### Excel Files (XLSX, XLS)
1. **All Sheets**: Processes every sheet in the workbook
2. **Headers**: Column headers are extracted for each sheet
3. **Data Rows**: All data rows are extracted (up to 1000 per sheet)
4. **Structure**: Preserves sheet names and row structure
5. **Format**: 
   ```
   [Sheet: Sheet1]
   Headers: Column1 | Column2 | Column3
   Row 1: Value1 | Value2 | Value3
   Row 2: Value4 | Value5 | Value6
   ```

## Installation

Excel support requires additional packages:

```bash
pip install openpyxl pandas
```

These are already included in `requirements.txt`.

## Usage Examples

### Upload Excel File
1. Go to Documents tab
2. Select your .xlsx or .xls file
3. System automatically:
   - Detects all sheets
   - Extracts headers and data
   - Creates searchable chunks
   - Indexes everything

### Ask Questions About Excel Data
- "What are the column headers in Sheet1?"
- "What data is in row 5?"
- "What values are in the Sales column?"
- "Summarize the data in the Budget sheet"

### Upload Word Document
1. Go to Documents tab
2. Select your .docx file
3. System automatically:
   - Extracts all paragraphs
   - Extracts tables
   - Creates searchable chunks
   - Indexes everything

### Ask Questions About Word Documents
- "What tables are in this document?"
- "What is the main content about?"
- "What data is in the first table?"

## Limitations

### Excel Files
- **Row Limit**: Limited to 1000 rows per sheet to avoid processing huge files
- **Formulas**: Only extracted values, not formulas
- **Charts/Images**: Not extracted (only data)
- **Formatting**: Not preserved (only data values)

### Word Documents
- **.doc Files**: Limited support (older format)
  - May not work for all .doc files
  - Recommendation: Convert to .docx
- **Images**: Not extracted (only text and tables)
- **Formatting**: Not preserved (only content)

## Converting .doc to .docx

If you have .doc files, convert them to .docx:

**Using Microsoft Word:**
1. Open .doc file in Word
2. File → Save As
3. Choose "Word Document (*.docx)"
4. Save

**Using LibreOffice (Free):**
1. Open .doc file in LibreOffice Writer
2. File → Save As
3. Choose "ODF Text Document (.odt)" or "Word 2007-365 (.docx)"
4. Save

## Performance

- **Excel files**: Processing time depends on number of sheets and rows
  - Small files (< 100 rows): ~1-2 seconds
  - Medium files (100-1000 rows): ~2-5 seconds
  - Large files (> 1000 rows): ~5-10 seconds (first 1000 rows per sheet)
  
- **Word files**: Generally fast
  - Small documents: < 1 second
  - Large documents with many tables: 1-3 seconds

## Best Practices

1. **Excel Files**:
   - Keep files organized with clear sheet names
   - Use headers in first row
   - For very large files, consider splitting into smaller files

2. **Word Files**:
   - Use .docx format when possible
   - Tables will be extracted and searchable
   - Structure is preserved in the extracted text

3. **Both**:
   - Clear, descriptive content works best
   - Well-organized documents produce better search results

