from gpt4all import GPT4All
import sys
import datetime

hora_atual = datetime.datetime.now()
print(f"Iniciando o processo... {hora_atual} ")
# Verifica os argumentos de linha de comando
if len(sys.argv) > 1:
    parametro1 = sys.argv[1]
    parametro2 = sys.argv[2] if len(sys.argv) > 2 else "saida.txt"  # Define arquivo de saída padrão
else:
    print("Erro: Nenhum parâmetro foi passado.")
    sys.exit(1)  # Encerra o programa

nome_arquivo = parametro1
arquivo_destino = parametro2

print(f"Arquivo de origem: {nome_arquivo} {hora_atual} ")
print(f"Arquivo de destino: {arquivo_destino} {hora_atual} ")

try:
    # Abre o arquivo para leitura
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    sys.exit(1)

# Cria o prompt para a IA
prompt1 = f"Could you rewrite the following Python code in C language, showing only the source code as the result?\n\n{conteudo}"

# Função para enviar mensagens ao modelo e obter a resposta
def send_message(model, prompt):
    output = model.generate(prompt, max_tokens=500)  # Ajuste o número de tokens conforme necessário
    return output

# Inicializa o modelo GPT4All
print(f"Enviado dados a IA... {hora_atual} ")
try:
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", device="cpu")  # Certifique-se de que o nome do modelo está correto
except Exception as e:
    print(f"Erro ao inicializar o modelo: {e}")
    sys.exit(1)

# Gera a resposta da IA
try:
    conteudo_resposta = send_message(model, prompt1)
except Exception as e:
    print(f"Erro ao gerar a resposta: {e}")
    sys.exit(1)

# Salva a resposta no arquivo de saída
try:
    print(f"Resposta recebida... {hora_atual} ")
    with open(arquivo_destino, "w", encoding="utf-8") as arquivo:
        print(f"Salvando arquivo de destino: {hora_atual} ")
        arquivo.write(conteudo_resposta)
    print(f"Resposta salva em '{arquivo_destino}'.")
except Exception as e:
    print(f"Erro ao salvar a resposta: {e}")

print(f"Processo finalizado. {hora_atual} ")