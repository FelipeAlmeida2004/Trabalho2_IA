import heapq
from functions import covers_rule, precision_rule, coverage_rule, neighbors, thresholds_candidates

def create_astar(X, y, label, candidates, p_min=0.9, c_min=2, prof_max=3):
    def is_goal(precision, coverage):
        return precision >= p_min and coverage >= c_min

    queue = []
    count = 0
    visited = set()

    mask = covers_rule((), X)
    precision, coverage = precision_rule(mask, y, label), coverage_rule(mask, y, label)
    h = 0 if is_goal(precision, coverage) else 1
    heapq.heappush(queue, (0 + h, -precision, -coverage, count, ()))

    while queue:
        f, less_prec, less_cover, _, conds = heapq.heappop(queue)

        if is_goal(-less_prec, -less_cover):
            return conds

        if len(conds) >= prof_max:
            continue

        for son in neighbors(conds, candidates):
            mask = covers_rule(son, X)
            cover = coverage_rule(mask, y, label)

            if cover < c_min:
                continue

            key = mask.tobytes()

            if key in visited:
                continue

            visited.add(key)
            prec = precision_rule(mask, y, label)
            g = len(son)
            h = 0 if is_goal(prec, cover) else 1
            count += 1
            heapq.heappush(queue, (g + h, -prec, -cover, count, son))
    return None


def sequencial_coverage(X, y, p_min=0.9, c_min=2, prof_max=3):
    candidates = thresholds_candidates(X,y)
    rules = []

    for label in np.unique(y):
        remains = np.ones(len(X), dtype=bool)

        while ((y == label) & remains).sum() >= c_min:
            conds = create_astar(X[remains], y[remains], label, candidates, p_min, c_min, prof_max)

            if conds is None:
                break

            coverage = covers_rule(conds, X)
            rules.append({
                "conds": conds, "classe": label, "n": int(coverage.sum()), "origem": "astar"
            })
            remains &= ~coverage
    return rules


if __name__ == "__main__":
    from casos_teste_nao_validos import *

    X, y = para_X_y(caso_10_celulas, ["razao_nc", "lobulos"])

    for c_min in (2, 1):
        print("c_min =", c_min)
        for rule in sequencial_coverage(X, y, c_min=c_min):
            print("  ", rule["classe"], rule["conds"], "| n =", rule["n"])

    X, y = para_X_y(caso_repetido, ["x"])
    print("caso_repetido:")
    for rule in sequencial_coverage(X, y):
        print("  ", rule["classe"], rule["conds"], "| n =", rule["n"])