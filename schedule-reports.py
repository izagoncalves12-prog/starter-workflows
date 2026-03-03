def run_agent():
    print("Teste de Sanidade: Sem busca no Google...")
    prompt = "Escreva uma mensagem de incentivo para uma coordenadora de educação chamada Iza que está aprendendo automação."
    
    # Rodando SEM a ferramenta de busca (tools)
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
        # Tiramos a linha da 'google_search' aqui
    )
    return response.text
