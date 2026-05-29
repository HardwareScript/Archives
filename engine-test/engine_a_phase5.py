import re

# --- THE RAW HARDWARE SCRIPT (.hw) ---
# This is what the user actually types in their editor
hw_code = """
define Space "SprinklerBoard":
    dimensions: 50mm by 50mm by 2mm
    grid: 50 by 50 by 2

add Transistor_NPN named ValveSwitch at [1, 20, 10] rotated North
"""

# --- TOKEN SPECIFICATION ---
# We use Regex to teach Python how to read Hardware Script
TOKEN_TYPES =[
    ('KEYWORD',   r'\b(define|Space|dimensions|grid|add|named|at|rotated|by)\b'),
    ('STRING',    r'"[^"]*"'),
    ('COORD',     r'\[\d+,\s*\d+,\s*\d+\]'),     # e.g., [1, 20, 10]
    ('MEASURE',   r'\b\d+(?:\.\d+)?(?:mm|cm|V|A)\b'), # e.g., 50mm
    ('NUMBER',    r'\b\d+\b'),
    ('IDENTIFIER',r'[a-zA-Z_][a-zA-Z0-9_]*'),    # e.g., Transistor_NPN
    ('COLON',     r':'),
    ('SKIP',      r'[ \t\n]+'),                  # Ignore spaces and line breaks
    ('MISMATCH',  r'.'),                         # Catch errors
]

# --- THE LEXER ---
def tokenize(code):
    print("🔍 STEP 1: LEXING (Breaking text into tokens)...")
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_TYPES)
    tokens =[]
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"❌ Syntax Error: Unexpected character '{value}'")
        tokens.append((kind, value))
        print(f"   Detected {kind.ljust(12)} : {value}")
    return tokens

# --- THE PARSER ---
def parse(tokens):
    print("\n🧠 STEP 2: PARSING (Translating tokens to Engine A commands)...")
    ast = {"Space": None, "Components":[]}
    
    i = 0
    while i < len(tokens):
        kind, val = tokens[i]
        
        # Parse 'define Space'
        if val == 'define' and tokens[i+1][1] == 'Space':
            space_name = tokens[i+2][1].strip('"')
            ast["Space"] = {"name": space_name}
            print(f"   => Found Space Definition: {space_name}")
            i += 3
            continue
            
        # Parse 'dimensions: Xmm by Ymm by Zmm'
        if val == 'dimensions':
            x = tokens[i+2][1]
            y = tokens[i+4][1]
            z = tokens[i+6][1]
            ast["Space"]["dimensions"] = (x, y, z)
            print(f"   => Parsed Dimensions: X:{x}, Y:{y}, Z:{z}")
            i += 7
            continue
            
        # Parse 'add <Component> named <Name> at [Z, X, Y] rotated <Dir>'
        if val == 'add':
            comp_type = tokens[i+1][1]
            comp_name = tokens[i+3][1]
            coords = tokens[i+5][1]
            rotation = tokens[i+7][1]
            
            ast["Components"].append({
                "type": comp_type,
                "name": comp_name,
                "coords": coords,
                "rotation": rotation
            })
            print(f"   => Parsed Component: {comp_type} '{comp_name}' at {coords} facing {rotation}")
            i += 8
            continue
            
        i += 1
        
    return ast

# --- EXECUTE MVP COMPILER ---
if __name__ == "__main__":
    print("==================================================")
    print("🛠️  HARDWARE SCRIPT COMPILER MVP")
    print("==================================================\n")
    
    # 1. Lexing
    tokens = tokenize(hw_code)
    
    # 2. Parsing
    ast = parse(tokens)
    
    print("\n✅ COMPILATION SUCCESSFUL! The AST is ready for Engine A:")
    print(ast)