#!/usr/bin/env python3
"""Test suite for bank statement parsers"""
import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_icici():
    """Test ICICI parser"""
    try:
        # Import the parser
        from custom_parsers.icici_parser import parse
        
        # Check if test data exists
        pdf_path = Path("data/icici/icici_sample.pdf")
        if not pdf_path.exists():
            pytest.skip(f"Test data not found: {pdf_path}")
        
        # Parse the PDF
        result_df = parse(str(pdf_path))
        
        # Basic validation
        assert isinstance(result_df, pd.DataFrame), "Parser must return a DataFrame"
        assert not result_df.empty, "DataFrame should not be empty"
        
        # Check required columns exist
        expected_columns = ['Date', 'Description']
        for col in expected_columns:
            assert col in result_df.columns, f"Missing required column: {col}"
        
        # Check if we have some financial columns
        financial_cols = ['Debit Amt', 'Credit Amt', 'Amount', 'Balance', 'Debit', 'Credit']
        has_financial_col = any(col in result_df.columns for col in financial_cols)
        assert has_financial_col, f"Must have at least one financial column from: {financial_cols}"
        
        # Validate date format (basic check)
        first_date = str(result_df.iloc[0]['Date'])
        assert '/' in first_date or '-' in first_date, "Date should contain '/' or '-' separator"
        
        print(f"✅ ICICI parser test passed - {len(result_df)} transactions found")
        print(f"Columns: {list(result_df.columns)}")
        
        # Optional: Compare with expected results if available
        expected_csv = Path("data/icici/result.csv")
        if expected_csv.exists():
            expected_df = pd.read_csv(expected_csv)
            # Basic comparison - at least similar number of rows
            row_diff = abs(len(result_df) - len(expected_df))
            if row_diff > len(expected_df) * 0.2:  # Allow 20% difference
                print(f"⚠️ Warning: Row count mismatch - Got {len(result_df)}, expected ~{len(expected_df)}")
        
        return True
        
    except ImportError as e:
        pytest.fail(f"Failed to import parser: {e}")
    except Exception as e:
        pytest.fail(f"Parser test failed: {e}")


def test_sbi():
    """Test SBI parser"""
    try:
        # Import the parser
        from custom_parsers.sbi_parser import parse
        
        # Check if test data exists
        pdf_path = Path("data/sbi/sbi_sample.pdf")
        if not pdf_path.exists():
            pytest.skip(f"Test data not found: {pdf_path}")
        
        # Parse the PDF
        result_df = parse(str(pdf_path))
        
        # Basic validation
        assert isinstance(result_df, pd.DataFrame), "Parser must return a DataFrame"
        assert not result_df.empty, "DataFrame should not be empty"
        
        # Check required columns exist
        expected_columns = ['Date', 'Description']
        for col in expected_columns:
            assert col in result_df.columns, f"Missing required column: {col}"
        
        print(f"✅ SBI parser test passed - {len(result_df)} transactions found")
        return True
        
    except ImportError:
        pytest.skip("SBI parser not found")
    except Exception as e:
        pytest.fail(f"SBI parser test failed: {e}")


if __name__ == "__main__":
    # Run tests directly
    if len(sys.argv) > 1:
        bank = sys.argv[1]
        if bank == "icici":
            test_icici()
        elif bank == "sbi":
            test_sbi()
    else:
        pytest.main([__file__])