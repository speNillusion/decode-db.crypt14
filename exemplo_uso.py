#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de uso do descriptografador para arquivos db.crypt14 do WhatsApp

Este script demonstra como usar o descriptografador.py para descriptografar
um arquivo de backup do WhatsApp no formato db.crypt14.
"""

import os
import sys
from decriptografador import descriptografar_crypt14

def main():
    print("===== Exemplo de Uso do Descriptografador de WhatsApp db.crypt14 =====")
    print("\nEste script demonstra como usar o descriptografador.py em seu código.")
    
    # Verifica se os arquivos necessários existem
    arquivo_chave = input("\nDigite o caminho para o arquivo de chave (key): ")
    if not os.path.isfile(arquivo_chave):
        print(f"Erro: O arquivo de chave '{arquivo_chave}' não foi encontrado.")
        return
    
    arquivo_criptografado = input("Digite o caminho para o arquivo criptografado (msgstore.db.crypt14): ")
    if not os.path.isfile(arquivo_criptografado):
        print(f"Erro: O arquivo criptografado '{arquivo_criptografado}' não foi encontrado.")
        return
    
    arquivo_saida = input("Digite o caminho para salvar o arquivo descriptografado (ex: msgstore.db): ")
    
    # Confirma a operação
    print("\nResumo da operação:")
    print(f"Arquivo de chave: {arquivo_chave}")
    print(f"Arquivo criptografado: {arquivo_criptografado}")
    print(f"Arquivo de saída: {arquivo_saida}")
    
    confirmacao = input("\nDeseja prosseguir com a descriptografia? (s/n): ")
    if confirmacao.lower() != 's':
        print("Operação cancelada pelo usuário.")
        return
    
    # Executa a descriptografia
    try:
        print("\nIniciando processo de descriptografia...")
        descriptografar_crypt14(arquivo_chave, arquivo_criptografado, arquivo_saida)
        print("\nProcesso concluído com sucesso!")
        print(f"O arquivo descriptografado foi salvo em: {arquivo_saida}")
    except Exception as e:
        print(f"\nErro durante a descriptografia: {e}")
        print("Verifique se os arquivos estão corretos e tente novamente.")

if __name__ == "__main__":
    main()