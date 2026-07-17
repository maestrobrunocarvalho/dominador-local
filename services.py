import os
import json
from dotenv import load_dotenv
from groq import Groq
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import subprocess

# Carregamento robusto das configurações
caminho_env = os.path.join(os.path.dirname(__file__), 'keys', '.env')
if not os.path.exists(caminho_env):
    caminho_env = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(caminho_env)

api_key = os.getenv("GROQ_API_KEY")
print(f"DEBUG: Chave API carregada? {'SIM' if api_key else 'NÃO'}")
client = Groq(api_key=api_key)

# Função de IA (Camaleão Geográfico)
def gerar_conteudo_ia(sintoma, cidade):
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
    return json.loads(chat_completion.choices[0].message.content)

# Função atualizada: Gera o conteúdo, monta o HTML e SALVA O ARQUIVO automaticamente
def gerar_pagina_html_completa(sintoma, regiao, conteudo_ia):
    online_txt = conteudo_ia.get("online", "")
    local_txt = conteudo_ia.get("local", "")
    
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atendimento Especializado em {regiao}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 20px auto; padding: 20px; }}
        .bloco {{ margin-bottom: 20px; padding: 15px; border-radius: 8px; }}
        #bloco-online {{ background: #f4f7f6; }}
        #bloco-local {{ background: #e8f4fd; display: none; border-left: 5px solid #2196F3; }}
    </style>
</head>
<body>
    <div id="bloco-online" class="bloco">{online_txt}</div>
    <div id="bloco-local" class="bloco">{local_txt}</div>

    <script>
        fetch('https://ip-api.com/json/')
            .then(response => response.json())
            .then(data => {{
                if (data.city === "{regiao}") {{
                    document.getElementById('bloco-local').style.display = 'block';
                }}
            }})
            .catch(e => console.log("Erro na geolocalização"));
    </script>
</body>
</html>
    """
    
    os.makedirs("paginas_geradas", exist_ok=True)
    nome_arquivo = f"paginas_geradas/{sintoma.replace(' ', '_').lower()}_{regiao.replace(' ', '_').lower()}.html"
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    return nome_arquivo

# Função de indexação
def indexar_url(url_para_indexar):
    key_file = os.path.join(os.path.dirname(__file__), 'keys', 'credentials.json')
    SCOPES = ['https://www.googleapis.com/auth/indexing']
    
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, SCOPES)
        service = build('indexing', 'v3', credentials=credentials)
        body = {'url': url_para_indexar, 'type': 'URL_UPDATED'}
        request = service.urlNotifications().publish(body=body)
        return str(request.execute())
    except Exception as e:
        return f"Erro na indexação: {str(e)}"

# Função de deploy (Github)
def publicar_no_github(caminho_arquivo, mensagem_commit="Nova página gerada pelo Dominador"):
    try:
        subprocess.run(["git", "add", caminho_arquivo], check=True)
        subprocess.run(["git", "commit", "-m", mensagem_commit], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return "Sucesso: Página publicada no GitHub!"
    except Exception as e:
        return f"Erro no deploy: {str(e)}"