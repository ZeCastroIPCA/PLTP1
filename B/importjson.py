import json

class Node:
    def __init__(self, op, args=None, symbol=None):
        self.op = op
        self.args = args if args else []
        self.symbol = symbol

def convert_to_afnd(root):
    afnd = {"states": [], "alphabet": [], "transitions": [], "start_state": "", "accept_states": []}
    state_count = 0

    def add_state():
        nonlocal state_count
        state_name = f"q{state_count}"
        state_count += 1
        afnd["states"].append(state_name)
        return state_name

    def process_node(node):
        if node.op == 'alt':
            state = add_state()
            afnd["transitions"].append({"from": state, "to": process_node(node.args[0]), "symbol": "epsilon"})
            afnd["transitions"].append({"from": state, "to": process_node(node.args[1]), "symbol": "epsilon"})
            return state
        elif node.op == 'seq':
            left = process_node(node.args[0])
            right = process_node(node.args[1])
            afnd["transitions"].append({"from": left, "to": right, "symbol": "epsilon"})
            return left
        elif node.op == 'kle':
            start = add_state()
            end = add_state()
            afnd["transitions"].append({"from": start, "to": end, "symbol": "epsilon"})
            afnd["transitions"].append({"from": start, "to": process_node(node.args[0]), "symbol": "epsilon"})
            afnd["transitions"].append({"from": process_node(node.args[0]), "to": end, "symbol": "epsilon"})
            afnd["transitions"].append({"from": end, "to": start, "symbol": "epsilon"})
            return start
        elif node.symbol:
            afnd["alphabet"].append(node.symbol)
            state = add_state()
            afnd["transitions"].append({"from": state, "to": add_state(), "symbol": node.symbol})
            return state

    start_state = process_node(expression_tree)
    afnd["start_state"] = start_state
    afnd["accept_states"] = [f"q{state_count - 1}"]

    return afnd

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert regular expression to NFA.")
    parser.add_argument("input_file", type=str, help="Input JSON file containing the regular expression")
    parser.add_argument("--output", "-o", type=str, default="afnd.json", help="Output JSON file for the generated AFND")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        data = json.load(f)

    expression_tree = parse_json_to_tree(data)
    afnd = convert_to_afnd(expression_tree)

    with open(args.output, "w") as f:
        json.dump(afnd, f, indent=4)

if __name__ == "__main__":
    main()
