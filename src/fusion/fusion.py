
import numpy as np
from functions.functions import covers_rule, precision_rule
from tree_decision.tree_decision import major_class
from sklearn.metrics import f1_score


# Verifica se as regras que chegam a mesma classe são iguais e se significam a mesma coisa
def same_rule(rule_a, rule_b, X):
    if rule_a["classe"] != rule_b["classe"]:
        return False

    mask_a = covers_rule(rule_a["conds"], X)
    mask_b = covers_rule(rule_b["conds"], X)

    return np.array_equal(mask_a, mask_b)

def separate_rules(rule_tree, rule_astar, X):
    common, ex_astar, used = [], [], set()

    for b in rule_astar:
        pair = None
        for i, a in enumerate(rule_tree):
            if i not in used and same_rule(a, b, X):
                pair = i
                break

        if pair is None:
            ex_astar.append(a)
        else:
            used.add(pair)
            # Seleciona a menor codição de regras dentre as comuns
            shorter = min(rule_tree[pair], b, key=lambda r: len(r["conds"]))
            common.append(shorter)

    ex_tree = [a for i, a in enumerate(rule_tree) if i not in used]
    return common, ex_astar, ex_tree


# Define quais regras são mais confiavéis
def fit_rule_confidence(rules, X_train, y_train):
    conf = []
    for rule in rules:
        mask = covers_rule(rule["conds"], X_train)
        conf.append(precision_rule(mask,  y_train, rule["classe"]))



def predict_rules(rules, conf, default_class, X):
    fires = np.array([covers_rule(rule["conds"], X) for rule in rules])   
    preds = []

    for k in range(len(X)):
        active = np.flatnonzero(fires[:, k])            
        if len(active) == 0:                            
            preds.append(default_class)
            continue

        candidates = {rules[i]["classe"] for i in active}
        if len(candidates) == 1:                        
            preds.append(candidates.pop())
            continue

        best = active[conf[active].argmax()]          
        preds.append(rules[best]["classe"])

    return np.array(preds)


def final_rules(rule_tree, rule_astar, X_train, y_train, X_val, y_val): 
    common, ex_astar, ex_tree = same_rule(rule_tree, rule_astar, X_train)
    default_class = major_class(y_train)

    def score(rules):
        conf = fit_rule_confidence(rules, X_train, y_train)
        pred = predict_rules(rules, conf, default_class, X_val)
        return f1_score(y_val, pred, average="macro")

    current = list(common)
    candidates = ex_tree + ex_astar
    best_score = score(current)

    while candidates:
        scores = [score(current + [cand]) for cand in candidates]
        j = int(np.argmax(scores))

        if scores[j] <= best_score:
            break

        best_score = score[j]
        current.append(candidates.pop(j))

        info = {
            "comuns": len(common), "ex_tree": len(ex_tree), "ex_astar": len(ex_astar),
            "regras_finais": len(current), "f1": round(best_score, 3)
        }

        return current, info