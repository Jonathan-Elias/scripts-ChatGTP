import ftplib
from tqdm import tqdm  # biblioteca para exibir barra de progresso

# endereço e credenciais do FTP
host = 'ftp.exemplo.com'
username = 'anonymous'
password = 'anonymous'

# nome do arquivo que contém a lista de endereços IP
filename = 'ips.txt'

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
        
        #Como gerar wordlist com ip's do FTP
        #inserir API do shodan: shodan init API_KEY
        #shodan download --limit 1000 ftp.json.gz ftp "Anonymous access granted"
        #shodan parse ftp.json.gz > list-ftp.txt
        #cat list-ftp.txt |cut -d " " -f 1
