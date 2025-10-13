"""
Column Validator - Main Streamlit Application
Reorganized version with data type validation
"""
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Import our modules
from config import COLUMN_CONFIGS
from validation import validate_file_name, validate_columns, validate_data_types
from ui_components import (
    display_validation_summary, 
    display_data_type_validation,
    display_file_analysis,
    display_expected_configuration,
    display_data_type_summary,
    create_export_report
)

# Load environment variables
load_dotenv()

def check_authentication():
    """Authentication system using environment variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 Authentication Required")
        st.markdown("Please enter your credentials to access the Column Validator")
        
        # Get credentials from environment variables with fallback defaults
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
        
        # Show environment variable info in development
        if os.getenv("STREAMLIT_ENV") == "production":
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
        
        st.markdown("### ⚙️ Validation Options")
        validate_data_types_enabled = st.checkbox("Enable Data Type Validation", value=True)
        show_file_analysis = st.checkbox("Show Detailed File Analysis", value=False)
        show_data_summary = st.checkbox("Show Data Type Summary", value=False)
    
    st.title("📊 File Column Validator")
    st.markdown("Upload files to validate column matching and data types against predetermined configurations")
    
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
            st.markdown(f"**Expected file pattern:** `NET_ASP*`")
        else:
            product_lines = list(COLUMN_CONFIGS[customer].keys())
            product_line = st.selectbox(
                "Select Product Line",
                options=product_lines,
                index=0
            )
            # Show expected file pattern
            if product_line == "MASTIC":
                st.markdown(f"**Expected file pattern:** `NET_ASP_MASTIC*`")
            elif product_line == "VARIFORM":
                st.markdown(f"**Expected file pattern:** `NET_ASP_VF*`")
    
    # Show current configuration
    display_expected_configuration(customer, product_line)
    
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
            
            # # Show detailed file analysis if enabled
            # if show_file_analysis:
            #     with st.expander("🔍 Detailed File Analysis"):
            #         display_file_analysis(df)
            
            # # Show data type summary if enabled
            # if show_data_summary:
            #     with st.expander("📊 Data Type Summary"):
            #         display_data_type_summary(df)
            
            # Show file preview
            with st.expander("📄 File Preview"):
                st.write(f"**File:** {uploaded_file.name}")
                st.write(f"**Rows:** {len(df)}, **Columns:** {len(df.columns)}")
                st.dataframe(df.head())
            
            # Get column names
            file_columns = df.columns.tolist()
            
            # Validate columns
            if customer in ["NVR", "WW"]:
                results = validate_columns(file_columns, customer, None)
                display_validation_summary(results, customer, "No Product Line")
                # Show detailed file analysis if enabled
                if show_file_analysis:
                    with st.expander("🔍 Detailed File Analysis"):
                        display_file_analysis(df)
                
                # Data type validation if enabled
                if validate_data_types_enabled:
                    type_results = validate_data_types(df, customer)
                    display_data_type_validation(type_results, customer, "No Product Line")
                    # Show data type summary if enabled
                    if show_data_summary:
                        with st.expander("📊 Data Type Summary"):
                            display_data_type_summary(df)
                else:
                    type_results = {"type_issues": [], "type_matches": [], "total_checked": 0}
                
                # Export results option
                if st.button("📥 Export Validation Report"):
                    report_df = create_export_report(results, type_results, customer, "N/A", uploaded_file.name)
                    csv = report_df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download Report as CSV",
                        data=csv,
                        file_name=f"validation_report_{customer}_NoProductLine.csv",
                        mime="text/csv"
                    )
            else:
                # Regular customers with product lines
                results = validate_columns(file_columns, customer, product_line)
                display_validation_summary(results, customer, product_line)
                # Show detailed file analysis if enabled
                if show_file_analysis:
                    with st.expander("🔍 Detailed File Analysis"):
                        display_file_analysis(df)
                
                # Data type validation if enabled
                if validate_data_types_enabled:
                    type_results = validate_data_types(df, customer, product_line)
                    display_data_type_validation(type_results, customer, product_line)
                    # Show data type summary if enabled
                    if show_data_summary:
                        with st.expander("📊 Data Type Summary"):
                            display_data_type_summary(df)
                else:
                    type_results = {"type_issues": [], "type_matches": [], "total_checked": 0}
                
                # Export results option
                if st.button("📥 Export Validation Report"):
                    report_df = create_export_report(results, type_results, customer, product_line, uploaded_file.name)
                    csv = report_df.to_csv(index=False)
                    
                    st.download_button(
                        label="Download Report as CSV",
                        data=csv,
                        file_name=f"validation_report_{customer}_{product_line}.csv",
                        mime="text/csv"
                    )
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    main()
