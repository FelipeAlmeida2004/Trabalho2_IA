
# Função de Gini

TIPOS = ["Linfócitio", "Monócito", "Eosinófilo", "Básofilo", "Neutrófilo"]

def gini_function(labels):
    total = len(labels)
    
    classes = {}
    soma = 0.0

    if total == 0:
        return 0.0

    for classe in labels:
        classes[classe] = classes.get(classe, 0) + 1

    for qnt in classes.values():
        p = qnt / total
        soma += p ** 2

    return 1 - soma

# Exemplo:
# print(gini_function([TIPOS[0] * 3, TIPOS[3] * 2, TIPOS[1], TIPOS[4] * 5]))


# Gini Ponderado
def gini_balanced_function(labels_left, labels_rigth):
    total = len(labels_left) + len(labels_rigth)
    return ((len(labels_left) / total) * gini_function(labels_left) + 
            (len(labels_rigth) / total) * gini_function(labels_rigth))


# Função que válida o melhor corte (baseado em um atributo)
def best_cut(values, labels):
    classes_for_values = {}
    best_threshold, best_gini = None, float("inf")

    # Mapea o valor com a classe correspondente -> {0.5: {"A", "B"}}
    for value, label in zip(values, labels):
        classes_for_values.setdefault(value, set()).add(label)

    sorted_values = sorted(classes_for_values)

    # Válida os pares de classes dois a dois -> (a, b)
    for a, b in zip(sorted_values[:-1], sorted_values[1:]):
        ca, cb = classes_for_values[a], classes_for_values[b]

        if len(ca) == 1 and ca == cb: # Verifica se houve a troca de classes 
            continue

        threshold = (a + b) / 2

        # Gera lista de classes que possuem valores menores e maiores que o limiar
        left = [label for value, label in zip(values, labels) if value <= threshold]
        right = [label for value, label in zip(values, labels) if value > threshold]

        gini = gini_balanced_function(left, right)
        if gini < best_gini:
            best_threshold, best_gini = threshold, gini

    return best_threshold, best_gini

    # Válida a melhor divisão (basedo no melhor atributo)
def best_divider(x, y):
    best_attribute, best_threshold, best_gini = None, None, float("inf")

    for j in range(x.shape[1]):
        threshold, gini = best_cut(x[:, j], y)

        if gini < best_gini:
            best_attribute, best_threshold, best_gini = j, threshold, gini

    return best_attribute, best_threshold, best_gini