#!/bin/bash

# Função para exibir o banner
exibir_banner() {
    echo "###############################################"
    echo "#              Script de Automação             #"
    echo "###############################################"
    echo
    echo "Este script automatiza a extração de IPs de um arquivo de dados de FTP usando o Shodan CLI."
    echo "Ele executa os seguintes comandos em sequência:"
    echo "1. shodan download --limit 10 ftp.json.gz ftp 'Anonymous access granted'"
    echo "2. shodan parse ftp.json.gz --fields ip_str > list-ftp.txt"
    echo "3. cat list-ftp.txt | cut -d ' ' -f 1 > anonftp.txt"
    echo
}

# Função para perguntar se deseja continuar
perguntar_continuar() {
    read -p "Deseja continuar a execução do script? (s/n): " resposta
    if [[ "$resposta" == "s" || "$resposta" == "S" ]]; then
        return 0  # Continuar
    else
        return 1  # Sair
    fi
}

# Exibir o banner
exibir_banner

# Perguntar se deseja continuar
if perguntar_continuar; then
    # Comando 1: shodan download
    echo "Executando comando: shodan download --limit 10 ftp.json.gz ftp 'Anonymous access granted'"
    shodan download --limit 10 ftp.json.gz ftp 'Anonymous access granted'
    sleep 1

    # Comando 2: shodan parse
    echo "Executando comando: shodan parse ftp.json.gz --fields ip_str > list-ftp.txt"
    shodan parse ftp.json.gz --fields ip_str > list-ftp.txt
    sleep 1

    # Comando 3: cat e cut
    echo "Executando comando: cat list-ftp.txt | cut -d ' ' -f 1 > anonftp.txt"
    cat list-ftp.txt | cut -d ' ' -f 1 > anonftp.txt

    echo "Extração de IPs concluída. Os IPs foram salvos no arquivo anonftp.txt."
else
    echo "Execução do script cancelada."
fi
