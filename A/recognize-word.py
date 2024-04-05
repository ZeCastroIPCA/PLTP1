import json

#Function to recognize a word in an automaton
def reconhecer_palavra(afd, palavra):
    #Start at the initial state
    estado_atual = afd["estado_inicial"]
    #The path of states visited
    caminho = [estado_atual]
    
    #Iterate over the word
    for simbolo in palavra:
        #Get the possible transitions from the current state with the current symbol
        transicoes_possiveis = [t for t in afd["transicoes"] if t["origem"] == estado_atual and t["simbolo"] == simbolo]
        #If there is no transition available, the word is not recognized
        if not transicoes_possiveis:
            return False, caminho, f"Não há transição disponível para o símbolo {simbolo} a partir do estado {estado_atual}"
        
        #Move to the next state
        estado_atual = transicoes_possiveis[0]["destino"]
        caminho.append(estado_atual)
    
    #Check if the final state is a final state
    if estado_atual in afd["estados_finais"]:
        return True, caminho, None
    else:
        return False, caminho, f"O estado atual {estado_atual} não é um estado final"

#Get the automaton from the JSON file
with open("automato.json", "r") as file:
    automato_json = json.load(file)

#Test the word "001"
palavra_teste = "001"

#Recognize the word
reconhecido, caminho, erro = reconhecer_palavra(automato_json, palavra_teste)

#Print the result
print(f"A palavra '{palavra_teste}' é reconhecida: {reconhecido}")
print(f"Caminho: {' -> '.join(caminho)}")

#Print the error message if the word is not recognized
if not reconhecido:
    print(f"Erro: {erro}")
