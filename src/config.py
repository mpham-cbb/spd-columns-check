"""
Column configurations and data type definitions for all customers
"""
from typing import Dict, List, Any

# Data type mappings
DATA_TYPES = {
    "string": str,
    "integer": int,
    "float": float,
    "date": "datetime64[ns]",
    "boolean": bool
}

# Column configurations with data types
COLUMN_CONFIGS = {
    "ABC": {
        "MASTIC": {
            "essential": {
                "Region": "string",
                "District Num": "string", 
                "District Name": "string",
                "Branch": "string",
                "City": "string", 
                "State": "string",
                "Customer": "string",
                "Customer Name": "string",
                "Tran Date": "date",
                "Start Date": "date",
                "End Date": "date",
                "Customer Invoice #": "string",
                "Item": "string",
                "Qty Sold": "float",
                "Unit of Measure": "string",
                "Deviation #": "string",
                "Type": "string",
                "Ship-to Number": "string",
                "Invoice Price": "float",
                "Net Price": "float",
                "Reason Code": "string"
            },
            "other": {
                "Vendor Deal": "string",
                "Brand Line Description": "string",
                "Desc": "string",
                "Size": "string",
                "Description": "string",
                "Special Category": "string",
                "Description 2": "string",
                "Contractor": "string",
                "Ply Gem Item Number": "string",
                "PC per UOM": "float",
                "Converted Qty": "float",
                "Converted UOM": "string",
                "Branch/Location Combo": "string",
                "Vlookup": "string",
                "$ Off Per Carton": "float",
                "Transaction Month": "string",
                "Transaction Year": "integer",
                "Deviation Begin Date": "date",
                "Deviation End Date": "date",
                "Total Amount Requested": "float",
                "Invoice Comments": "string",
                "Month Submitted": "string"
            }
        },
        "VARIFORM": {
            "essential": {
                "Region": "string",
                "District Num": "string",
                "District Name": "string", 
                "Branch": "string",
                "City": "string",
                "State": "string",
                "Customer": "string",
                "Customer Name": "string",
                "Tran Date": "date",
                "Start Date": "date", 
                "End Date": "date",
                "Customer Invoice #": "string",
                "Item": "string",
                "Qty Sold": "float",
                "Unit Of Measure": "string",
                "JDE #": "string",
                "Profile": "string",
                "Type": "string",
                "Invoice Price": "float",
                "ABC Price": "float",
                "Reference Customer PO": "string",
                "Reason Code": "string"
            },
            "other": {
                "Vendor Deal": "string",
                "Brand Line Description": "string",
                "Desc": "string",
                "Size": "string",
                "Description": "string",
                "Special Category": "string",
                "Description": "string",
                "Pricing UOM": "string",
                "UOM Conv": "float",
                "SPD Vlook": "string",
                "Invoice Pc Price": "float",
                "ABC Piece Price": "float",
                "Difference": "float",
                "Amount Due": "float",
                "Credit Month": "string",
                "Credit Year": "integer",
                "Reference Delivery Instructions #1": "string",
                "Month Submitted": "string"
            }
        }
    },
    "SRS": {
        "MASTIC": {
            "essential": {
                "Branch ID": "string",
                "End Customer Number": "string",
                "End Customer Name": "string",
                "Item Code": "string",
                "Invoice": "string",
                "Invoice Date": "date",
                "Ship Qty": "float",
                "UOM": "string",
                "Reason Code": "string",
                "JDE #": "string",
                "Deviation": "string",
                "Profile": "string",
                "Type": "string",
                "Invoice Price": "float",
                "Net Price": "float"
            },
            "other": {
                "SPD #": "string",
                "Ship To #": "string",
                "Distributor Name": "string",
                "PlyGem Item#": "string",
                "Item Desc": "string",
                "Job Name": "string",
                "Color Tier": "string",
                "Item Description": "string",
                "SRS Create Date": "date",
                "Rebate Amt": "float",
                "Rebate": "float",
                "Invoice Comments": "string",
                "Vlookup": "string",
                "Conversion": "float",
                "Converted QTY": "float",
                "Revised Rebate Due": "float",
                "Revised Total Rebate": "float"
            }
        },
        "VARIFORM": {
            "essential": {
                "Branch ID": "string",
                "End Customer Number": "string",
                "End Customer Name": "string",
                "Item Code": "string",
                "Invoice": "string",
                "Invoice Date": "date",
                "Ship Qty": "float",
                "UOM": "string",
                "Reason Code": "string",
                "JDE#": "string",
                "Reference Customer PO": "string",
                "Profile": "string",
                "Type": "string",
                "Invoice Price": "float",
                "Rebate Price": "float"
            },
            "other": {
                "SPD #": "string",
                "Ship To #": "string",
                "Distributor Name": "string",
                "PlyGem Item#": "string",
                "Item Desc": "string",
                "Supplier": "string",
                "Job Name": "string",
                "SRS Create Date": "date",
                "Rebate Amt": "float",
                "Rebate": "float",
                "Reference Delivery Instructions #1": "string",
                "Vlookup": "string",
                "Difference": "float",
                "Revised Total Rebate Due": "float"
            }
        }
    },
    "QXO": {
        "MASTIC": {
            "essential": {
                "Invoice Date": "date",
                "Invoice Number": "string",
                "Branch": "string",
                "City": "string",
                "State": "string",
                "Customer #": "string",
                "Customer Name": "string",
                "Customer Item Number": "string",
                "Product #": "string",
                "Quantity Purchased": "float",
                "Unit of Measure": "string",
                "Reason Code": "string",
                "JDE #": "string",
                "SPD": "string",
                "Invoice Price": "float",
                "SPD Cost": "float",
                "Type": "string"
            },
            "other": {
                "Vendor Contract #": "string",
                "Item Description": "string",
                "Plygem Item Number": "string",
                "Invoice Notes": "string",
                "Profile": "string",
                "Carton Quantity": "float",
                "Rebate Amount": "float",
                "Total Rebate": "float"
            }
        },
        "VARIFORM": {
            "essential": {
                "Invoice Date": "date",
                "Invoice Number": "string",
                "Branch": "string",
                "City": "string",
                "State": "string",
                "Customer #": "string",
                "Customer Name": "string",
                "Customer Item Number": "string",
                "Product #": "string",
                "Quantity Purchased": "float",
                "Unit of Measure": "string",
                "Reason Code": "string",
                "JDE #": "string",
                "Reference Customer PO": "string",
                "Type": "string",
                "Invoice Price": "float",
                "Net Price": "float"
            },
            "other": {
                "Vendor Contract #": "string",
                "Item Description": "string",
                "Plygem Item Number": "string",
                "Reference Delivery Instructions #1": "string",
                "Profile": "string",
                "Vlookup": "string",
                "Conversion": "float",
                "Carton Quantity": "float",
                "Difference": "float",
                "Total Rebate": "float"
            }
        }
    },
    "NVR": {
        "essential": {
            "Ply Gem Ship-To Number": "string",
            "Distributor Branch ID": "string",
            "City": "string",
            "State": "string",
            "Distributor Region": "string",
            "Sold To": "string",
            "Distributor Invoice Date": "date",
            "Distributor Invoice Number": "string",
            "Distributor Item Number": "string",
            "Brand": "string",
            "Ply Gem Product Category": "string",
            "Rebate Profile": "string",
            "Item Profile": "string",
            "Ply Gem Color Group": "string",
            "Ply Gem Description": "string",
            "Series": "string",
            "Reported Qty": "float",
            "Reported UOM": "string",
            "Distributor Invoice per Piece": "float",
            "Branch Cost per Piece": "float"
        },
        "other": {
            "Distributor": "string",
            "Month": "string",
            "Year": "integer",
            "Mastic Vinyl": "string",
            "TSM #": "string",
            "TSM Name": "string",
            "RSM #": "string",
            "RSM Name": "string",
            "Converted Qty": "float",
            "Converted UOM (100=SQ 300=CT)": "string",
            "Profile on NVR Program?": "string",
            "Distributor Credit/(Debit) per piece": "float",
            "Total Distributor Payout": "float",
            "Date Rebate Processed": "date",
            "Credit Memo Number": "string",
            "Total Invoice": "float",
            "Total Branch Cost": "float",
            "NVR Cost per Piece": "float",
            "Total NVR Cost": "float"
        }
    },
    "WW": {
        "essential": {
            "Distributor": "string",
            "Ply Gem Ship To Number": "string",
            "Distributor Branch ID": "string",
            "City": "string",
            "State": "string",
            "Distributor Region": "string",
            "Window World Location Number": "string",
            "Window World Location Name": "string",
            "Distributor Invoice Date": "date",
            "Distributor Invoice Number": "string",
            "Distributor Item Number": "string",
            "Ply Gem Category": "string",
            "Ply Gem Rebate Profile": "string",
            "Ply Gem Description": "string",
            "Series": "string",
            "Reported Qty": "float",
            "Reported UOM": "string",
            "Distributor Invoice Per Unit": "float",
            "Distributor Cost per Unit for Window World Sales": "float"
        },
        "other": {
            "Month": "string",
            "Year": "integer",
            "Quarter": "string",
            "TSM #": "string",
            "TSM Name": "string",
            "RSM #": "string",
            "RSM Name": "string",
            "lookup": "string",
            "Ply Gem Color Group": "string",
            "Converted Qty": "float",
            "Converted UOM": "string",
            "Distributor Credit/(Debit) per Unit": "float",
            "Total Distributor Payout": "float",
            "Date Rebate Processed": "date",
            "Credit Memo Number": "string",
            "Total Distributor Invoice": "float",
            "Total Distributor Cost for Window World Sales": "float",
            "Window World Cost per Unit": "float",
            "Total Window World Cost": "float"
        }
    }
}

def get_column_names(customer: str, product_line: str = None) -> Dict[str, List[str]]:
    """Get column names (without data types) for backward compatibility"""
    if customer in ["NVR", "WW"]:
        config = COLUMN_CONFIGS[customer]
        return {
            "essential": list(config["essential"].keys()),
            "other": list(config["other"].keys())
        }
    else:
        config = COLUMN_CONFIGS[customer][product_line]
        return {
            "essential": list(config["essential"].keys()),
            "other": list(config["other"].keys())
        }

def get_expected_data_types(customer: str, product_line: str = None) -> Dict[str, str]:
    """Get expected data types for all columns"""
    if customer in ["NVR", "WW"]:
        config = COLUMN_CONFIGS[customer]
        return {**config["essential"], **config["other"]}
    else:
        config = COLUMN_CONFIGS[customer][product_line]
        return {**config["essential"], **config["other"]}
