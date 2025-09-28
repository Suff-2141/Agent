import pdfplumber
import pandas as pd
import re

def parse(pdf_path: str) -> pd.DataFrame:
    """
    Parses an ICICI Bank statement PDF and extracts transaction data.

    Returns a DataFrame with columns:
        - Date
        - Description
        - Debit Amt
        - Credit Amt
        - Balance
    """
    data = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                lines = text.split('\n')
                for i in range(len(lines)):
                    line = lines[i]

                    # Match date formats
                    date_match = re.search(r'(\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}|\d{2}\s[A-Za-z]{3}\s\d{4})', line)
                    if date_match:
                        date_str = date_match.group(1)
                        description = ""
                        debit_amt = None
                        credit_amt = None
                        balance = None

                        # Extract description
                        desc_match = re.search(r'^\s*(?:\d{2}[-/]\d{2}[-/]\d{4}|\d{2}\s[A-Za-z]{3}\s\d{4})\s+(.*?)\s*$', line)
                        if desc_match:
                            description = desc_match.group(1).strip()

                        # Extract amounts from current line
                        amounts = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', line)
                        if len(amounts) >= 2:
                            try:
                                amt1 = float(amounts[0].replace(',', ''))
                                debit_amt = amt1 if amt1 > 0 else None
                            except ValueError:
                                debit_amt = None
                            try:
                                amt2 = float(amounts[1].replace(',', ''))
                                credit_amt = amt2 if amt2 > 0 else None
                            except ValueError:
                                credit_amt = None
                        elif len(amounts) == 1:
                            try:
                                balance = float(amounts[0].replace(',', ''))
                            except ValueError:
                                balance = None

                        # Check next line for missing balance
                        if balance is None and i + 1 < len(lines):
                            next_line = lines[i+1]
                            balance_match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d{2})', next_line)
                            if balance_match:
                                try:
                                    balance = float(balance_match.group(1).replace(',', ''))
                                except ValueError:
                                    balance = None

                        # Check next line for missing debit/credit
                        if debit_amt is None and credit_amt is None and i + 1 < len(lines):
                            next_line = lines[i+1]
                            next_amounts = re.findall(r'(\d{1,3}(?:,\d{3})*\.\d{2})', next_line)
                            if len(next_amounts) >= 2:
                                try:
                                    amt1 = float(next_amounts[0].replace(',', ''))
                                    debit_amt = amt1 if amt1 > 0 else None
                                except ValueError:
                                    debit_amt = None
                                try:
                                    amt2 = float(next_amounts[1].replace(',', ''))
                                    credit_amt = amt2 if amt2 > 0 else None
                                except ValueError:
                                    credit_amt = None

                        data.append({
                            "Date": date_str,
                            "Description": description,
                            "Debit Amt": debit_amt,
                            "Credit Amt": credit_amt,
                            "Balance": balance
                        })

    except Exception as e:
        print(f"⚠️ Failed to parse PDF: {e}")

    return pd.DataFrame(data)
