"""
lexer.py
Lexical analyzer and source code generator
"""

import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from lexicalAnalyzer.yalexParser import YALexParser
import os

def copy_file_contents(source_file_path, output_file_handle):
    """
    Append the contents of a source file to an already open file handle.
    
    Args:
    source_file_path (str): Path to the source file.
    output_file_handle: Open file handle where to append the contents.
    """
    try:
        with open(source_file_path, 'r') as source_file:
            content = source_file.read()
        output_file_handle.write(content)
        print("Content successfully appended from", source_file_path)
    except Exception as e:
        print("Error occurred while appending contents:", e)

def generate_source_code(yalex_path, output_path):
    parser = YALexParser(yalex_path)
    parser.parse()
    tokens = parser.generate_all_regex()

    try:
        with open(output_path, 'w') as f:
            f.write("#LexicalAnalyzer.py\n")
            f.write("from graphviz import Digraph\n")
            f.write("import os\n\n")
            f.write(f"tokens = {tokens}\n\n")

            copy_file_contents('./lexicalAnalyzer/lexerFunctions.py', f)

    except Exception as e:
        print("An error occurred while generating the source code:", e)
        
# programmed by @melissaperez_