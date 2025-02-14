
#  LAB1 - Coleta de Dados de Repositórios Populares no GitHub

Este projeto tem como objetivo coletar informações dos **100 repositórios mais populares** do GitHub utilizando a **API GraphQL**. Os dados extraídos serão usados para responder a questões de pesquisa relacionadas à **maturidade**, **popularidade**, **atualizações** e **engajamento** dos repositórios.

As informações são salvas no arquivo `repositorios.csv`, permitindo análises posteriores.

---

##  Dependências

- `requests` - Para fazer requisições HTTP para a API do GitHub.
- `gql` - Para interagir com a API GraphQL do GitHub.

---

## 🛠 Como configurar o ambiente
1. **Gerar um Token de Acesso no GitHub**.
2. **Baixar o projeto**:

   ```bash
   git clone 
   cd nome-do-repositorio
   ```
3. **Criar o ambiente virtual**:

   ```bash
   python3 -m venv .venv
   ```

4. **Ativar o ambiente virtual**:

   ```bash
   .venv\Scripts\activate     # Windows
   ```

5. **Instalar dependências**:

   ```bash
   pip install requests gql
   ```
   
6. **Configurar o token no código**.
7. **Executar o script**:

   ```bash
   python consulta_repositorios.py
   ```

8. **Verificar os dados salvos** (`repositorios.csv`).

