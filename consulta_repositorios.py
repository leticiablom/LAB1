import requests
import csv
import time
from config import API_ENDPOINT, API_HEADERS
from queries import build_query  

def execute_query(query_text, max_attempts=3):
    """Executa a query na API com tentativas e backoff exponencial."""
    for attempt in range(max_attempts):
        resp = requests.post(API_ENDPOINT, json={'query': query_text}, headers=API_HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        elif attempt < max_attempts - 1:
            time.sleep(2 ** attempt)
        else:
            raise Exception(f"Falha na query (status {resp.status_code}): {resp.text}")

def collect_repositories(target=100):
    """Coleta repositórios paginados até atingir o número desejado."""
    collected = []
    cursor_marker = None

    while len(collected) < target:
        q = build_query(cursor_marker)
        api_result = execute_query(q)
        
        if 'data' in api_result:
            search_result = api_result['data']['search']
            for edge in search_result['edges']:
                repo_data = edge['node']
                closed = sum(1 for issue in repo_data['issues']['nodes'] if issue['state'] == 'CLOSED')
                open_ = sum(1 for issue in repo_data['issues']['nodes'] if issue['state'] == 'OPEN')
                collected.append([
                    repo_data['name'],
                    repo_data['createdAt'],
                    repo_data['pullRequests']['totalCount'],
                    repo_data['releases']['totalCount'],
                    repo_data['updatedAt'],
                    repo_data['primaryLanguage']['name'] if repo_data.get('primaryLanguage') else 'N/A',
                    closed,
                    open_
                ])
                if len(collected) >= target:
                    break

            if not search_result['pageInfo']['hasNextPage']:
                break
            cursor_marker = search_result['pageInfo']['endCursor']
        else:
            print("Erro na resposta da API:", api_result)
            break

    return collected

def export_to_csv(data, output_file='repositorios.csv'):
    """Salva os dados coletados em um arquivo CSV."""
    header = ['Nome', 'Data de Criação', 'Pull Requests Aceitas', 'Total de Releases',
              'Última Atualização', 'Linguagem Primária', 'Issues Fechadas', 'Issues Abertas']
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerows(data)
    print(f"Dados coletados e salvos em '{output_file}' ({len(data)} repositórios)")

if __name__ == "__main__":
    repos_info = collect_repositories(target=100)
    export_to_csv(repos_info)
