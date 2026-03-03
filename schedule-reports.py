import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# 1. Configuração de Segurança (Lendo dos Secrets do GitHub)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Validação simples para garantir que as chaves existem
if not all([GEMINI_API_KEY, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
    print("Erro: Uma ou mais variáveis de ambiente não foram configuradas nos Secrets.")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def run_agent():
    # 2. Configura o modelo com a ferramenta de busca do Google
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{'google_search_retrieval': {}}]
    )

    prompt = """
    Você é um Analista de Inteligência Jurídica especializado em Propriedade Intelectual. 
    Sua tarefa é pesquisar as notícias mais relevantes das últimas 24 horas sobre 'Direitos Autorais e IA'.
    
    Diretrizes de Pesquisa:
    - Idiomas: Pesquise em Inglês, Português e Espanhol para uma cobertura global.
    - Foco: Decisões de tribunais, novos processos judiciais, projetos de lei (ex: PL 2338 no Brasil, AI Act na UE) e acordos de licenciamento.
    - Qualidade: Ignore posts de blogs de opinião. Priorize fontes oficiais e portais de notícias jurídicas/tecnológicas.

    Estrutura do Relatório (Markdown):
    Agrupe obrigatoriamente por CONTINENTE e depois por PAÍS.
    Para cada notícia:
    - [Título em PT-BR]
    - Resumo Executivo: O que aconteceu e qual a implicação legal (máximo 3 frases).
    - Fonte: [Link direto para a notícia].

    Se não houver atualizações relevantes no dia, responda: 'Sem atualizações críticas hoje.'
    Finalize com uma seção chamada 'Tendência Global do Dia'.
    """

    response = model.generate_content(prompt)
    return response.text

def send_email(content):
    if "Sem atualizações críticas" in content:
        print("Nenhuma notícia relevante encontrada. E-mail não enviado.")
        return

    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Relatório Diário: Direitos Autorais & Inteligência Artificial"

    msg.attach(MIMEText(content, 'plain'))

    try:
        # Configuração do servidor SMTP do Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("Relatório enviado com sucesso por e-mail!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    print("Iniciando pesquisa do agente...")
    report_content = run_agent()
    print("Pesquisa concluída. Enviando e-mail...")
    send_email(report_content)
