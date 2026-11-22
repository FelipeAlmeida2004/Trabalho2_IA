# Trabalho2_IA

Agente com aprendizado supervisionado para classificação de leucócitos (neutrófilo, eosinófilo, basófilo, linfócito e monócito) por regras geradas automaticamente. Trabalho 2 da disciplina de Inteligência Artificial (UFSCar, 2026/2).

As dependências do projeto são gerenciadas com o [Poetry](https://python-poetry.org/docs/).

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

Com o `poetry run`, o comando usa o ambiente do projeto sem precisar ativá-lo:

```bash
poetry run python tree_decision.py
poetry run python rules.py
poetry run python sklearn_comp.py
```

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

| Arquivo | Conteúdo |
| --- | --- |
| `functions.py` | Índice de Gini, Gini ponderado, melhor corte de um atributo e melhor divisão entre atributos |
| `tree_decision.py` | Construção da árvore de decisão (`create_tree`) e previsão (`predict_tree`) |
| `rules.py` | Extração das regras da árvore (`extract_rules`) e simplificação (`simplify_rule`) |
| `sklearn_comp.py` | Comparação da árvore implementada com a do scikit-learn |
| `casos_teste_nao_validos.py` | Casos de teste em dicionários e a função `para_X_y` |
