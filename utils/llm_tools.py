"""LLM interaction utilities for code generation"""
import re
from typing import Dict, Any

def extract_code_blocks(text: str) -> str:
    """Extract Python code from LLM response"""
    # Remove markdown code blocks
    code = re.sub(r'```python\n?', '', text)
    code = re.sub(r'```\n?', '', code)
    
    # Remove any explanatory text before/after code
    lines = code.split('\n')
    code_lines = []
    in_code = False
    
    for line in lines:
        # Detect start of actual code
        if line.strip().startswith(('import ', 'from ', 'def ', 'class ', '#')):
            in_code = True
        
        if in_code:
            code_lines.append(line)
    
    return '\n'.join(code_lines)

def validate_parser_structure(code: str) -> bool:
    """Validate that generated code has required structure"""
    required_patterns = [
        r'def parse\(',
        r'pd\.DataFrame',
        r'return.*DataFrame'
    ]
    
    for pattern in required_patterns:
        if not re.search(pattern, code):
            return False
    
    return True

def format_error_context(error: str, max_length: int = 500) -> str:
    """Format error message for LLM context"""
    # Extract the most relevant error information
    lines = error.split('\n')
    relevant_lines = []
    
    for line in lines:
        if any(keyword in line.lower() for keyword in ['error', 'failed', 'assertion', 'traceback']):
            relevant_lines.append(line)
    
    context = '\n'.join(relevant_lines)
    if len(context) > max_length:
        context = context[:max_length] + '...'
    
    return context