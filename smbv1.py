import subprocess

def smb_scan(ip, port):
    smbclient_cmd = f"smbclient -L \\\\{ip} -N -p {port} --option='client min protocol=NT1'"
    subprocess.run(smbclient_cmd, shell=True)

    print("\n\n===========================================================\n\n")

    resp = input("Deseja continuar a pesquisa? (1 = SIM, 2 = NÃO): ")

    if resp == "1":
        print("\n\nEscolha qual diretório quer ganhar o acesso:\n")
        file = input("Entre com o Diretório: ")

        print("\n\n_______________\n| Boa sorte!!!|\n---------------\n\n")

        smbclient_cmd = f"smbclient //{ip}/{file} -N -p {port} --option='client min protocol=NT1'"
        subprocess.run(smbclient_cmd, shell=True)

# Banner informativo
def print_banner():
    banner = """
---------------------------------------------
Script de Verificação SMB
---------------------------------------------
Este script realiza uma varredura SMB em um
determinado IP e porta fornecidos como entrada.
Ele exibe os resultados da varredura e oferece
a opção de acessar um diretório específico.
---------------------------------------------
Modo de uso: python smbv1.py
---------------------------------------------
"""
    print(banner)

# Solicitar IP e porta para teste
print_banner()
ip = input("Digite o IP: ")
port = input("Digite a porta: ")

smb_scan(ip, port)
