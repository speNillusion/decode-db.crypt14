@echo off
setlocal

echo ===== Descriptografador de WhatsApp db.crypt14 =====
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erro: Python nao encontrado. Por favor, instale o Python 3.6 ou superior.
    echo Voce pode baixar o Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verifica se as dependências estão instaladas
echo Verificando dependencias...
pip show pycryptodome >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Instalando dependencias necessarias...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Erro ao instalar dependencias. Por favor, execute: pip install pycryptodome
        pause
        exit /b 1
    )
)

echo Dependencias verificadas com sucesso!
echo.

:: Solicita os caminhos dos arquivos
set /p arquivo_chave=Digite o caminho para o arquivo de chave (key): 
set /p arquivo_criptografado=Digite o caminho para o arquivo criptografado (msgstore.db.crypt14): 
set /p arquivo_saida=Digite o caminho para salvar o arquivo descriptografado (ex: msgstore.db): 

:: Verifica se os arquivos existem
if not exist "%arquivo_chave%" (
    echo Erro: O arquivo de chave nao foi encontrado.
    pause
    exit /b 1
)

if not exist "%arquivo_criptografado%" (
    echo Erro: O arquivo criptografado nao foi encontrado.
    pause
    exit /b 1
)

:: Executa o descriptografador
echo.
echo Iniciando processo de descriptografia...
echo.

python decriptografador.py "%arquivo_chave%" "%arquivo_criptografado%" "%arquivo_saida%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo Ocorreu um erro durante a descriptografia.
    echo Verifique se os arquivos estao corretos e tente novamente.
) else (
    echo.
    echo Processo concluido com sucesso!
    echo O arquivo descriptografado foi salvo em: %arquivo_saida%
)

pause