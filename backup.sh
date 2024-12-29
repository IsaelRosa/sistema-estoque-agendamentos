#! /bin/bash

diretorio_backup="/home/isael/devops"
nome_arquivo="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
tar -czf "$nome_arquivo" "diretorio_backup"
echo "Backup concluido em $nome_arquivo"
