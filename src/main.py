"""
main.py
Lexical and syntactical analyzer main, no UI
"""
import sys
sys.path.insert(0, '/Users/melissa/Desktop/UVG/lenguajes/CC3071-LabAB/')

from src.LexSyn import *

yalex_path = './yalex/hard.yal'
yapar_path = './yapar/hard.yalp'
chars_path = './chars/hard.txt'

LexSyn(yalex_path, yapar_path, chars_path)

# programmed by @melissaperez_