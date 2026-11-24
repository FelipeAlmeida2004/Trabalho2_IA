"""Casos de teste para a árvore de decisão (Gini).
Cada célula é um dicionário. A função para_X_y transforma a lista em X (atributos) e y (classes)."""
import numpy as np

def para_X_y(celulas, atributos):
    X = np.array([[c[a] for a in atributos] for c in celulas], dtype=float)
    y = np.array([c["classe"] for c in celulas])
    return X, y

# ---------------------------------------------------------------
# Caso 1: exemplo da "Renda" da Aula 11 (testa o melhor_corte)
# ---------------------------------------------------------------
caso_renda = [
    {"renda": 125, "classe": "não"}, {"renda": 100, "classe": "não"},
    {"renda": 70,  "classe": "não"}, {"renda": 120, "classe": "não"},
    {"renda": 95,  "classe": "sim"}, {"renda": 60,  "classe": "não"},
    {"renda": 220, "classe": "não"}, {"renda": 85,  "classe": "sim"},
    {"renda": 75,  "classe": "não"}, {"renda": 90,  "classe": "sim"},
]

# ---------------------------------------------------------------
# Caso 2: 5 células, 2 atributos (testa melhor_divisao e uma árvore simples)
# ---------------------------------------------------------------
caso_5_celulas = [
    {"razao_nc": 0.40, "area": 950, "classe": "monócito"},
    {"razao_nc": 0.85, "area": 400, "classe": "linfócito"},
    {"razao_nc": 0.45, "area": 900, "classe": "monócito"},
    {"razao_nc": 0.90, "area": 420, "classe": "linfócito"},
    {"razao_nc": 0.80, "area": 410, "classe": "monócito"},
]

# ---------------------------------------------------------------
# Caso 3: as 10 células do desenho, agora com o número de lóbulos
# ---------------------------------------------------------------
caso_10_celulas = [
    {"razao_nc": 0.90, "lobulos": 1, "classe": "linfócito"},
    {"razao_nc": 0.85, "lobulos": 1, "classe": "linfócito"},
    {"razao_nc": 0.82, "lobulos": 1, "classe": "linfócito"},
    {"razao_nc": 0.78, "lobulos": 1, "classe": "monócito"},
    {"razao_nc": 0.60, "lobulos": 4, "classe": "neutrófilo"},
    {"razao_nc": 0.55, "lobulos": 3, "classe": "neutrófilo"},
    {"razao_nc": 0.50, "lobulos": 5, "classe": "neutrófilo"},
    {"razao_nc": 0.48, "lobulos": 1, "classe": "monócito"},
    {"razao_nc": 0.45, "lobulos": 3, "classe": "neutrófilo"},
    {"razao_nc": 0.40, "lobulos": 1, "classe": "monócito"},
]

# ---------------------------------------------------------------
# Caso 4: casos de borda
# ---------------------------------------------------------------
caso_tudo_igual = [   # todas da mesma classe: a raiz já deve ser folha
    {"razao_nc": 0.90, "classe": "linfócito"},
    {"razao_nc": 0.85, "classe": "linfócito"},
    {"razao_nc": 0.70, "classe": "linfócito"},
]
caso_valores_iguais = [   # mesmos valores, classes diferentes: nenhum corte possível
    {"razao_nc": 0.50, "classe": "monócito"},
    {"razao_nc": 0.50, "classe": "neutrófilo"},
    {"razao_nc": 0.50, "classe": "neutrófilo"},
]

# ---------------------------------------------------------------
# Caso 5: atributo repetido no caminho (testa a simplificação das regras)
# Valores 1 a 9 com classes A A A B B B C C C
# ---------------------------------------------------------------
caso_repetido = [
    {"x": 1, "classe": "A"}, {"x": 2, "classe": "A"}, {"x": 3, "classe": "A"},
    {"x": 4, "classe": "B"}, {"x": 5, "classe": "B"}, {"x": 6, "classe": "B"},
    {"x": 7, "classe": "C"}, {"x": 8, "classe": "C"}, {"x": 9, "classe": "C"},
]
