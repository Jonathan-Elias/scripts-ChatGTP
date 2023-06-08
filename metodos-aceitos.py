import requests
import json
import sys

def test_directory_methods(url):
    response = requests.options(url)
    methods = response.headers.get("Allow", "").split(", ")
    return methods

def test_directory_urls(urls):
    results = {}
    total_urls = len(urls)
    processed_urls = 0

    for url in urls:
        methods = test_directory_methods(url)
        results[url] = methods

        processed_urls += 1
        progress = processed_urls / total_urls * 100
        sys.stdout.write(f"\rProgresso: [{progress:.2f}%]")
        sys.stdout.flush()

    sys.stdout.write("\n")
    return results

def save_to_txt(results, filename):
    with open(filename, 'w') as f:
        for url, methods in results.items():
            f.write(f"{url}: {methods}\n")

def main():
    json_file = input("Digite o caminho do arquivo JSON com as URLs: ")
    output_file = input("Digite o nome do arquivo de saída (sem extensão): ")

    with open(json_file, 'r') as f:
        urls = json.load(f)

    results = test_directory_urls(urls)

    save_to_txt(results, f"{output_file}.txt")

    print(f"O resultado do teste foi salvo em {output_file}.txt")

    print("Resultados:")
    for url, methods in results.items():
        print(f"{url}: {methods}")

if __name__ == "__main__":
    main()
