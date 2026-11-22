
def extract_rules(node, conds=()):
    if "classe" in node:
        return [{"conds": conds, "classe": node["classe"], "n": node["n"], "origem": "arvore"}]

    attribute, threshold = node["atributo"], node["limiar"]
    return (
        extract_rules(node["esq"], conds + ((attribute, "<=", threshold),)) + 
        extract_rules(node["dir"], conds + ((attribute, ">", threshold),))
    )


def simplify_rule(rule):
    best = {}

    for attribute, operator, threshold in rule["conds"]:
        key = (attribute, operator)

        if key not in best:
            best[key] = threshold
        elif operator == "<=":
            best[key] = min(best[key], threshold)
        else:
            best[key] = max(best[key], threshold)

    conds = tuple((attribute, operator, threshold) for (attribute, operator), threshold in best.items())
    return {**rule, "conds": conds}


if __name__ == "__main__":
    from tree_decision import create_tree
    from casos_teste_nao_validos import *

    X, y = para_X_y(caso_repetido, ["x"])
    for regra in extract_rules(create_tree(X, y)):
        print("antes: ", regra["conds"], "->", regra["classe"])
        print("depois:", simplify_rule(regra)["conds"], "->", regra["classe"])
