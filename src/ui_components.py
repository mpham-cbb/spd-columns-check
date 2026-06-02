"""
UI components for the Streamlit app
"""
import streamlit as st
import pandas as pd
from typing import Dict, List
from config import get_column_names, get_expected_data_types

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
    # with st.expander("📋 Matching Columns Details"):
    #     if results["matching_essential"]:
    #         st.write("**✅ Matching Essential Columns:**")
    #         for col in sorted(results["matching_essential"]):
    #             st.write(f"• {col}")
        
    #     if results["matching_other"]:
    #         st.write("**✅ Matching Other Columns:**")
    #         for col in sorted(results["matching_other"]):
    #             st.write(f"• {col}")

def display_data_type_validation(type_results: Dict, customer: str, product_line: str):
    """Display data type validation results"""
    
    st.subheader(f"🔍 Data Type Validation for {customer} - {product_line}")
    
    # Add explanation about Excel General format
    with st.expander("ℹ️ About Data Type Validation"):
        st.info("""
        **Excel "General" Format Handling:**
        - Columns formatted as "General" in Excel are automatically converted by pandas
        - **String columns** accept any data type (most flexible for business data)
        - **Numeric columns** check if data can be converted to numbers
        - **Date columns** check if data can be parsed as dates
        
        This validation is designed to be flexible with Excel's "General" format.
        """)
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Columns Checked", type_results["total_checked"])
    
    with col2:
        st.metric("Type Issues", len(type_results["type_issues"]))
    
    with col3:
        match_rate = len(type_results["type_matches"]) / max(type_results["total_checked"], 1) * 100
        st.metric("Type Match Rate", f"{match_rate:.1f}%")
    
    # Show type issues
    if type_results["type_issues"]:
        st.error("❌ **Data Type Issues**")
        st.info("💡 These issues may not be critical if your Excel columns are formatted as 'General'")
        for issue in type_results["type_issues"]:
            with st.expander(f"🔴 {issue['column']} - {issue['status']}"):
                st.write(f"**Expected:** {issue['expected']}")
                st.write(f"**Pandas Detected:** {issue['actual']}")
                st.write(f"**Sample Values:** {issue['sample_values']}")
                if issue['expected'] == 'string':
                    st.info("💡 String columns are very flexible - this might not be an actual issue.")
    else:
        st.success("✅ All data types are compatible with expectations!")
    
    # Show successful matches in expandable section
    # if type_results["type_matches"]:
    #     with st.expander("✅ Compatible Data Types"):
    #         for match in type_results["type_matches"]:
    #             st.write(f"• **{match['column']}**: Expected {match['expected']}, Got {match['actual']} ✅")

def display_file_analysis(df: pd.DataFrame):
    """Display detailed file analysis"""
    
    file_columns = df.columns.tolist()
    
    # Show exact column names with repr() to see hidden characters
    st.write("**🔍 EXACT Column Names in Your File:**")
    for i, col in enumerate(file_columns):
        st.code(f"{i+1}. {repr(col)}")

def display_expected_configuration(customer: str, product_line: str):
    """Display expected column configuration"""
    
    if customer not in ["NVR", "WW"] and product_line:
        config = get_column_names(customer, product_line)
        expected_types = get_expected_data_types(customer, product_line)

        if product_line in ("MASTIC XREF", "VARIFORM XREF"):
            config_label = f"View {customer} {product_line} Configuration"
        else:
            config_label = f"View {customer} - {product_line} Configuration"

        if config["essential"] or config["other"]:
            with st.expander(f"📋 {config_label}"):
                if config["essential"]:
                    st.write("**Essential Columns (Exact match required):**")
                    for col in config["essential"]:
                        expected_type = expected_types.get(col, "unknown")
                        st.code(f"• {repr(col)} → {expected_type}")
                
                if config["other"]:
                    st.write("**Other Columns (Flexible):**")
                    for col in config["other"]:
                        expected_type = expected_types.get(col, "unknown")
                        st.code(f"• {repr(col)} → {expected_type}")
        else:
            st.info(f"⚠️ Configuration for {customer} - {product_line} is not yet defined")
    elif customer in ["NVR", "WW"]:
        config = get_column_names(customer)
        expected_types = get_expected_data_types(customer)
        
        if config["essential"] or config["other"]:
            with st.expander(f"📋 View {customer} Configuration"):
                if config["essential"]:
                    st.write("**Essential Columns (Exact match required):**")
                    for col in config["essential"]:
                        expected_type = expected_types.get(col, "unknown")
                        st.code(f"• {repr(col)} → {expected_type}")
                
                if config["other"]:
                    st.write("**Other Columns (Flexible):**")
                    for col in config["other"]:
                        expected_type = expected_types.get(col, "unknown")
                        st.code(f"• {repr(col)} → {expected_type}")
        else:
            st.info(f"ℹ️ {customer} customer configuration will be applied after file upload")

def display_data_type_summary(df: pd.DataFrame):
    """Display data type summary table"""
    
    from validation import get_data_type_summary
    
    summary = get_data_type_summary(df)
    
    st.write("**📊 Data Type Summary:**")
    
    # Create a DataFrame for better display
    summary_df = pd.DataFrame([
        {
            "Column": s["column"],
            "Data Type": s["dtype"],
            "Null Count": s["null_count"],
            "Null %": f"{s['null_percentage']}%",
            "Sample Values": str(s["sample_values"][:2])  # Show first 2 samples
        }
        for s in summary
    ])
    
    st.dataframe(summary_df, use_container_width=True)

def create_export_report(results: Dict, type_results: Dict, customer: str, product_line: str, filename: str) -> pd.DataFrame:
    """Create exportable validation report"""
    
    report_data = {
        "Customer": [customer],
        "Product Line": [product_line or "N/A"],
        "File Name": [filename],
        "Total File Columns": [results["total_file_columns"]],
        "Missing Essential": [", ".join(results["missing_essential"])],
        "Extra Columns": [", ".join(results["extra_columns"])],
        "Essential Match Rate": [f"{len(results['matching_essential']) / max(results['total_essential_required'], 1) * 100:.1f}%"],
        "Data Type Issues": [len(type_results.get("type_issues", []))],
        "Data Type Match Rate": [f"{len(type_results.get('type_matches', [])) / max(type_results.get('total_checked', 1), 1) * 100:.1f}%"]
    }
    
    return pd.DataFrame(report_data)
