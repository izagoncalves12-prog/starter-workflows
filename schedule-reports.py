import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai

# 1. Configurações de Segurança (Lidas dos Secrets do GitHub)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Inicializa o cliente oficial do Google
client = genai.Client(api_key=GEMINI_API_KEY)

def run_agent():
    print("Iniciando pesquisa global com Google Search...")
    
    prompt = """
    Pesquise notícias das últimas 24 horas sobre 'Direitos Autorais e Inteligência Artificial'.
    Busque fontes em Inglês, Português e Espanhol.
    Organize o relatório por CONTINENTE e PAÍS.
    Para cada notícia inclua: Título em PT-BR, um resumo de 3 frases e o link da fonte oficial.
    Foque em decisões judiciais, novas leis e acordos entre empresas de mídia e Big Techs.
    Finalize com uma seção chamada 'Tendência do Dia'.
    """

    # Chamada do modelo com a ferramenta de busca ativada
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt,
        config={'tools': [{'google_search': {}}]} 
    )
    
    return response.text

def send_email(content):
    print("Preparando para enviar e-mail...")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = "Relatório Diário: IA e Direitos Autorais"
    
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("Relatório enviado com sucesso para a sua caixa de entrada!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

if __name__ == "__main__":
    try:
        # Executa o agente de notícias
        report = run_agent()
        
        # Se o relatório foi gerado, envia o e-mail
        if report:
            send_email(report)
        else:
            print("O robô não encontrou notícias novas hoje.")
            
    except Exception as e:
        # Se der erro de cota (429), o log vai mostrar aqui
        print(f"Ocorreu um erro na execução: {e}")
