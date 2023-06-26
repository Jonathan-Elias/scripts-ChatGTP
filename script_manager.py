import subprocess

scripts = {
    1: {
        'name': 'Brute Force WEB',
        'command': ['python', 'bruteforceweb.py']
    },
    2: {
        'name': 'Métodos aceitos',
        'command': ['python', 'metodos-aceitos.py']
    },
    3: {
        'name': 'Compartilhamento SMBv1',
        'command': ['python', 'smbv1.py']
    },
    4: {
        'name': 'Compartilhamento SMBv1 Rede',
        'command': ['python', 'smbv1rede.py']
    },
    5: {
        'name': 'Brute force sub pastas (OBS: Depende do script N 1 para executar!)',
        'command': ['python', 'BruteForceWebDir.py']
    },
    6: {
        'name': 'Fazer Parse dos FTPs no Shodan',
        'command': ['bash', 'shodan_ftp_automation.sh']
    },
    7: {
        'name': 'Testar as conexões FTPs (OBS: Depende do script N 6 para executar!)',
        'command': ['python', 'ftp-anon.py']
    },
    # Adicione mais scripts conforme necessário
}

def execute_script(script):
    subprocess.run(script['command'])

print("")
def print_scripts():
    print("Selecione o script a ser executado:")
    for num, script in scripts.items():
        print(f"{num}. {script['name']}")

def print_banner():
    banner = """
======================================================
Bem-vindo ao Script Manager!
Este script permite executar scripts de forma interativa.
Selecione um número correspondente ao script desejado.
Digite 0 para sair do programa.
======================================================
"""
    print(banner)

def main():
    print_banner()
    while True:
        print_scripts()
        selected = int(input("Número do script: "))
        if selected == 0:
            break
        script = scripts.get(selected)
        if script:
            execute_script(script)
        else:
            print("Script inválido.")
        
        print("")
        response = input("Deseja executar outro script? (s/n): ")
        if response.lower() != 's':
            break

if __name__ == "__main__":
    main()
