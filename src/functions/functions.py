import numpy as np
# ====== Árvore de Decisão ======

# Função de Gini
TIPOS = ["Linfócito", "Monócito", "Eosinófilo", "Basófilo", "Neutrófilo"]

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


# Gini Ponderado
def gini_balanced_function(labels_left, labels_right):
    total = len(labels_left) + len(labels_right)
    return ((len(labels_left) / total) * gini_function(labels_left) + 
            (len(labels_right) / total) * gini_function(labels_right))


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


# Válida a melhor divisão (baseado no melhor atributo)
def best_divider(x, y):
    best_attribute, best_threshold, best_gini = None, None, float("inf")

    for j in range(x.shape[1]):
        threshold, gini = best_cut(x[:, j], y)

        if gini < best_gini:
            best_attribute, best_threshold, best_gini = j, threshold, gini

    return best_attribute, best_threshold, best_gini



# ====== A* ======

# Verifica se o limiar de cada atributo cobre a regra gerada
def covers_rule(conds, X):
    mask = np.ones(len(X), dtype=bool)

    for attribute, operator, threshold in conds:
        if operator == '<=':
            mask &= X[:, attribute] <= threshold
        else:
            mask &= X[:, attribute] > threshold
    return mask


# Conta a quantidade de valores Verdadeiros, verificando a cobetura das regras
def coverage_rule(mask, y, label):
    return int(((y == label) & mask).sum())


def precision_rule(mask, y, label):
    coverage = mask.sum()

    if coverage == 0:
        return 0.0
    return coverage_rule(mask, y, label) / coverage


# Cria uma lista de limiares candidatos
def thresholds_candidates(X, y):
    candidates = []

    for j in range(X.shape[1]):
        classes_values = {}
        for value, label in zip(X[:, j], y):
            classes_values.setdefault(value, set()).add(label)

        values = sorted(classes_values)
        list = []

        for a, b in zip(values[:-1], values[1:]):
            ca, cb = classes_values[a], classes_values[b]
            if len(ca) == 1 and ca == cb:
                continue
            list.append((a+b)/2)
        candidates.append(list)
    return candidates


def neighbors(conds, candidates):
    used = {(attribute, operator) for attribute, operator, _ in conds}
    children = []

    for j, thresholds in enumerate(candidates):
        for op in ("<=", ">"):
            if (j, op) in used:
                continue
            for thr in thresholds:
                children.append(conds + ((j, op, thr),))
    return children