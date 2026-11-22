from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from casos_teste_nao_validos import *
from tree_decision import *


# X, y = para_X_y(caso_repetido, ["x"]) -> primeiro caso de teste

X, y = load_iris(return_X_y=True)
X = X[:, 2:4]


model = DecisionTreeClassifier(criterion="gini", max_depth=2, random_state=0)
model.fit(X, y)
prevision_sk = model.predict(X)


tree = create_tree(X, y, prof_max=2)
prevision_mine = np.array([predict_tree(tree, cell) for cell in X])

print("previsões sklearn:", prevision_sk)
print("previsões minhas: ", prevision_mine)
print("concordância:", (prevision_mine == prevision_sk).mean())
print("acurácia sklearn:", (prevision_sk == y).mean())
print("acurácia minha:  ", (prevision_mine == y).mean())