import ftplib
from tqdm import tqdm  # biblioteca para exibir barra de progresso

# endereço e credenciais do FTP
host = 'ftp.exemplo.com'
username = 'anonymous'
password = 'anonymous'

# Exibe o banner explicativo
print('''
===============================================
         Teste de Conexão FTP - Script
===============================================

Este script permite testar a conexão FTP utilizando
uma lista de endereços IP. Ele verifica se é possível
fazer login em cada servidor FTP usando credenciais
pré-definidas.

Modo de Uso:
1. Certifique-se de ter uma wordlist com os endereços
   IP dos servidores FTP a serem testados.
2. Execute o script e insira o nome do arquivo que
   contém a lista de endereços IP quando solicitado.
3. Aguarde enquanto o script testa a conexão FTP com
   cada IP da lista.
4. O script exibirá uma mensagem indicando se as
   credenciais foram válidas ou inválidas para cada IP.

Certifique-se de ter as seguintes informações preenchidas
no script:
- host: o endereço do servidor FTP a ser testado.
- username: o nome de usuário para o login FTP.
- password: a senha para o login FTP.

===============================================
''')

# nome do arquivo que contém a lista de endereços IP
filename = input("Insira o nome do arquivo que contém a lista de endereços IP: ")

# abre o arquivo e lê os endereços IP
with open(filename) as file:
    ips = file.readlines()

# exibe a barra de progresso
for ip in tqdm(ips, desc='Testando conexão FTP', unit='ip'):
    ip = ip.strip()  # remove caracteres de quebra de linha

    try:
        # cria uma conexão com o servidor FTP
        ftp = ftplib.FTP(ip)

        # tenta fazer login com o nome de usuário e senha especificados
        ftp.login(username, password)

        # fecha a conexão com o servidor FTP
        ftp.quit()

        # exibe uma mensagem de sucesso
        tqdm.write(f'Credenciais válidas para: {ip}')

    except ftplib.all_errors:
        # exibe uma mensagem de erro
        tqdm.write(f'Credenciais inválidas para: {ip}')
