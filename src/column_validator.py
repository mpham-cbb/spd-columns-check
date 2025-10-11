import streamlit as st
import pandas as pd
import io
import re
import os
from typing import Dict, List, Tuple, Set
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Column configurations for each customer and product line
COLUMN_CONFIGS = {
    "ABC": {
        "MASTIC": {
            "essential": [
                "Region", "District Num", "District Name", "Branch", "City", "State",
                "Customer", "Customer Name", "Tran Date", "Start Date", "End Date",
                "Customer Invoice #", "Item", "Qty Sold", "Unit of Measure",
                "Deviation #", "Type", "Ship-to Number", "Invoice Price",
                "Net Price", "Reason Code"
            ],
            "other": [
                "Vendor Deal", "Brand Line Description", "Desc", "Size", "Description",
                "Special Category", "Description 2", "Contractor", "Ply Gem Item Number",
                "PC per UOM", "Converted Qty", "Converted UOM", "Branch/Location Combo",
                "Vlookup", "$ Off Per Carton", "Transaction Month", "Transaction Year",
                "Deviation Begin Date", "Deviation End Date", "Total Amount Requested",
                "Invoice Comments", "Month Submitted"
            ]
        },
        "VARIFORM": {
            "essential": [
                "Region", "District Num", "District Name", "Branch", "City", "State",
                "Customer", "Customer Name", "Tran Date", "Start Date", "End Date",
                "Customer Invoice #", "Item", "Qty Sold", "Unit of Measure",
                "JDE #", "Profile", "Type", "Invoice Price", "ABC Price",
                "Reference Customer PO", "Reason Code"
            ],
            "other": [
                "Vendor Deal", "Brand Line Description", "Desc", "Size", "Description",
                "Special Category", "Description", "Pricing UOM", "UOM Conv",
                "SPD Vlook", "Invoice Pc Price", "ABC Piece Price", "Difference",
                "Amount Due", "Credit Month", "Credit Year",
                "Reference Delivery Instructions #1", "Month Submitted"
            ]
        }
    },
    "SRS": {
        "MASTIC": {
            "essential": [
                "Branch ID", "End Customer Number", "End Customer Name", "Item Code",
                "Invoice", "Invoice Date", "Ship Qty", "UOM", "Reason Code", "JDE #",
                "Deviation", "Profile", "Type", "Invoice Price", "Net Price"
            ], 
            "other": [
                "SPD #", "Ship To #", "Distributor Name", "PlyGem Item#", "Item Desc",
                "Job Name", "Color Tier", "Item Description", "SRS Create Date",
                "Rebate Amt", "Rebate", "Invoice Comments", "Vlookup", "Conversion",
                "Converted QTY", "Revised Rebate Due", "Revised Total Rebate"
            ]
        },
        "VARIFORM": {
            "essential": [
                "Branch ID", "End Customer Number", "End Customer Name", "Item Code",
                "Invoice", "Invoice Date", "Ship Qty", "UOM", "Reason Code", "JDE#",
                "Reference Customer PO", "Profile", "Type", "Invoice Price",
                "Rebate Price"
            ], 
            "other": [
                "SPD #", "Ship To #", "Distributor Name", "PlyGem Item#", "Item Desc",
                "Supplier", "Job Name", "SRS Create Date", "Rebate Amt", "Rebate",
                "Reference Delivery Instructions #1", "Vlookup", "Difference",
                "Revised Total Rebate Due"
            ]
        }
    },
    "QXO": {
        "MASTIC": {
            "essential": [
                "Invoice Date", "Invoice Number", "Branch", "City", "State", "Customer #",
                "Customer Name", "Customer Item Number", "Product #",
                "Quantity Purchased", "Unit of Measure", "Reason Code", "JDE #", "SPD",
                "Invoice Price", "SPD Cost"
            ], 
            "other": [
                "Vendor Contract #", "Item Description", "Plygem Item Number",
                "Invoice Notes", "Profile", "Carton Quantity", "Rebate Amount",
                "Total Rebate"
            ]
        },
        "VARIFORM": {
            "essential": [
                "Invoice Date", "Invoice Number", "Branch", "City", "State", "Customer #",
                "Customer Name", "Customer Item Number", "Product #", "Quantity Purchased",
                "Unit of Measure", "Reason Code", "JDE #", "Reference Customer PO", "Type",
                "Invoice Price", "Net Price"
            ], 
            "other": [
                "Vendor Contract #", "Item Description", "Plygem Item Number",
                "Reference Delivery Instructions #1", "Profile", "Vlookup", "Conversion",
                "Carton Quantity", "Difference", "Total Rebate"
            ]
        }
    },
    "NVR": {
        "essential": [
            "Ply Gem Ship-To Number", "Distributor Branch ID", "City", "State",
            "Distributor Region", "Sold To", "Distributor Invoice Date",
            "Distributor Invoice Number", "Distributor Item Number", "Brand",
            "Ply Gem Product Category", "Rebate Profile", "Item Profile",
            "Ply Gem Color Group", "Ply Gem Description", "Series", "Reported Qty",
            "Reported UOM", "Distributor Invoice per Piece", "Branch Cost per Piece"
        ],
        "other": [
            "Distributor", "Month", "Year", "Mastic Vinyl", "TSM #", "TSM Name", "RSM #",
            "RSM Name", "Converted Qty", "Converted UOM (100=SQ 300=CT)",
            "Profile on NVR Program?", "Distributor Credit/(Debit) per piece",
            "Total Distributor Payout", "Date Rebate Processed", "Credit Memo Number",
            "Total Invoice", "Total Branch Cost", "NVR Cost per Piece", "Total NVR Cost"
        ]
    },
    "WW": {
        "essential": [
            "Distributor", "Ply Gem Ship To Number", "Distributor Branch ID", "City",
            "State", "Distributor Region", "Window World Location Number",
            "Window World Location Name", "Distributor Invoice Date",
            "Distributor Invoice Number", "Distributor Item Number", "Ply Gem Category",
            "Ply Gem Rebate Profile", "Ply Gem Description", "Series", "Reported Qty",
            "Reported UOM", "Distributor Invoice Per Unit",
            "Distributor Cost per Unit for Window World Sales"
        ],
        "other": [
            "Month", "Year", "Quarter", "TSM #", "TSM Name", "RSM #", "RSM Name",
            "lookup", "Ply Gem Color Group", "Converted Qty", "Converted UOM",
            "Distributor Credit/(Debit) per Unit", "Total Distributor Payout",
            "Date Rebate Processed", "Credit Memo Number", "Total Distributor Invoice",
            "Total Distributor Cost for Window World Sales", "Window World Cost per Unit",
            "Total Window World Cost"
        ]
    }
}

def validate_file_name(filename: str, customer: str, product_line: str) -> Tuple[bool, str]:
    """
    Validate file name pattern based on customer and product line (CASE SENSITIVE)
    
    Args:
        filename: Name of the uploaded file
        customer: Selected customer
        product_line: Selected product line
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Case sensitive validation - do NOT convert to uppercase
    
    # For NVR and WW customers, no product line needed, just NET_ASP*
    if customer in ["NVR", "WW"]:
        if filename.startswith("NET_ASP"):
            return True, ""
        else:
            return False, f"File name must start with 'NET_ASP' (case sensitive) for {customer} customer"
    
    # For other customers with product lines
    if product_line == "MASTIC":
        if filename.startswith("NET_ASP_MASTIC"):
            return True, ""
        else:
            return False, "File name must start with 'NET_ASP_MASTIC' (case sensitive) for MASTIC product line"
    elif product_line == "VARIFORM":
        if filename.startswith("NET_ASP_VF"):
            return True, ""
        else:
            return False, "File name must start with 'NET_ASP_VF' (case sensitive) for VARIFORM product line"
    
    return True, ""

def validate_columns(file_columns: List[str], customer: str, product_line: str) -> Dict:
    """
    Validate columns against the predetermined configuration
    
    Args:
        file_columns: List of column names from uploaded file
        customer: Selected customer
        product_line: Selected product line (None for NVR/WW)
    
    Returns:
        Dictionary containing validation results
    """
    # Handle NVR and WW customers (no product line)
    if customer in ["NVR", "WW"]:
        config = COLUMN_CONFIGS.get(customer, {})
    else:
        config = COLUMN_CONFIGS.get(customer, {}).get(product_line, {})
    
    essential_cols = set(config.get("essential", []))
    other_cols = set(config.get("other", []))
    file_cols_set = set(file_columns)
    
    # Find missing essential columns (exact match required)
    missing_essential = essential_cols - file_cols_set
    
    # Find extra columns not in predetermined list
    all_predetermined = essential_cols | other_cols
    extra_columns = file_cols_set - all_predetermined
    
    # Find matching columns
    matching_essential = essential_cols & file_cols_set
    matching_other = other_cols & file_cols_set
    
    return {
        "missing_essential": list(missing_essential),
        "extra_columns": list(extra_columns),
        "matching_essential": list(matching_essential),
        "matching_other": list(matching_other),
        "total_file_columns": len(file_columns),
        "total_essential_required": len(essential_cols),
        "total_other_available": len(other_cols)
    }

def display_validation_summary(results: Dict, customer: str, product_line: str):
    """Display the validation results in a formatted way"""
    
    st.subheader(f"📊 Validation Summary for {customer} - {product_line}")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("File Columns", results["total_file_columns"])
    
    with col2:
        essential_match_rate = len(results["matching_essential"]) / max(results["total_essential_required"], 1) * 100
        st.metric("Essential Match", f"{essential_match_rate:.1f}%")
    
    with col3:
        st.metric("Missing Essential", len(results["missing_essential"]))
    
    with col4:
        st.metric("Extra Columns", len(results["extra_columns"]))
    
    # Detailed results
    if results["missing_essential"]:
        st.error("❌ **Missing Essential Columns** (Exact match required)")
        for col in sorted(results["missing_essential"]):
            st.code(f"• {repr(col)}")
    else:
        st.success("✅ All essential columns are present!")
    
    if results["extra_columns"]:
        st.warning("⚠️ **Extra Columns** (Not in predetermined list)")
        for col in sorted(results["extra_columns"]):
            st.code(f"• {repr(col)}")
    
    # Matching columns summary
    with st.expander("📋 Matching Columns Details"):
        if results["matching_essential"]:
            st.write("**✅ Matching Essential Columns:**")
            for col in sorted(results["matching_essential"]):
                st.code(f"• {col}")
        
        if results["matching_other"]:
            st.write("**✅ Matching Other Columns:**")
            for col in sorted(results["matching_other"]):
                st.write(f"• {col}")

def check_authentication():
    """
    Authentication system using environment variables
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 Authentication Required")
        st.markdown("Please enter your credentials to access the Column Validator")
        
        # Get credentials from environment variables with fallback defaults
        # valid_username = os.getenv("VALIDATOR_USERNAME", "admin")
        # valid_password = os.getenv("VALIDATOR_PASSWORD", "validator2024")
        valid_username = os.getenv("GEN_USERNAME")
        valid_password = os.getenv("GEN_PASSWORD")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username == valid_username and password == valid_password:
                    st.session_state.authenticated = True
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
                    st.markdown(
                        "<p style='font-size: 0.9em; color: gray;'>"
                        "If you continue to experience login issues, please contact Mia Pham at "
                        "<a href='mailto:nguyen.pham@cornerstone-bb.com'>nguyen.pham@cornerstone-bb.com</a>."
                        "</p>",
                        unsafe_allow_html=True,
                    )
        
        # Optinal: show environment variable info in development
        if os.getenv("STREAMLIT_ENV") == "development":
            with st.expander("🔧 Development Info"):
                st.info("Environment variables for credentials:")
                st.code("VALIDATOR_USERNAME=your_username\nVALIDATOR_PASSWORD=your_password")
                st.write(f"Current username from env: `{valid_username}`")
        
        st.stop()

def main():
    st.set_page_config(
        page_title="Column Validator",
        page_icon="📊",
        layout="wide"
    )
    
    # Check authentication first
    check_authentication()
    
    # Add logout button in sidebar
    with st.sidebar:
        st.markdown("### 👤 User Session")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.title("📊 File Column Validator")
    st.markdown("Upload files to validate column matching against predetermined configurations")
    
    # Customer and Product Line Selection
    col1, col2 = st.columns(2)
    
    with col1:
        customer = st.selectbox(
            "Select Customer",
            options=list(COLUMN_CONFIGS.keys()),
            index=0
        )
    
    with col2:
        # For NVR and WW, no product line selection needed
        if customer in ["NVR", "WW"]:
            st.info(f"ℹ️ {customer} customer does not require product line selection")
            product_line = None
            # Show expected file pattern
            st.markdown(f"**Expected file pattern:** `NET_ASP*.xlsx`")
        else:
            product_lines = list(COLUMN_CONFIGS[customer].keys())
            product_line = st.selectbox(
                "Select Product Line",
                options=product_lines,
                index=0
            )
            # Show expected file pattern
            if product_line == "MASTIC":
                st.markdown(f"**Expected file pattern:** `NET_ASP_MASTIC*.xlsx`")
            elif product_line == "VARIFORM":
                st.markdown(f"**Expected file pattern:** `NET_ASP_VF*.xlsx`")
    
    # Show current configuration
    if customer not in ["NVR", "WW"] and product_line:
        config = COLUMN_CONFIGS[customer][product_line]
        if config["essential"] or config["other"]:
            with st.expander(f"📋 View {customer} - {product_line} Configuration"):
                if config["essential"]:
                    st.write("**Essential Columns (Exact match required):**")
                    for col in config["essential"]:
                        st.write(f"• {col}")
                
                if config["other"]:
                    st.write("**Other Columns (Flexible):**")
                    for col in config["other"]:
                        st.write(f"• {col}")
        else:
            st.info(f"⚠️ Configuration for {customer} - {product_line} is not yet defined")
    elif customer in ["NVR", "WW"]:
        config = COLUMN_CONFIGS[customer]
        if config["essential"] or config["other"]:
            with st.expander(f"📋 View {customer} Configuration"):
                if config["essential"]:
                    st.write("**Essential Columns (Exact match required):**")
                    for col in config["essential"]:
                        st.write(f"• {col}")
                
                if config["other"]:
                    st.write("**Other Columns (Flexible):**")
                    for col in config["other"]:
                        st.write(f"• {col}")
        else:
            st.info(f"ℹ️ {customer} customer configuration will be applied after file upload")
    
    st.divider()
    
    # File Upload
    uploaded_file = st.file_uploader(
        "Choose a file to validate",
        type=['csv', 'xlsx', 'xls'],
        help="Upload CSV or Excel files"
    )
    
    if uploaded_file is not None:
        # Validate file name pattern
        is_valid_name, name_error = validate_file_name(uploaded_file.name, customer, product_line)
        
        if not is_valid_name:
            st.error(f"❌ **File Name Error:** {name_error}")
            st.info("Please rename your file to match the expected pattern and upload again.")
            return
        else:
            st.success(f"✅ File name pattern is correct: `{uploaded_file.name}`")
        
        try:
            # Read file based on type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, sheet_name='Working Copy')
            
            # Get column names
            file_columns = df.columns.tolist()
            
            # Show exact column names with repr() to see hidden characters
            # st.write("**🔍 EXACT Column Names in Your File:**")
            # for i, col in enumerate(file_columns):
            #     st.code(f"{i+1}. {repr(col)}")
            
            # # Show expected columns
            # if customer not in ["NVR", "WW"]:
            #     config = COLUMN_CONFIGS[customer][product_line]
            #     st.write("**📋 Expected Essential Columns:**")
            #     for i, col in enumerate(config["essential"]):
            #         st.code(f"{i+1}. {repr(col)}")
            # else:
            #     config = COLUMN_CONFIGS[customer]
            #     st.write("**📋 Expected Essential Columns:**")
            #     for i, col in enumerate(config["essential"]):
            #         st.code(f"{i+1}. {repr(col)}")
            
            # Show file preview
            with st.expander("📄 File Preview"):
                st.write(f"**File:** {uploaded_file.name}")
                st.write(f"**Rows:** {len(df)}, **Columns:** {len(df.columns)}")
                st.dataframe(df.head())
            
            # Validate columns
            if customer in ["NVR", "WW"]:
                config = COLUMN_CONFIGS[customer]
                if config["essential"] or config["other"]:
                    results = validate_columns(file_columns, customer, None)
                    display_validation_summary(results, customer, "No Product Line")
                    
                    # Export results option
                    if st.button("📥 Export Validation Report"):
                        report_data = {
                            "Customer": [customer],
                            "Product Line": ["N/A"],
                            "File Name": [uploaded_file.name],
                            "Total File Columns": [results["total_file_columns"]],
                            "Missing Essential": [", ".join(results["missing_essential"])],
                            "Extra Columns": [", ".join(results["extra_columns"])],
                            "Essential Match Rate": [f"{len(results['matching_essential']) / max(results['total_essential_required'], 1) * 100:.1f}%"]
                        }
                        
                        report_df = pd.DataFrame(report_data)
                        csv = report_df.to_csv(index=False)
                        
                        st.download_button(
                            label="Download Report as CSV",
                            data=csv,
                            file_name=f"validation_report_{customer}_NoProductLine.csv",
                            mime="text/csv"
                        )
                else:
                    st.info(f"📋 Column validation for {customer} will be implemented based on your requirements")
                    st.write("**File columns detected:**")
                    for i, col in enumerate(file_columns, 1):
                        st.write(f"{i}. {col}")
            elif product_line and config["essential"] or config["other"]:
                results = validate_columns(file_columns, customer, product_line)
                display_validation_summary(results, customer, product_line)
                
                # Export results option
                if st.button("📥 Export Validation Report"):
                    report_data = {
                        "Customer": [customer],
                        "Product Line": [product_line or "N/A"],
                        "File Name": [uploaded_file.name],
                        "Total File Columns": [results["total_file_columns"]],
                        "Missing Essential": [", ".join(results["missing_essential"])],
                        "Extra Columns": [", ".join(results["extra_columns"])],
                        "Essential Match Rate": [f"{len(results['matching_essential']) / max(results['total_essential_required'], 1) * 100:.1f}%"]
                    }
                    
                    report_df = pd.DataFrame(report_data)
                    csv = report_df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download Report as CSV",
                        data=csv,
                        file_name=f"validation_report_{customer}_{product_line or 'NoProductLine'}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("Cannot validate: Configuration not defined for selected customer and product line")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()
