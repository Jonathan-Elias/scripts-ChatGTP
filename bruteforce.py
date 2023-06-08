import requests
import json
import sys

def directory_scan(url, wordlist):
    result = []
    with open(wordlist, 'r') as f:
        paths = f.read().splitlines()

    total_paths = len(paths)
    processed_paths = 0

    for path in paths:
        target_url = f"{url}/{path}"
        response = requests.get(target_url)
        sys.stdout.write(f"\rTestando: {target_url}")
        sys.stdout.flush()

        if response.status_code == 200:
            result.append(target_url)

        processed_paths += 1
        progress = processed_paths / total_paths * 100
        sys.stdout.write(f"\r\nProgresso: [{progress:.2f}%]")  # Adiciona uma linha em branco antes de exibir o progresso
        sys.stdout.flush()

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

    print(f"O resultado do teste foi salvo em {output_file}.json")
    print("Resultados com código de retorno 200:")
    for res in result:
        print(res)

if __name__ == "__main__":
    main()
