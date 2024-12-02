import requests
import json
import sys
import datetime
import subprocess

# Função para obter a hora atual formatada
def obter_hora_atual():
    return datetime.datetime.now()

# Função para validar os argumentos fornecidos ao script
def validar_argumentos():
    if len(sys.argv) < 4:
        print("Uso: python nome_do_programa.py <arquivo_python.py> <arquivo_c.c> <entradas>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2], sys.argv[3]

# Função para ler o conteúdo de um arquivo
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado. {obter_hora_atual()}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e} {obter_hora_atual()}")
        sys.exit(1)

# Função para enviar dados à API
def enviar_para_api(prompt, api_key, id_modelo):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body_mensagem = {"model": id_modelo, "messages": [{"role": "user", "content": prompt}]}
    try:
        resposta = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body_mensagem)
        return resposta.json()
    except requests.RequestException as e:
        print(f"Erro na requisição à API: {e} {obter_hora_atual()}")
        sys.exit(1)

# Função para salvar o conteúdo em um arquivo
def salvar_arquivo(nome_arquivo, conteudo):
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
        print(f"Arquivo salvo em: {nome_arquivo} {obter_hora_atual()}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e} {obter_hora_atual()}")
        sys.exit(1)

# Função para executar um arquivo Python
def executar_arquivo_python(nome_arquivo, entradas):
    try:
        print(f"Executando arquivo Python: {nome_arquivo} {obter_hora_atual()}")
        resultado = subprocess.run(
            ["python", nome_arquivo],
            input=entradas,
            text=True,
            capture_output=True,
            check=True
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o arquivo Python: {e} {obter_hora_atual()}")
        return None

# Função para compilar e executar um arquivo em C
def executar_arquivo_c(nome_arquivo, entradas):
    try:
        executavel = nome_arquivo.replace(".c", "_exec1")
        subprocess.run(["gcc", nome_arquivo, "-o", executavel, "-lm"], check=True)
        resultado = subprocess.run(
            [f"./{executavel}"],
            input=entradas,
            text=True,
            capture_output=True,
            check=True
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao compilar ou executar o arquivo C: {e} {obter_hora_atual()}")
        return None

# Função para comparar os resultados das execuções
def comparar_resultados(resultado_python, resultado_c):
    print(f"Comparando os resultados... {obter_hora_atual()}")
    if resultado_python == resultado_c:
        print("Os resultados são iguais.")
    else:
        print("Os resultados são diferentes.")
        print(f"Resultado do Python: {resultado_python}")
        print(f"Resultado do C: {resultado_c}")

# Ponto de entrada do script
if __name__ == "__main__":
    print(f"Iniciando o processo... {obter_hora_atual()}")

    # Validação e leitura dos parâmetros
    arquivo_python, arquivo_c, entradas = validar_argumentos()
    conteudo_python = ler_arquivo(arquivo_python)

    # Criação do prompt para a API
    prompt = f"Por favor, traduza o seguinte código em Python para C. Apenas o código-fonte puro.\n\n{conteudo_python}"
    API_KEY = "123456"
    ID_MODELO = "gpt-3.5-turbo"
    resposta_api = enviar_para_api(prompt, API_KEY, ID_MODELO)

    # Processamento da resposta e salvamento
    conteudo_resposta = resposta_api['choices'][0]['message']['content']
    conteudo_resposta = "#include <math.h>\n\n" + conteudo_resposta
    salvar_arquivo(arquivo_c, conteudo_resposta)

    # Execução e comparação dos resultados
    resultado_python = executar_arquivo_python(arquivo_python, entradas)
    resultado_c = executar_arquivo_c(arquivo_c, entradas)

    if resultado_python and resultado_c:
        comparar_resultados(resultado_python, resultado_c)

    print(f"Processo finalizado. {obter_hora_atual()}")
