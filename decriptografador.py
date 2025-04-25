#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Descriptografador para arquivos db.crypt14 do WhatsApp
Baseado no projeto wa-crypt-tools (https://github.com/ElDavoo/wa-crypt-tools)

Este script requer o arquivo de chave (key) para descriptografar o arquivo db.crypt14.
O arquivo de chave normalmente está localizado em /data/data/com.whatsapp/files/key
em dispositivos Android com acesso root.
"""

import argparse
import os
import sys
import zlib
from io import DEFAULT_BUFFER_SIZE

try:
    from Crypto.Cipher import AES
except ImportError:
    print("Erro: A biblioteca pycryptodome não está instalada.")
    print("Instale-a usando: pip install pycryptodome")
    sys.exit(1)

# Cabeçalho fixo do arquivo de chave (27 bytes)
KEY_HEADER = b'\xac\xed\x00\x05\x75\x72\x00\x02\x5b\x42\xac\xf3\x17\xf8' \
            b'\x06\x08\x54\xe0\x02\x00\x00\x78\x70\x00\x00\x00\x83'

# Offsets conhecidos para arquivos crypt14
WHATSAPP_SALT_OFFSET = 15
WHATSAPP_IV_OFFSET = 67
WHATSAPP_DATA_OFFSET = 191

def oscilate(n, min_val, max_val):
    """
    Gera uma sequência de números oscilando em torno de n,
    útil para procurar offsets quando não temos certeza do valor exato.
    """
    yield n
    for i in range(1, max(n - min_val, max_val - n) + 1):
        if n - i >= min_val:
            yield n - i
        if n + i <= max_val:
            yield n + i

def encontrar_offset_dados(header, iv_offset, chave):
    """
    Tenta encontrar o offset onde os dados criptografados começam
    testando diferentes posições.
    """
    iv = header[iv_offset:iv_offset + 16]
    cipher = AES.new(chave, AES.MODE_GCM, iv)
    
    # Testa diferentes offsets possíveis
    for offset in range(180, 200):
        try:
            # Tenta descriptografar e descomprimir um pequeno trecho
            # Se funcionar, encontramos o offset correto
            dados_teste = header[offset:offset + 100]
            dados_descriptografados = cipher.decrypt(dados_teste)
            zlib.decompress(dados_descriptografados)
            return offset
        except (zlib.error, ValueError):
            # Ignora erros, significa que testamos um offset incorreto
            continue
    return -1

def carregar_chave(caminho_chave):
    """
    Carrega e valida o arquivo de chave.
    """
    if not os.path.isfile(caminho_chave):
        print(f"Erro: Arquivo de chave '{caminho_chave}' não encontrado.")
        sys.exit(1)
        
    with open(caminho_chave, 'rb') as arquivo_chave:
        conteudo = arquivo_chave.read()
        
    # Verifica se o arquivo tem o cabeçalho correto
    if not conteudo.startswith(KEY_HEADER):
        print("Aviso: O arquivo de chave não tem o cabeçalho esperado.")
        print("Isso pode indicar que o arquivo não é uma chave válida do WhatsApp.")
        
    # A chave real está nos últimos 32 bytes do arquivo
    chave = conteudo[-32:]
    if len(chave) != 32:
        print("Erro: A chave extraída não tem o tamanho esperado (32 bytes).")
        sys.exit(1)
        
    return chave

def descriptografar_crypt14(caminho_chave, caminho_crypt14, caminho_saida, forcar=False):
    """
    Descriptografa um arquivo db.crypt14 usando a chave fornecida.
    """
    print("Carregando arquivo de chave...")
    chave = carregar_chave(caminho_chave)
    
    print("Abrindo arquivo criptografado...")
    try:
        arquivo_crypt14 = open(caminho_crypt14, 'rb')
    except FileNotFoundError:
        print(f"Erro: Arquivo criptografado '{caminho_crypt14}' não encontrado.")
        sys.exit(1)
    
    # Lê o cabeçalho para análise
    cabecalho = arquivo_crypt14.read(512)
    if len(cabecalho) < 512:
        print("Erro: O arquivo criptografado é muito pequeno.")
        sys.exit(1)
    
    # Determina os offsets
    iv_offset = WHATSAPP_IV_OFFSET
    data_offset = WHATSAPP_DATA_OFFSET
    
    if not forcar:
        # Tenta encontrar o offset correto dos dados
        offset_encontrado = encontrar_offset_dados(cabecalho, iv_offset, chave)
        if offset_encontrado != -1:
            data_offset = offset_encontrado
            print(f"Offset de dados encontrado: {data_offset}")
    
    # Extrai o vetor de inicialização (IV)
    iv = cabecalho[iv_offset:iv_offset + 16]
    print("Iniciando descriptografia...")
    
    # Configura o cipher AES-GCM com a chave e IV
    cipher = AES.new(chave, AES.MODE_GCM, iv)
    
    # Posiciona o arquivo no início dos dados criptografados
    arquivo_crypt14.seek(data_offset)
    
    # Cria o arquivo de saída
    try:
        arquivo_saida = open(caminho_saida, 'wb')
    except Exception as e:
        print(f"Erro ao criar arquivo de saída: {e}")
        arquivo_crypt14.close()
        sys.exit(1)
    
    # Descriptografa e descomprime os dados em blocos
    try:
        descompressor = zlib.decompressobj()
        while True:
            bloco = arquivo_crypt14.read(DEFAULT_BUFFER_SIZE)
            if not bloco:
                break
            # Descriptografa o bloco e o descomprime
            bloco_descriptografado = cipher.decrypt(bloco)
            arquivo_saida.write(descompressor.decompress(bloco_descriptografado))
        
        # Escreve quaisquer dados restantes do descompressor
        arquivo_saida.write(descompressor.flush())
        
    except Exception as e:
        print(f"Erro durante a descriptografia: {e}")
        if not forcar:
            print("Tente novamente com a opção --forcar para ignorar verificações de segurança.")
        arquivo_crypt14.close()
        arquivo_saida.close()
        sys.exit(1)
    
    # Fecha os arquivos
    arquivo_crypt14.close()
    arquivo_saida.close()
    
    print(f"Descriptografia concluída com sucesso! Arquivo salvo em: {caminho_saida}")
    print("O arquivo de saída é um banco de dados SQLite que pode ser aberto com ferramentas apropriadas.")

def main():
    parser = argparse.ArgumentParser(description="Descriptografa arquivos db.crypt14 do WhatsApp")
    parser.add_argument("arquivo_chave", help="O arquivo de chave do WhatsApp (normalmente chamado 'key')")
    parser.add_argument("arquivo_criptografado", help="O arquivo db.crypt14 criptografado")
    parser.add_argument("arquivo_saida", help="O caminho para salvar o arquivo descriptografado")
    parser.add_argument("-f", "--forcar", action="store_true", help="Ignorar verificações de segurança")
    
    args = parser.parse_args()
    
    descriptografar_crypt14(args.arquivo_chave, args.arquivo_criptografado, args.arquivo_saida, args.forcar)

if __name__ == "__main__":
    main()