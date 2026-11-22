from tree_decision import arvore

def extract_rules(node, conds=()):
    if "classe" in node:
        return [{"conds": conds, "classe": node["classe"], "n": node["n"], "origem": "arvore"}]

    attribute, threshold = node["atributo"], node["limiar"]
    return (
        extract_rules(node["esq"], conds + ((attribute, "<=", threshold),)) + 
        extract_rules(node["dir"], conds + ((attribute, ">", threshold),))
    )


regras = extract_rules(arvore)


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
        

