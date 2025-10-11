# Column Validator Web App

A Streamlit web application to validate if columns in submitted files match with pre-determined column configurations for different customers and product lines.

## Features

- **Multi-Customer Support**: 5 customers (ABC, SRS, QXO, NVR, WW)
- **Product Line Selection**: 2 product lines per customer (MASTIC, VARIFORM)
- **Column Validation**: 
  - Essential Attribute columns (exact match required)
  - Other columns (flexible matching)
- **File Support**: CSV and Excel files (.csv, .xlsx, .xls)
- **Validation Summary**: Detailed report of missing and extra columns
- **Export Functionality**: Download validation reports as CSV

## Current Configuration

### ABC - MASTIC (Fully Configured)

**Essential Attribute Columns (21):**
- Region, District Num, District Name, Branch, City, State
- Customer, Customer Name, Tran Date, Start Date, End Date
- Customer Invoice #, Item, Qty Sold, Unit of Measure
- Deviation #, Type, Ship-to Number, Invoice Price, Net Price, Reason Code

**Other Columns (23):**
- Vendor Deal, Brand Line Description, Desc, Size, Description
- Special Category, Description 2, Contractor, Ply Gem Item Number
- PC per UOM, Converted Qty, Converted UOM, Branch/Location Combo
- Vlookup, $ Off Per Carton, Transaction Month, Transaction Year
- Deviation Begin Date, Deviation End Date, Total Amount Requested
- Invoice Comments, Month Submitted

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run column_validator.py
```

## Usage

1. **Select Customer and Product Line**: Choose from the dropdown menus
2. **Upload File**: Upload a CSV or Excel file
3. **Review Results**: 
   - View validation summary with metrics
   - Check missing essential columns
   - Review extra columns not in configuration
4. **Export Report**: Download validation results as CSV

## Validation Logic

- **Essential Columns**: Must match exactly (case-sensitive)
- **Other Columns**: Flexible matching, used for reference
- **Missing Essential**: Columns required but not found in file
- **Extra Columns**: Columns in file but not in predetermined list

## Next Steps

- Configure remaining customer/product line combinations
- Add case-insensitive matching options
- Implement fuzzy matching for similar column names
- Add batch file processing
