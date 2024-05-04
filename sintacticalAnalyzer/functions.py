"""
functions.py
Calculate the first and follow sets of a given grammar
"""


"""
Calcula el conjunto FIRST de un símbolo no terminal en una gramática
:param grammar: la gramática
:param symbol: el símbolo no terminal
:param first_sets: diccionario con los conjuntos FIRST calculados
:return: el conjunto FIRST del símbolo no terminal
"""
def first(grammar, symbol, first_sets):
    if symbol in first_sets:
        return first_sets[symbol]

    first_result = set()
    if symbol not in grammar:
        first_result.add(symbol)
    else:
        for production in grammar[symbol]:
            prod_symbols = production if isinstance(production, tuple) else production.split()
            for prod_symbol in prod_symbols:
                if prod_symbol == symbol:
                    break
                temp_first = first(grammar, prod_symbol, first_sets)
                first_result.update(temp_first - {''})
                if '' not in temp_first:
                    break
            else:
                first_result.add('')
    first_sets[symbol] = first_result
    return first_result

"""
Calcula el conjunto FOLLOW de un símbolo no terminal en una gramática
:param grammar: la gramática
:param symbol: el símbolo no terminal
:param follow_sets: diccionario con los conjuntos FOLLOW calculados
:param first_sets: diccionario con los conjuntos FIRST calculados
:return: el conjunto FOLLOW del símbolo no terminal
"""
def follow(grammar, symbol, follow_sets, first_sets):
    if symbol not in follow_sets:
        follow_sets[symbol] = set()
        if symbol == next(iter(grammar)):
            follow_sets[symbol].add('$')

    for head, productions in grammar.items():
        for production in productions:
            production_parts = production if isinstance(production, tuple) else production.split()
            for i, part in enumerate(production_parts):
                if part == symbol:
                    next_symbols = production_parts[i+1:]
                    if next_symbols:
                        next_first = set()
                        derives_empty = False
                        for ns in next_symbols:
                            temp_first = first(grammar, ns, first_sets)
                            next_first.update(temp_first - {'ε'})
                            if 'ε' in temp_first:
                                derives_empty = True
                                continue
                            else:
                                break
                        if derives_empty:
                            follow_sets[symbol].update(follow_sets[head])
                        follow_sets[symbol].update(next_first)
                    else:
                        if head != symbol:
                            follow(grammar, head, follow_sets, first_sets)
                            follow_sets[symbol].update(follow_sets[head])

def compute_sets(grammar):
    first_sets = {}
    follow_sets = {}
    for nonterminal in grammar:
        first(grammar, nonterminal, first_sets)
    for nonterminal in grammar:
        follow(grammar, nonterminal, follow_sets, first_sets)
    return first_sets, follow_sets

# programmed by @melissaperez_