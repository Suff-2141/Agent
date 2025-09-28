def generate_fallback_parser(bank):
    return f'''import pandas as pd, pdfplumber, re

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text() or ""
            for line in text.split("\\n"):
                parts = line.split()
                if len(parts) >= 3:
                    # Assume first token = Date, last token = Amount, rest = Description
                    date, *desc, amt = parts
                    rows.append({{
                        "Date": date,
                        "Description": " ".join(desc),
                        "Amount": amt
                    }})
    return pd.DataFrame(rows)
'''
