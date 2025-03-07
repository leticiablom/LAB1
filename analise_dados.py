import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados do CSV
df = pd.read_csv('repositorios.csv')

# Converter colunas de data para datetime (removendo fuso horário)
df['Data de Criação'] = pd.to_datetime(df['Data de Criação']).dt.tz_localize(None)
df['Última Atualização'] = pd.to_datetime(df['Última Atualização']).dt.tz_localize(None)

# Criar colunas calculadas
df['Idade (anos)'] = (pd.Timestamp.today() - df['Data de Criação']).dt.days / 365
df['Tempo desde última atualização (dias)'] = (pd.Timestamp.today() - df['Última Atualização']).dt.days
df['Percentual de Issues Fechadas'] = (df['Issues Fechadas'] / (df['Issues Fechadas'] + df['Issues Abertas'])) * 100

# Remover valores nulos
df.dropna(inplace=True)

# Cálculo das medianas
medianas = {
    "Idade Média (anos)": df["Idade (anos)"].median(),
    "Pull Requests Aceitas": df["Pull Requests Aceitas"].median(),
    "Total de Releases": df["Total de Releases"].median(),
    "Tempo desde Última Atualização (dias)": df["Tempo desde última atualização (dias)"].median(),
    "Percentual de Issues Fechadas": df["Percentual de Issues Fechadas"].median()
}

# Exibir os valores medianos
print("\n=== Valores Medianados ===")
for k, v in medianas.items():
    print(f"{k}: {v:.2f}")

# Criar os gráficos

# Gráfico 1: Distribuição da Idade dos Repositórios
plt.figure(figsize=(10,5))
plt.hist(df["Idade (anos)"], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.xlabel("Idade (anos)")
plt.ylabel("Número de Repositórios")
plt.title("Distribuição da Idade dos Repositórios")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Gráfico 2: Número de Releases vs. Tempo desde Última Atualização
plt.figure(figsize=(10,5))
plt.scatter(df["Total de Releases"], df["Tempo desde última atualização (dias)"], alpha=0.5)
plt.xlabel("Total de Releases")
plt.ylabel("Tempo desde Última Atualização (dias)")
plt.title("Número de Releases vs. Tempo desde Última Atualização")
plt.grid(True)

# Gráfico 3: Percentual de Issues Fechadas
plt.figure(figsize=(10,5))
plt.hist(df["Percentual de Issues Fechadas"], bins=20, color='green', alpha=0.7, edgecolor='black')
plt.xlabel("Percentual de Issues Fechadas")
plt.ylabel("Número de Repositórios")
plt.title("Distribuição do Percentual de Issues Fechadas")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Gráfico 4: Linguagens mais usadas
plt.figure(figsize=(10,5))
df["Linguagem Primária"].value_counts().nlargest(10).plot(kind='bar', color='purple', alpha=0.7, edgecolor='black')
plt.xlabel("Linguagem")
plt.ylabel("Número de Repositórios")
plt.title("Top 10 Linguagens Mais Utilizadas")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Análise por linguagem (RQ 07)
linguagem_analise = df.groupby("Linguagem Primária").median(numeric_only=True)[["Pull Requests Aceitas", "Total de Releases", "Tempo desde última atualização (dias)"]]
linguagem_analise = linguagem_analise.sort_values(by="Pull Requests Aceitas", ascending=False)

# Exibir a tabela das linguagens mais populares
print("\n=== Análise por Linguagem ===")
print(linguagem_analise.head(10))

# Gráfico 5: Contribuições por Linguagem
plt.figure(figsize=(10,5))
linguagem_analise["Pull Requests Aceitas"].nlargest(10).plot(kind='bar', color='red', alpha=0.7, edgecolor='black')
plt.xlabel("Linguagem")
plt.ylabel("Pull Requests Aceitas (mediana)")
plt.title("Top 10 Linguagens com Mais Contribuições Externas")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Exibir todos os gráficos juntos
plt.show()
