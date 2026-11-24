# Trabalho2_IA

Agente com aprendizado supervisionado para classificação de leucócitos (neutrófilo, eosinófilo, basófilo, linfócito e monócito) por regras geradas automaticamente. Trabalho 2 da disciplina de Inteligência Artificial (UFSCar, 2026/2).

As dependências do projeto são gerenciadas com o [Poetry](https://python-poetry.org/docs/).

## Sobre o projeto

O agente classifica cada célula a partir de atributos extraídos da imagem (forma, cor e textura) por técnicas de processamento digital de imagens. Nenhuma regra é escrita à mão: elas são geradas por dois algoritmos com vieses de busca diferentes e depois fundidas num único conjunto.

1. **Percepção (PDI):** cada imagem de célula vira uma linha de atributos, como a razão núcleo/citoplasma e o número de lóbulos do núcleo. Os rótulos (classes) vêm do dataset.
2. **Gerador 1: árvore de decisão.** Implementada do zero com o índice de Gini. Cada caminho da raiz até uma folha vira uma regra.
3. **Gerador 2: cobertura sequencial com A\*.** Para cada classe, o A\* encontra a regra com menos condições que atinge uma precisão e uma cobertura mínimas; a cobertura sequencial remove as células cobertas e repete até cobrir a classe.
4. **Fusão das regras:** as regras comuns aos dois geradores entram no conjunto final, e as exclusivas entram por subida de encosta, se melhorarem o F1 macro na validação. Conflitos entre regras são resolvidos pela regra de Bayes.
5. **Comparação:** o conjunto final de regras é comparado com modelos sem regras (k-NN e Naïve Bayes) no mesmo conjunto de teste.

### Situação atual

| Etapa | Situação |
| --- | --- |
| Árvore de decisão (Gini), previsão e extração de regras | Concluída e validada com o scikit-learn (Iris: mesmas previsões, 6 erros em 150) |
| Simplificação das regras | Concluída |
| Gerador 2: A\* e cobertura sequencial | Concluído e testado com os casos de teste |
| Fusão das regras | A fazer |
| Extração de atributos (PDI) | A fazer |
| Comparação com k-NN e Naïve Bayes | A fazer |

## Requisitos

- Python 3.12 ou mais recente
- Poetry 2.x

## 1. Instalar o Poetry

O Poetry é instalado uma única vez por máquina, fora do projeto.

### Linux (e macOS / WSL)

1. Instale com o instalador oficial:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. O Poetry é instalado em `$HOME/.local/bin`. Se essa pasta ainda não estiver no PATH, adicione no final do `~/.bashrc` (ou `~/.zshrc`):

   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

   Depois, recarregue o terminal com `source ~/.bashrc` ou abra um terminal novo.

3. Confira a instalação:

   ```bash
   poetry --version
   ```

### Windows (PowerShell)

1. Instale com o instalador oficial:

   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
   ```

   Se o comando `py` não existir na sua máquina, troque o `py` do final por `python`.

2. O Poetry é instalado em `%APPDATA%\Python\Scripts`. Se essa pasta ainda não estiver no PATH:
   - abra **Configurações > Sistema > Sobre > Configurações avançadas do sistema > Variáveis de Ambiente**;
   - em **Variáveis de usuário**, edite a variável `Path` e adicione `%APPDATA%\Python\Scripts`.

3. Feche e abra o PowerShell (ou o VS Code) e confira a instalação:

   ```powershell
   poetry --version
   ```

### Alternativa: instalar com pipx (Linux e Windows)

Se você já usa o [pipx](https://pipx.pypa.io/), o Poetry também pode ser instalado com:

```bash
pipx install poetry
```

## 2. Instalar as bibliotecas do projeto

Na pasta do projeto (onde está o `pyproject.toml`), rode:

```bash
poetry install
```

O Poetry cria um ambiente virtual na pasta `.venv` do projeto (configurado no `poetry.toml`) e instala exatamente as versões registradas no `poetry.lock`:

| Biblioteca | Uso no projeto |
| --- | --- |
| `numpy` | Matrizes de atributos (X), rótulos (y) e cálculos da árvore |
| `scikit-learn` | Comparação com a árvore implementada do zero e datasets de teste (Iris, Wine) |

O mesmo comando funciona no Linux e no Windows.

## 3. Rodar o código

Os comandos são executados **a partir da pasta raiz do projeto** (onde está o `pyproject.toml`), com `python -m` e o caminho do módulo separado por pontos, sem o `.py`. Assim os imports a partir de `src` funcionam. Com o `poetry run`, o comando usa o ambiente do projeto sem precisar ativá-lo:

```bash
poetry run python -m src.tree_decision.tree_decision
poetry run python -m src.tree_decision.rules
poetry run python -m src.tree_decision.sklearn_comp
poetry run python -m src.a_star.A_star
```

Rodar um arquivo diretamente (por exemplo, `python src/a_star/A_star.py`) dá `ModuleNotFoundError: No module named 'src'`. No VS Code, o botão de executar funciona porque o `.vscode/settings.json` coloca a raiz do projeto no `PYTHONPATH` do terminal integrado.

Para ativar o ambiente e usar `python` diretamente:

- **Linux:**

  ```bash
  eval $(poetry env activate)
  ```

- **Windows (PowerShell):**

  ```powershell
  Invoke-Expression (poetry env activate)
  ```

No VS Code, selecione o interpretador do projeto com **Ctrl+Shift+P > Python: Select Interpreter** e escolha o Python da pasta `.venv`.

## Adicionar uma biblioteca nova

Use o Poetry em vez do `pip install`, para a biblioteca ficar registrada no `pyproject.toml` e no `poetry.lock`:

```bash
poetry add nome-da-biblioteca
```

Depois, faça commit dos dois arquivos. Os outros membros do grupo só precisam rodar `poetry install` de novo.

## Estrutura dos arquivos

```text
Trabalho2_IA/
├── pyproject.toml          # dependências (Poetry)
├── poetry.lock
├── poetry.toml
├── README.md
└── src/
    ├── a_star/
    │   └── A_star.py
    ├── dataset/
    │   └── casos_teste_nao_validos.py
    ├── functions/
    │   └── functions.py
    └── tree_decision/
        ├── tree_decision.py
        ├── rules.py
        └── sklearn_comp.py
```

Cada pasta de `src` tem um `__init__.py` vazio, que a marca como pacote Python. Os imports usam sempre o caminho completo a partir de `src`, por exemplo `from src.functions.functions import gini_function`.

| Arquivo | Conteúdo |
| --- | --- |
| `src/functions/functions.py` | Funções de apoio. **Árvore:** índice de Gini, Gini ponderado, melhor corte de um atributo e melhor divisão entre atributos. **A\*:** células cobertas por uma regra (`covers_rule`), cobertura (`coverage_rule`), precisão (`precision_rule`), limiares candidatos (`thresholds_candidates`) e regras vizinhas (`neighbors`) |
| `src/tree_decision/tree_decision.py` | Gerador 1: construção da árvore de decisão (`create_tree`) e previsão (`predict_tree`) |
| `src/tree_decision/rules.py` | Extração das regras da árvore (`extract_rules`) e simplificação (`simplify_rule`) |
| `src/tree_decision/sklearn_comp.py` | Comparação da árvore implementada com a do scikit-learn |
| `src/a_star/A_star.py` | Gerador 2: busca A\* de uma regra para uma classe (`create_astar`) e cobertura sequencial (`sequencial_coverage`) |
| `src/dataset/casos_teste_nao_validos.py` | Casos de teste em dicionários e a função `para_X_y` |

## Formato das regras

Os dois geradores produzem regras no mesmo formato, o que permite a fusão:

```python
{
    "conds": ((1, "<=", 2.0), (0, "<=", 0.8)),   # (atributo, operador, limiar)
    "classe": "monócito",
    "n": 3,                                        # células de treino cobertas
    "origem": "arvore",                            # ou "astar"
}
```

O número do atributo é a posição da coluna em X. No exemplo, com os atributos `["razao_nc", "lobulos"]`, a regra é: SE lóbulos <= 2 E razão_NC <= 0,8 ENTÃO monócito.

