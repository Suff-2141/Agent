Agent-as-Coder: Bank Statement Parser Generator
An intelligent agent that automatically generates custom bank statement parsers using AI. The agent analyzes sample bank PDFs and CSV data to create tailored Python parsers that can extract transaction data from bank statements.
Agent Overview & Quick Start
Agent Architecture: The Agent-as-Coder operates as an autonomous code generation system following a streamlined workflow: Input Analysis → AI Code Generation → Automated Testing → Deployment. The agent takes bank-specific sample data (PDF statements and CSV schemas), leverages Google's Gemini AI models to generate custom Python parsers using pdfplumber, validates the generated code through automated testing, and deploys working parsers with intelligent retry mechanisms and fallback templates for robust production use.

5-Step Run Process:

1. Install: pip install google-generativeai pdfplumber pandas
2. Setup Data: Create data/{bank_name}/ with {bank}_sample.pdf and {bank}_sample.csv files
3. Configure: Add your Gemini API key in llm_handler.py
4. Generate: "Run python agent.py --icici{bank_name}" to create the parser
5. Use: Import and use the generated parser from custom_parsers/{bank}_parser.py with parse("statement.pdf") function
