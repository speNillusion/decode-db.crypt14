# Descriptografador para arquivos db.crypt14 do WhatsApp

Esta ferramenta permite descriptografar arquivos de backup do WhatsApp no formato `db.crypt14`, que são utilizados pelo WhatsApp para armazenar mensagens criptografadas em dispositivos Android.

## Requisitos

- Python 3.6 ou superior
- Biblioteca pycryptodome

## Instalação

1. Certifique-se de ter o Python instalado em seu sistema
2. Instale a biblioteca necessária:

```
pip install pycryptodome
```

## Como usar

### Pré-requisitos importantes

Para descriptografar um arquivo `db.crypt14`, você **precisa** do arquivo de chave correspondente. Este arquivo normalmente é chamado de `key` e está localizado em `/data/data/com.whatsapp/files/key` em dispositivos Android com acesso root.

Sem o arquivo de chave, é impossível descriptografar o backup, pois o WhatsApp utiliza criptografia forte para proteger seus dados.

### Uso básico

```
python decriptografador.py arquivo_chave arquivo_criptografado arquivo_saida
```

Exemplo:

```
python decriptografador.py key msgstore.db.crypt14 msgstore.db
```

### Opções

- `-f` ou `--forcar`: Ignora verificações de segurança e tenta descriptografar mesmo se houver problemas

## Resultado

O arquivo de saída será um banco de dados SQLite que pode ser aberto com ferramentas como:

- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [WhatsApp Viewer](https://github.com/andreas-mausch/whatsapp-viewer)

## Limitações

- Esta ferramenta funciona apenas com arquivos no formato `db.crypt14`
- É necessário ter o arquivo de chave correspondente ao backup
- Não é possível descriptografar backups sem a chave correta