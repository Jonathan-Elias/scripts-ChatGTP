import requests
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()

def directory_scan(url, wordlist):
    result = []
    with open(wordlist, 'r', encoding='latin-1') as f:
        paths = f.read().splitlines()

    total_paths = len(paths)
    processed_paths = 0

    def scan_path(path):
        nonlocal result

        target_url = f"{url}{path}"  # Modifica a URL para incluir o caminho do diretório
        response = session.get(target_url)

        if response.status_code == 200:
            result.append(target_url)

        if response.status_code == 200 and os.path.isdir(path):  # Verifica se o caminho é um diretório e executa a atividade principal
            sub_result = directory_scan(target_url + "/", wordlist)  # Chamada recursiva para as subpastas
            result.extend(sub_result)  # Adiciona os resultados das subpastas ao resultado principal

            sub_paths = [os.path.join(path, sub_path) for sub_path in os.listdir(path)]
            sub_result = directory_scan(url, wordlist, sub_paths)  # Chamada recursiva para o brute force das subpastas
            result.extend(sub_result)  # Adiciona os resultados do brute force das subpastas ao resultado principal

        sys.stdout.write("\033[F")  # Move o cursor para a linha anterior
        sys.stdout.write("\033[K")  # Limpa a linha atual

        nonlocal processed_paths
        processed_paths += 1
        progress = processed_paths / total_paths * 100
        sys.stdout.write(f"\rProgresso: [{progress:.2f}%]")
        sys.stdout.flush()

    with ThreadPoolExecutor() as executor:
        executor.map(scan_path, paths)

    sys.stdout.write("\n")
    return result

def save_to_json(result, filename):
    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)

def main():
    url = input("Digite a URL ou o IP do site a ser testado: ")
    wordlist = input("Digite o caminho da wordlist: ")
    output_file = input("Digite o nome do arquivo de saída (sem extensão): ")

    result = directory_scan(url, wordlist)
    save_to_json(result, f"{output_file}.json")

    print(f"\nO resultado do teste foi salvo em {output_file}.json")
    print("Resultados com código de retorno 200:")
    for res in result:
        print(res)

if __name__ == "__main__":
    main()
