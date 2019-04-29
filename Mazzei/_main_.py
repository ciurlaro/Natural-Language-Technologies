from Mazzei._init_ import *
from Mazzei._logic_ import *


with open(data_file, encoding='utf-8') as grammar_file:
    grammar = CFG.fromstring(grammar_file.read())
    data = [line.split() for line in grammar_file]

for sentence in sentences:
    tree = cky_parsing(sentence.split(), grammar, draw=True)
    translate(tree, translation_rules, draw=True)