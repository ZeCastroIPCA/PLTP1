import json

# Funções para construir o AFND
def generate_afnd(expression):
    if "simb" in expression:
        return generate_afnd_symb(expression["simb"])
    elif "op" in expression:
        if expression["op"] == "alt":
            return generate_afnd_alt(expression["args"])
        elif expression["op"] == "seq":
            return generate_afnd_seq(expression["args"])
        elif expression["op"] == "kle":
            return generate_afnd_kle(expression["args"])

def generate_afnd_symb(symb):
    return {
        "states": ["q0", "q1"],
        "alphabet": [symb],
        "transitions": [
            {"from": "q0", "to": "q1", "symbol": symb}
        ],
        "initial_state": "q0",
        "accepting_states": ["q1"]
    }

def generate_afnd_alt(args):
    afnd1 = generate_afnd(args[0])
    afnd2 = generate_afnd(args[1])

    return {
        "states": ["q0", "q1"] + afnd1["states"] + afnd2["states"],
        "alphabet": list(set(afnd1["alphabet"] + afnd2["alphabet"])),
        "transitions": [
            {"from": "q0", "to": afnd1["initial_state"], "symbol": ""},
            {"from": "q0", "to": afnd2["initial_state"], "symbol": ""},
        ] + [{"from": state, "to": "q1", "symbol": ""} for state in afnd1["accepting_states"]] +
          [{"from": state, "to": "q1", "symbol": ""} for state in afnd2["accepting_states"]] +
          afnd1["transitions"] + afnd2["transitions"],
        "initial_state": "q0",
        "accepting_states": ["q1"]
    }

def generate_afnd_seq(args):
    afnd1 = generate_afnd(args[0])
    afnd2 = generate_afnd(args[1])

    return {
        "states": ["q0", "q1"] + afnd1["states"] + afnd2["states"],
        "alphabet": list(set(afnd1["alphabet"] + afnd2["alphabet"])),
        "transitions": afnd1["transitions"] +
            [{"from": state, "to": afnd2["initial_state"], "symbol": ""} for state in afnd1["accepting_states"]] +
            afnd2["transitions"],
        "initial_state": "q0",
        "accepting_states": ["q1"]
    }

def generate_afnd_kle(args):
    afnd = generate_afnd(args[0])

    return {
        "states": ["q0", "q1"] + afnd["states"],
        "alphabet": afnd["alphabet"],
        "transitions": afnd["transitions"] +
            [{"from": "q0", "to": "q1", "symbol": ""}] +
            [{"from": "q0", "to": afnd["initial_state"], "symbol": ""}] +
            [{"from": state, "to": "q1", "symbol": ""} for state in afnd["accepting_states"]] +
            [{"from": "q1", "to": afnd["initial_state"], "symbol": ""}] +
            [{"from": "q1", "to": "q0", "symbol": ""}],
        "initial_state": "q0",
        "accepting_states": ["q1"]
    }

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        er_json = json.load(f)

    afnd = generate_afnd(er_json)

    with open(output_file, 'w') as f:
        json.dump(afnd, f, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Converts a regular expression to an equivalent nondeterministic finite automaton (AFND) in JSON format.")
    parser.add_argument("input_file", help="Path to the input JSON file containing the regular expression.")
    parser.add_argument("--output", help="Path to the output JSON file containing the generated AFND. If not specified, the result will be printed to the console.")
    args = parser.parse_args()

    main(args.input_file, args.output)
