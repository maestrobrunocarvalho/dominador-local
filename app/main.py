import services
import os

def executar_dominador():
    print("--- Dominador Google Local: Iniciando Automação ---")
    
    # 1. Inputs do usuário
    sintoma = input("Qual a dor do paciente (ex: Ansiedade)? ")
    cidade = input("Qual a cidade alvo? ")
    
    print("... Gerando conteúdo com IA...")
    # 2. Gera conteúdo
    conteudo_ia = services.gerar_conteudo_ia(sintoma, cidade)
    
    # 3. Monta HTML
    print("... Montando página HTML...")
    html_template = services.gerar_pagina_html_completa(conteudo_ia, cidade)
    
    # 4. Salva o arquivo localmente
    diretorio = "app/paginas_geradas"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
    nome_arquivo = f"{sintoma.lower().replace(' ', '_')}_{cidade.lower().replace(' ', '_')}.html"
    caminho_completo = os.path.join(diretorio, nome_arquivo)
    
    with open(caminho_completo, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"Arquivo gerado em: {caminho_completo}")
    
    # 5. Publicação Automática
    print("... Publicando no GitHub...")
    resultado_deploy = services.publicar_no_github(caminho_completo, f"Adicionando página: {sintoma} em {cidade}")
    print(resultado_deploy)
    
    # 6. Indexação
    # Nota: substitua 'SEU_SITE' pela sua URL real do GitHub Pages
    url_publica = f"https://maestrobrunocarvalho.github.io/dominador-local/{nome_arquivo}"
    print(f"... Solicitando indexação para: {url_publica} ...")
    status_index = services.indexar_url(url_publica)
    print(status_index)

    print("--- Missão Cumprida! Página no ar e Google notificado. ---")

if __name__ == "__main__":
    executar_dominador()