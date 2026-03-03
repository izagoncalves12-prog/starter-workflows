import os

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from google import genai # Mudança para a biblioteca nova



# 1. Configuração de Segurança

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMAIL_USER = os.getenv("EMAIL_USER")

EMAIL_PASS = os.getenv("EMAIL_PASS")

EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")



if not all([GEMINI_API_KEY, EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):

    print("Erro: Variáveis de ambiente faltando.")

    exit(1)



# Inicializando o cliente novo

client = genai.Client(api_key=GEMINI_API_KEY)



def run_agent():

    prompt = """

    Pesquise notícias das últimas 24 horas sobre 'Direitos Autorais e IA' em Inglês, Português e Espanhol.

    Organize por CONTINENTE e PAÍS.

    Inclua: Título em PT-BR, Resumo (3 frases) e Link da Fonte.

    Ignore blogs e foque em decisões judiciais ou novas leis.

    Finalize com 'Tendência Global do Dia'.

    """



    # Usando o modelo atualizado e a ferramenta de busca nova

    response = client.models.generate_content(

        model='gemini-1.5-flash', # Atualizado para a versão estável de 2026

        contents=prompt,

        config={'tools': [{'google_search': {}}]} 

    )

    return response.text



def send_email(content):

    if "Sem atualizações" in content:

        return



    msg = MIMEMultipart()

    msg['From'] = EMAIL_USER

    msg['To'] = EMAIL_RECEIVER

    msg['Subject'] = "Relatório Diário: Direitos Autorais & IA"

    msg.attach(MIMEText(content, 'plain'))



    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(msg)

        server.quit()

        print("Relatório enviado!")

    except Exception as e:

        print(f"Erro no e-mail: {e}")



if __name__ == "__main__":

    print("Iniciando pesquisa...")

    report = run_agent()

    send_email(report)
