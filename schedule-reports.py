import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# Carrega as chaves com segurança
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

client = genai.Client(api_key=GEMINI_API_KEY)

def run_agent():
    print("Iniciando pesquisa com Gemini 2.0 e chave nova...")
    prompt = "Resuma as 3 notícias mais importantes de hoje sobre Direitos Autorais e IA no mundo. Inclua links."
    
    # Usamos o 2.0 porque ele é o nativo da biblioteca google-genai em 2026
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt,
        config={'tools': [{'google_search': {}}]}
    )
    return response.text

def send_email(content):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Relatório Direitos Autorais & IA - AGORA VAI"
    msg.attach(MIMEText(content, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    report = run_agent()
    send_email(report)
    print("Sucesso! Verifique sua caixa de entrada.")
