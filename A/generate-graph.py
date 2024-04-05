import json
from graphviz import Source

#Function to generate graph of an automaton
def gerar_grafo_dot(afd):
    dot = "digraph AFD {\n"
    #Iterate over the states
    for transicao in afd["transicoes"]:
        #Add the transition to the graph
        dot += f'    {transicao["origem"]} -> {transicao["destino"]} [label="{transicao["simbolo"]}"];\n'
    #Add the final states to the graph
    dot += "}"
    return dot

#Get the automaton from the JSON file
with open("automato.json", "r") as file:
    automato_json = json.load(file)

#Generate the graph
dot_representation = gerar_grafo_dot(automato_json)
#Save the graph to a file
with open("automato.dot", "w") as file:
    file.write(dot_representation)

# Gerar a imagem do grafo usando Graphviz
graph = Source(dot_representation, filename="automato.dot", format="png")
graph.render()