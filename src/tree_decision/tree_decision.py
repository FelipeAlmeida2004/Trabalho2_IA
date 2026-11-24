import numpy as np
from src.functions.functions import gini_function, best_divider

def major_class(y):
    classes, count = np.unique(y, return_counts=True)
    return classes[count.argmax()]

def create_tree(X, y, prof=0, prof_max=3, min_sample=2):
    if gini_function(y) == 0 or prof >= prof_max or len(y) < min_sample:
        return {"classe": major_class(y), "n": len(y)}

    attribute, threshold, gini = best_divider(X, y)
    if attribute is None or gini >= gini_function(y):
        return {"classe": major_class(y), "n": len(y)}

    go_left = X[:, attribute] <= threshold

    return {
        "atributo": attribute, "limiar": threshold, "n": len(y),
        "esq": create_tree(X[go_left], y[go_left], prof + 1, prof_max, min_sample),
        "dir": create_tree(X[~go_left], y[~go_left], prof + 1, prof_max, min_sample),
    }

def predict_tree(node, cell):
    while "classe" not in node:                
        attribute = node["atributo"]
        threshold = node["limiar"]
        if cell[attribute] <= threshold:
            node = node["esq"]               
        else:
            node = node["dir"]                  
    return node["classe"]                      

if __name__ == "__main__":
    from src.dataset.casos_teste_nao_validos import *

    X, y = para_X_y(caso_10_celulas, ["razao_nc", "lobulos"])
    print(create_tree(X, y))