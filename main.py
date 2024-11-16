import requests
import json
import sys
import datetime

hora_atual = datetime.datetime.now()
print(f"Iniciando o processo... {hora_atual} ")

if len(sys.argv) > 1:
    parametro1 = sys.argv[1]
    parametro2 = sys.argv[2] if len(sys.argv) > 2 else None  # Opcional segundo parâmetro
else:
    print("Nenhum parâmetro foi passado.")

#nome_arquivo = "exemplo.py"
nome_arquivo = parametro1
arquivo_destino = parametro2

print(f"Arquivo de origem: {nome_arquivo} {hora_atual} ")
print(f"Arquivo de destino: {arquivo_destino} {hora_atual} ")

try:
    # Abrindo o arquivo no modo de leitura
     with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        # Lendo o conteúdo do arquivo
        conteudo = arquivo.read()
        # Imprimindo o conteúdo do arquivo
        #print(conteudo)
except FileNotFoundError:
    print(f"O arquivo '{nome_arquivo}' não foi encontrado na pasta atual.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")

prompt = f"Você poderia reescrever o seguinte código Python em linguagem C, mostrando como resultado somente o código fonte?\n\n{conteudo}"

API_KEY = "123456"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo"

body_mensagem = {
    "model": id_modelo,
    "messages": [{"role": "user", "content": prompt}]
}

print(f"Enviado dados a IA... {hora_atual} ")

requisicao = requests.post(link, headers=headers, json=body_mensagem)
resposta = requisicao.json()
print(f"Resposta recebida... {hora_atual} ")

conteudo_resposta = resposta['choices'][0]['message']['content']


with open(arquivo_destino, "w") as arquivo:
    print(f"Salvando arquivo... {hora_atual} ")
    arquivo.write(conteudo_resposta)

print(f"Processo finalizado. {hora_atual} ")