import json
import httpx
import concurrent.futures
from tqdm import tqdm

# Função para exibir o banner de informações
def exibir_banner():
    banner = '''
    ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗██╗██╗     
    ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██║   ██║██║██║     
    ██████╔╝ ╚████╔╝ █████╗  ██████╔╝██║   ██║██║██║     
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██╔══██╗██║   ██║██║██║     
    ██║        ██║   ███████╗██║  ██║╚██████╔╝██║███████╗
    ╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚══════╝
                                                      
    Script de Brute Force de Diretórios Web
    ----------------------------------------
    
    Este script permite realizar um brute force em diretórios web. Ele irá iterar sobre uma lista de URLs base e uma wordlist de diretórios, fazendo requisições HTTP para cada combinação URL/diretório e exibindo as URLs ativas encontradas.
    
    Modo de uso:
    1. Insira o nome do arquivo JSON com as URLs base.
    2. Insira o nome do arquivo da wordlist contendo os diretórios a serem testados.
    3. Aguarde o processamento.
    4. Ao final da execução, você terá a opção de salvar os resultados em um arquivo JSON, TXT ou sair.
    
    ----------------------------------------
    '''

    print(banner)

# Exibe o banner
exibir_banner()

# Solicita o nome do arquivo JSON
nome_arquivo_json = input("Digite o nome do arquivo JSON com as URLs: ")

# Abre o arquivo JSON
with open(nome_arquivo_json, 'r') as arquivo_json:
    urls = json.load(arquivo_json)

# Solicita o nome do arquivo de wordlist
nome_arquivo_wordlist = input("Digite o nome do arquivo de wordlist: ")

# Abre o arquivo de wordlist
with open(nome_arquivo_wordlist, 'r') as arquivo_wordlist:
    wordlist = arquivo_wordlist.read().splitlines()

# Inicializa a barra de progresso
total_iteracoes = len(urls) * len(wordlist)
pbar = tqdm(total=total_iteracoes, ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', position=1)

# Lista para armazenar os resultados
resultados = []

# Função para fazer a requisição HTTP em uma URL
def fazer_requisicao(url_completa):
    with httpx.Client() as client:
        response = client.get(url_completa)
        return url_completa if response.status_code == 200 else None

# Função para processar as URLs e wordlist
def processar_urls(urls, wordlist):
    for url in urls:
        for diretorio in wordlist:
            # Monta a URL completa do diretório
            url_completa = url + "/" + diretorio
            
            # Envia a requisição HTTP
            resultado = fazer_requisicao(url_completa)
            
            # Atualiza a barra de progresso
            pbar.update(1)
            
            # Exibe o resultado se houver
            if resultado:
                resultados.append(resultado)

# Define o número máximo de threads (pode ser ajustado)
NUM_THREADS = 10

# Divide as URLs em grupos para processamento paralelo
grupos_urls = [urls[i:i+NUM_THREADS] for i in range(0, len(urls), NUM_THREADS)]

# Cria um executor de threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Inicia as threads para processar os grupos de URLs
    futures = [executor.submit(processar_urls, grupo, wordlist) for grupo in grupos_urls]
    
    # Aguarda todas as threads serem concluídas
    concurrent.futures.wait(futures)

# Fecha a barra de progresso
pbar.close()

# Exibe os resultados encontrados
print("\n--- Resultados ---")
for resultado in resultados:
    print(resultado)

# Pergunta ao usuário o formato para salvar o resultado
opcao = input("\nDigite o número correspondente à opção desejada:\n1. Salvar em arquivo JSON\n2. Salvar em arquivo TXT\n3. Sair\nOpção: ")

if opcao == "1":
    # Solicita o nome do arquivo de saída JSON
    nome_arquivo_saida = input("Digite o nome do arquivo de saída JSON: ")
    
    # Salva os resultados em um arquivo JSON
    with open(nome_arquivo_saida, 'w') as arquivo_saida:
        json.dump(resultados, arquivo_saida)
        print(f"Os resultados foram salvos em {nome_arquivo_saida}.")
elif opcao == "2":
    # Solicita o nome do arquivo de saída TXT
    nome_arquivo_saida = input("Digite o nome do arquivo de saída TXT: ")
    
    # Salva os resultados em um arquivo TXT
    with open(nome_arquivo_saida, 'w') as arquivo_saida:
        for resultado in resultados:
            arquivo_saida.write(resultado + "\n")
        print(f"Os resultados foram salvos em {nome_arquivo_saida}.")
else:
    print("Programa encerrado.")
