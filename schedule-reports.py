import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# Configurações de Segurança
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

client = genai.Client(api_key=GEMINI_API_KEY)

def run_agent():
    print("Teste de Sanidade: Rodando SEM busca no Google...")
    prompt = "Escreva uma mensagem curta de incentivo para a Iza, coordenadora do ITS Rio, que está quase dominando a automação de IA!"
    
    # Rodando puramente o modelo, sem ferramentas extras
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    return response.text

def send_email(content):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Teste de Sanidade: O Robô está Vivo?"
    msg.attach(MIMEText(content, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    try:
        report = run_agent()
        send_email(report)
        print("CONSEGUIMOS! Verifique seu e-mail agora.")
    except Exception as e:
        print(f"O erro persiste: {e}")
