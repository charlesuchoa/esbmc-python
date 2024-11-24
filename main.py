import requests
import json
import sys
import datetime
import subprocess

hora_atual = datetime.datetime.now()
print(f"Iniciando o processo... {hora_atual} ")

if len(sys.argv) > 1:
    if len(sys.argv) < 4:
        print("Uso: python nome_do_progama.py <arquivo_python.py> <arquivo_c.c> <entradas> {hora_atual}")
        sys.exit(1)

    parametro1 = sys.argv[1]
    parametro2 = sys.argv[2] if len(sys.argv) > 2 else "saida.txt"  # Define arquivo de saída padrão
    parametro3 = sys.argv[3]

else:
    hora_atual = datetime.datetime.now()
    print("Erro: Nenhum parâmetro foi passado. {hora_atual}")
    sys.exit(1)  # Encerra o programa


nome_arquivo = parametro1
arquivo_destino = parametro2
arquivo_python = parametro1
arquivo_c = parametro2
entradas = parametro3

hora_atual = datetime.datetime.now()
print(f"Arquivo de origem: {nome_arquivo} {hora_atual} ")
print(f"Arquivo de destino: {arquivo_destino} {hora_atual} ")
print(f"Parametros: {entradas} {hora_atual} ")

try:
    # Abrindo o arquivo no modo de leitura
     with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        # Lendo o conteúdo do arquivo
        conteudo = arquivo.read()
        # Imprimindo o conteúdo do arquivo
        #print(conteudo)
except FileNotFoundError:
    hora_atual = datetime.datetime.now()
    print(f"O arquivo '{nome_arquivo}' não foi encontrado na pasta atual.  {hora_atual} ")
except Exception as e:
    hora_atual = datetime.datetime.now()
    print(f"Ocorreu um erro ao ler o arquivo: {e}  {hora_atual} ")

prompt = f"Por favor, traduza o seguinte código em Python para C. Na resposta, quero apenas o código-fonte puro em C, sem comentários, explicações, marcadores ou outros elementos. Apenas o código-fonte puro\n\n{conteudo}"

API_KEY = "123456"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

body_mensagem = {
    "model": id_modelo,
    "messages": [{"role": "user", "content": prompt}]
}

hora_atual = datetime.datetime.now()
print(f"Enviado dados a IA... {hora_atual} ")

requisicao = requests.post(link, headers=headers, json=body_mensagem)
resposta = requisicao.json()
hora_atual = datetime.datetime.now()
print(f"Resposta recebida... {hora_atual} ")

conteudo_resposta = resposta['choices'][0]['message']['content']
classe_math = "#include <math.h>"
conteudo_resposta = classe_math + "\n\n" + conteudo_resposta

with open(arquivo_destino, "w") as arquivo:
    hora_atual = datetime.datetime.now()
    print(f"Salvando arquivo... {hora_atual} ")
    arquivo.write(conteudo_resposta)

hora_atual = datetime.datetime.now()
print(f"Processo finalizado. {hora_atual} ")
print(f"Verificando arquivos gerados... {hora_atual} ")
print(f"Comparando arquivos... {hora_atual} ")

def executar_arquivo_python(nome_arquivo, entradas):
    try:
        hora_atual = datetime.datetime.now()
        print(f"Executando arquivo Python {nome_arquivo}  {hora_atual} ")
        resultado = subprocess.run(
            ["python", nome_arquivo],
            input=entradas,
            text=True,
            capture_output=True,
            check=True
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        hora_atual = datetime.datetime.now()
        print(f"Erro ao executar o arquivo Python: {e}  {hora_atual} ")
        print(f"Saída padrão (stdout): {e.stdout}  {hora_atual} ")
        print(f"Saída de erro (stderr): {e.stderr}  {hora_atual} ")
        return None

def executar_arquivo_c(nome_arquivo, entradas):
    try:
        # Compilar o arquivo C com o flag -lm
        hora_atual = datetime.datetime.now()
        print(f"Executando arquivo em C {nome_arquivo}  {hora_atual} ")
        executavel = nome_arquivo.replace(".c", "_exec1")
        subprocess.run(
            ["gcc", nome_arquivo, "-o", executavel, "-lm"], check=True
        )
        # Executar o arquivo compilado com entradas simuladas
        resultado = subprocess.run(
            [f"./{executavel}"],
            input=entradas,
            text=True,
            capture_output=True,
            check=True
        )
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        hora_atual = datetime.datetime.now()
        print(f"Erro ao compilar ou executar o arquivo C: {e}  {hora_atual} ")
        print(f"Saída de erro (stderr): {e.stderr.decode('utf-8')}  {hora_atual} ")
        return None

def comparar_resultados(resultado_python, resultado_c):
    hora_atual = datetime.datetime.now()
    print(f"Comparando os resultados...  {hora_atual} ")
    if resultado_python == resultado_c:
        hora_atual = datetime.datetime.now()
        print("Os resultados são iguais.  {hora_atual} ")
    else:
        hora_atual = datetime.datetime.now()
        print(f"Os resultados são diferentes.  {hora_atual} ")
        print(f"Resultado do Python: {resultado_python}  {hora_atual} ")
        print(f"Resultado do C: {resultado_c}  {hora_atual} ")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        hora_atual = datetime.datetime.now()
        print(f"Uso: python programa_python.py <arquivo_python.py> <arquivo_c.c> <entradas>  {hora_atual} ")
        sys.exit(1)

    arquivo_python = sys.argv[1]
    arquivo_c = sys.argv[2]
    entradas = sys.argv[3]  # Entradas fornecidas como argumento único

    hora_atual = datetime.datetime.now()
    print(f"Executando o arquivo Python...  {hora_atual} ")
    resultado_python = executar_arquivo_python(arquivo_python, entradas)

    hora_atual = datetime.datetime.now()
    print(f"Executando o arquivo C...  {hora_atual} ")
    resultado_c = executar_arquivo_c(arquivo_c, entradas)

    if resultado_python is not None and resultado_c is not None:
        comparar_resultados(resultado_python, resultado_c)

hora_atual = datetime.datetime.now()

print(f"Processo finalizado.  {hora_atual} ")
