import json
import argparse

def load_afd(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        epsilon_transitions = [t for t in transitions if t['from'] == state and t['symbol'] == '']
        for transition in epsilon_transitions:
            if transition['to'] not in closure:
                closure.add(transition['to'])
                stack.append(transition['to'])
    
    return closure

def move(states, symbol, transitions):
    result = set()
    for state in states:
        symbol_transitions = [t for t in transitions if t['from'] == state and t['symbol'] == symbol]
        for transition in symbol_transitions:
            result.add(transition['to'])
    return result

def save_afd(afd, filename):
    with open(filename, 'w') as f:
        json.dump(afd, f, indent=4)

def visualize_afd_with_graphviz(afd):
    try:
        import graphviz
    except ImportError:
        print("Graphviz is required for visualization. Please install graphviz package.")
        return
    
    dot = graphviz.Digraph(comment='Automato Finito Deterministico')
    for state in afd['states']:
        label = ''.join(state)
        if state in afd['accepting_states']:
            dot.node(label, label=label, shape='doublecircle')
        else:
            dot.node(label, label=label)
    for transition in afd['transitions']:
        dot.edge(''.join(transition['from']), ''.join(transition['to']), label=transition['symbol'])
    
    dot.render('afd_graph', format='png', cleanup=True)

def main():
    parser = argparse.ArgumentParser(description="Converts a nondeterministic finite automaton (AFND) to a deterministic finite automaton (AFD) using JSON format.")
    parser.add_argument("input_file", help="Path to the input JSON file containing the AFND.")
    parser.add_argument("-output", help="Path to the output JSON file containing the generated AFD.")
    parser.add_argument("-graphviz", action='store_true', help="Visualize the generated AFD using Graphviz (requires Graphviz to be installed).")
    args = parser.parse_args()
    
    afd = load_afd(args.input_file)
    
    if args.output:
        save_afd(afd, args.output)
        print(f"AFD saved to {args.output}")
    
    if args.graphviz:
        visualize_afd_with_graphviz(afd)
        print("AFD visualized with Graphviz (afd_graph.png)")

if __name__ == "__main__":
    main()
