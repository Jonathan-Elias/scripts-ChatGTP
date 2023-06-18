import subprocess
import ipaddress
import json
import sys
import os
import concurrent.futures

def smb_scan(ip):
    smbclient_cmd = f"smbclient -L \\\\{ip} -N -p 445 --option='client min protocol=NT1'"
    result = subprocess.run(smbclient_cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def save_results(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def load_results(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def print_results(results):
    print("\nResultados da varredura SMB na rede:")
    print("-----------------------------------")
    for ip, result in results.items():
        print(f"\nIP: {ip}\n{result}")

def smb_scan_network(network, filename):
    ips = list(ipaddress.IPv4Network(network))
    results = {}
    progress = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ip in ips:
            ip_str = str(ip)
            futures.append(executor.submit(smb_scan, ip_str))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            ip = ips[progress]
            ip_str = str(ip)
            if "Disk" in result:
                results[ip_str] = "Resultado da varredura SMB no IP: " + ip_str
            progress += 1
            sys.stdout.write(f"\rVarredura em andamento: {progress}/{len(ips)} IPs concluídos")
            sys.stdout.flush()

    save_results(results, filename)
    print_results(results)
    print("\nVarredura SMB na rede concluída.")

def smb_access_share(ip, filename):
    results = load_results(filename)
    if ip not in results:
        print(f"\nO IP {ip} não possui compartilhamentos SMB.")
        return

    share_info = results[ip]
    print(f"\nCompartilhamentos encontrados no IP {ip}:")
    print("-----------------------------------")
    for share in share_info["Disk"]:
        print(share["Disk"])

    while True:
        folder_name = input("\nDigite o nome da pasta compartilhada desejada (ou 'voltar' para selecionar outro IP): ")
        if folder_name.lower() == "voltar":
            return
        elif folder_name in [share["Disk"] for share in share_info["Disk"]]:
            smbclient_cmd = f"smbclient \\\\{ip}\\{folder_name} -N -p 445 --option='client min protocol=NT1'"
            result = subprocess.run(smbclient_cmd, shell=True, capture_output=True, text=True)
            print("\nResultado do acesso ao compartilhamento:")
            print("-----------------------------------")
            print(result.stdout)
            if "session setup failed" in result.stdout:
                option = input("\nO acesso foi recusado. Deseja tentar uma nova pasta compartilhada? (s/n): ")
                if option.lower() == "n":
                    return
            else:
                break
        else:
            print("\nNome de pasta inválido. Por favor, digite novamente")

def print_banner():
    banner = """---------------------------------------------
Script de Verificação SMB
---------------------------------------------
Este script realiza uma varredura SMB em uma rede fornecida como entrada.
Ele exibe os resultados da varredura e oferece a opção de acessar um diretório específico.

Modo de uso:

- Para varredura em uma rede:
  python teste.py REDE

Exemplo de varredura em rede:
  python teste.py 192.168.0.0/24
---------------------------------------------"""
    print(banner)

# Verificar se a entrada é uma rede ou um único IP
def is_network(target):
    try:
        ipaddress.IPv4Network(target)
        return True
    except ValueError:
        return False

# Verificar se o nome do arquivo é um IP ou uma rede
def is_invalid_filename(filename):
    try:
        ipaddress.IPv4Address(filename)
        return True
    except ipaddress.AddressValueError:
        pass

    try:
        ipaddress.IPv4Network(filename)
        return True
    except ValueError:
        pass

    return False

# Solicitar IP ou rede para teste
print_banner()
target = input("Digite o IP ou rede a ser testada: ")
filename = input("Digite o nome do arquivo para salvar os resultados: ")

if is_network(target):
    smb_scan_network(target, filename + ".json")
else:
    smb_access_share(target, filename + ".json")
