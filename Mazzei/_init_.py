from pathlib import Path

from nltk import grammar

data_folder = Path.cwd() / 'Grammars'
data_file = data_folder / "Star_Wars_Grammar.cfg"

sentences = ["Noi siamo illuminati",
             "Tu hai amici lì",
             "Tu avrai novecento anni di età",
             "Skywalker corre veloce",
             "Il futuro di questo ragazzo è nebuloso",
             "Tu hai molto da apprendere ancora",
             "Frase volutamente non supportata dalla grammatica"]

translation_rules = [grammar.Nonterminal('ADJP'), grammar.Nonterminal('ADJ'),
                     grammar.Nonterminal('VBN'),  grammar.Nonterminal('ADVP')]



