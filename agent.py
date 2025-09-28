import argparse
import sys
from pathlib import Path
from utils.llm_handler import LLMHandler
from utils.parser_utils import save_parser, test_parser
from utils.fallback import generate_fallback_parser

api_key = "AIzaSyBmtSY8K-nu6_X0A8Ow6ptZgRKABCj42d4"
model = LLMHandler(api_key, "gemini-2.0-flash-lite")

def read_files(bank: str):
    """Read PDF and CSV sample files for the given bank."""
    pdf = Path(f"data/{bank}/{bank}_sample.pdf")
    csv = Path(f"data/{bank}/{bank}_sample.csv")
    if not csv.exists():
        csv = Path(f"data/{bank}/result.csv")
    return pdf, csv.read_text() if csv.exists() else ""

def generate_parser(bank: str, csv_data: str):
    """
    Generate a Python parser for the bank statement.
    Falls back to default parser if model fails.
    Ensures code-only output without explanations.
    """
    schema = csv_data[:200] if csv_data else "Date,Description,Amount"
    prompt = f"""
Generate a Python parser for {bank} bank statement PDFs.
Function signature: parse(pdf_path: str) -> pd.DataFrame
CSV schema: {schema}
Use pdfplumber.
Return a pandas DataFrame.
DO NOT include explanations, markdown, or extra comments.
Code only.
"""

    try:
        code = model.generate(prompt, max_output_tokens=1000)
        if not code:
            raise ValueError("Empty response from model")

        clean_code = code.replace("```python", "").replace("```", "").strip()
        return clean_code
    except Exception as e:
        print(f"⚠️ Parser generation failed: {e}")
        return generate_fallback_parser(bank)

def save_parser(bank: str, code: str):
    """Save generated parser code to a file."""
    path = Path(f"custom_parsers/{bank}_parser.py")
    path.parent.mkdir(exist_ok=True)
    path.write_text(code, encoding="utf-8")
    return path

def main():
    parser = argparse.ArgumentParser(description="Generate a bank statement parser")
    parser.add_argument("--target", required=True, help="Bank name to generate parser for")
    args = parser.parse_args()

    bank = args.target.lower()
    print(f"Generating parser for {bank}...")

    pdf, csv = read_files(bank)
    path = Path(f"custom_parsers/{bank}_parser.py")

    if path.exists():
        print(f"Parser for {bank} already exists: {path}")
    else:
        code = generate_parser(bank, csv)
        path = save_parser(bank, code)
        print(f"Parser saved: {path}")

    if test_parser(bank):
        print("✅ Tests passed")
    else:
        print("❌ Tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
