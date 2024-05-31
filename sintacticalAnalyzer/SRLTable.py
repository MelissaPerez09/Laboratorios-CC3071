"""
SLRTable.py
Creación de tabla de análisis sintáctico SRL
"""

from tabulate import tabulate

def generate_grammar_rules(grammar):
    grammar_rules = []
    for head, productions in grammar.items():
        for production in productions:
            grammar_rules.append((head, production))
    return grammar_rules

def print_parsing_table(action_table, goto_table, terminals, non_terminals, num_states, grammar_rules):
    print("\n----------------------------\nSRL Table:\n----------------------------")
    # Ensure terminals and non_terminals are sorted lists
    terminals = sorted(list(terminals))
    non_terminals = sorted(list(non_terminals))
    
    headers = ["State"] + terminals + ["$"] + non_terminals
    rows = []

    for state in range(num_states):
        row = [state]
        for symbol in terminals + ["$"]:
            action = action_table.get((state, symbol))
            if action:
                if action[0] == 'shift':
                    row.append(f"S{action[1]}")
                elif action[0] == 'reduce':
                    # Find the index of the rule in grammar_rules
                    prod_index = grammar_rules.index((action[1], tuple(action[2])))
                    row.append(f"R{prod_index}")
                elif action[0] == 'accept':
                    row.append("accept")
                elif action[0] == 'error':
                    row.append("error")
            else:
                row.append("")

        for symbol in non_terminals:
            goto_state = goto_table.get((state, symbol))
            if goto_state is not None:
                row.append(f"I{goto_state}")
            else:
                row.append("")

        rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt='grid'))
    
    with open('table.txt', 'w') as f:
        f.write(tabulate(rows, headers=headers, tablefmt='grid'))