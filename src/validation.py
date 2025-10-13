"""
Validation functions for column names and data types
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
from config import get_column_names, get_expected_data_types

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
    # Get column configuration
    config = get_column_names(customer, product_line)
    essential_cols = set(config["essential"])
    other_cols = set(config["other"])
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

def validate_data_types(df: pd.DataFrame, customer: str, product_line: str = None) -> Dict:
    """
    Validate data types of columns in the DataFrame
    
    Args:
        df: DataFrame to validate
        customer: Selected customer
        product_line: Selected product line (None for NVR/WW)
    
    Returns:
        Dictionary containing data type validation results
    """
    expected_types = get_expected_data_types(customer, product_line)
    file_columns = df.columns.tolist()
    
    type_issues = []
    type_matches = []
    
    for col in file_columns:
        if col in expected_types:
            expected_type = expected_types[col]
            actual_dtype = str(df[col].dtype)
            
            # Check if data type matches expectation
            is_valid = _check_data_type_compatibility(df[col], expected_type)
            
            if is_valid:
                type_matches.append({
                    "column": col,
                    "expected": expected_type,
                    "actual": actual_dtype,
                    "status": "✅ Match"
                })
            else:
                type_issues.append({
                    "column": col,
                    "expected": expected_type,
                    "actual": actual_dtype,
                    "status": "❌ Mismatch",
                    "sample_values": df[col].dropna().head(3).tolist()
                })
    
    return {
        "type_issues": type_issues,
        "type_matches": type_matches,
        "total_checked": len(type_issues) + len(type_matches)
    }

def _check_data_type_compatibility(series: pd.Series, expected_type: str) -> bool:
    """
    Check if a pandas Series is compatible with the expected data type
    More flexible to handle Excel "General" format and pandas auto-inference
    """
    actual_dtype = str(series.dtype)
    
    # Handle different type mappings with flexibility for Excel "General" format
    if expected_type == "string":
        # Accept any type for string - Excel "General" can be anything
        # Most business data should be treated as string even if pandas infers as numeric
        return True
    elif expected_type == "integer":
        # Accept int or numeric that could be int
        if "int" in actual_dtype:
            return True
        if "float" in actual_dtype:
            # Check if all values are whole numbers (could be from Excel General)
            return series.dropna().apply(lambda x: float(x).is_integer()).all()
        if "object" in actual_dtype:
            # Try to convert to see if it's numeric
            return _can_convert_to_numeric(series, "int")
        return False
    elif expected_type == "float":
        # Accept float, int, or convertible numeric
        if "float" in actual_dtype or "int" in actual_dtype:
            return True
        if "object" in actual_dtype:
            return _can_convert_to_numeric(series, "float")
        return False
    elif expected_type == "date":
        return "datetime" in actual_dtype or _can_convert_to_date(series)
    elif expected_type == "boolean":
        return "bool" in actual_dtype or _can_convert_to_boolean(series)
    
    return False

def _can_convert_to_numeric(series: pd.Series, numeric_type: str) -> bool:
    """
    Check if a series can be converted to numeric (int or float)
    """
    try:
        sample = series.dropna().head(10)
        if len(sample) == 0:
            return True
        
        if numeric_type == "int":
            pd.to_numeric(sample, errors='raise').astype(int)
        else:
            pd.to_numeric(sample, errors='raise')
        return True
    except:
        return False

def _can_convert_to_boolean(series: pd.Series) -> bool:
    """
    Check if a series can be converted to boolean
    """
    try:
        sample = series.dropna().head(10)
        if len(sample) == 0:
            return True
        
        # Check if values are boolean-like
        unique_vals = set(str(v).lower() for v in sample.unique())
        boolean_vals = {'true', 'false', '1', '0', 'yes', 'no', 'y', 'n'}
        return unique_vals.issubset(boolean_vals)
    except:
        return False

def _can_convert_to_date(series: pd.Series) -> bool:
    """
    Check if a series can be converted to datetime
    """
    try:
        # Try to convert a sample to datetime
        sample = series.dropna().head(5)
        if len(sample) == 0:
            return True  # Empty series, assume it's fine
        
        pd.to_datetime(sample, errors='raise')
        return True
    except:
        return False

def get_data_type_summary(df: pd.DataFrame) -> List[Dict]:
    """
    Get a summary of all data types in the DataFrame
    """
    summary = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_count = df[col].isnull().sum()
        total_count = len(df[col])
        
        # Get sample values (non-null)
        sample_values = df[col].dropna().head(3).tolist()
        
        summary.append({
            "column": col,
            "dtype": dtype,
            "null_count": null_count,
            "null_percentage": round((null_count / total_count) * 100, 1),
            "sample_values": sample_values
        })
    
    return summary
