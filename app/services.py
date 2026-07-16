import os
import json
from dotenv import load_dotenv
from groq import Groq
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Debug para garantir que este arquivo está sendo carregado
print("DEBUG: O arquivo services.py foi carregado com sucesso.")

# Carrega as configurações
load_dotenv(os.path.join(os.path.dirname(__file__), 'keys', '.env'))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Função de IA (Camaleão Geográfico)
def gerar_conteudo_ia(sintoma, cidade):
    # Instrução ajustada para retornar conteúdo estruturado
    prompt = f"""
    Crie uma landing page persuasiva para psicólogo sobre {sintoma} em {cidade}.
    Retorne a resposta EXATAMENTE no seguinte formato JSON, sem texto extra:
    {{
        "online": "Conteúdo persuasivo para atendimento online...",
        "local": "Conteúdo persuasivo para atendimento presencial em {cidade}..."
    }}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"}
    )
    
    # Converte o retorno em dicionário Python
    return json.loads(chat_completion.choices[0].message.content)

# Função para montar o HTML completo com o Script do Camaleão
def gerar_pagina_html_completa(conteudo_ia, cidade_alvo):
    online_txt = conteudo_ia.get("online", "")
    local_txt = conteudo_ia.get("local", "")
    
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atendimento Especializado em {cidade_alvo}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 20px auto; padding: 20px; }}
        .bloco {{ margin-bottom: 20px; padding: 15px; border-radius: 8px; }}
        #bloco-online {{ background: #f4f7f6; }}
        #bloco-local {{ background: #e8f4fd; display: none; border-left: 5px solid #2196F3; }}
    </style>
</head>
<body>
    <div id="bloco-online" class="bloco">
        {online_txt}
    </div>

    <div id="bloco-local" class="bloco">
        {local_txt}
    </div>

    <script>
        fetch('https://ip-api.com/json/')
            .then(response => response.json())
            .then(data => {{
                if (data.city === "{cidade_alvo}") {{
                    document.getElementById('bloco-local').style.display = 'block';
                }}
            }})
            .catch(e => console.log("Erro na geolocalização"));
    </script>
</body>
</html>
    """
    return html_template

# Função de indexação
def indexar_url(url_para_indexar):
    key_file = os.path.join(os.path.dirname(__file__), 'keys', 'credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/indexing']
    
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, SCOPES)
        service = build('indexing', 'v3', credentials=credentials)
        
        body = {
            'url': url_para_indexar,
            'type': 'URL_UPDATED'
        }
        
        request = service.urlNotifications().publish(body=body)
        response = request.execute()
        return str(response)
    except Exception as e:
        return f"Erro na indexação: {str(e)}"

import subprocess

def publicar_no_github(caminho_arquivo, mensagem_commit="Nova página gerada pelo Dominador"):
    """
    Realiza o deploy automático do arquivo gerado para o GitHub.
    """
    try:
        # Adiciona o arquivo específico ao Git
        subprocess.run(["git", "add", caminho_arquivo], check=True)
        # Faz o commit
        subprocess.run(["git", "commit", "-m", mensagem_commit], check=True)
        # Faz o push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return "Sucesso: Página publicada no GitHub!"
    except subprocess.CalledProcessError as e:
        return f"Erro no deploy: {str(e)}"        