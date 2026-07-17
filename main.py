import flet as ft
from services import gerar_conteudo_ia, gerar_pagina_html_completa, publicar_no_github
from indexador import indexar_url

def main(page: ft.Page):
    page.title = "Dominador Google Local"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO

    def acao_gerar(e):
        if not input_regiao.value or not input_sintoma.value:
            resultado.value = "Preencha região e sintoma!"
            page.update()
            return

        resultado.value = "Gerando e salvando página..."
        page.update()

        try:
            conteudo = gerar_conteudo_ia(input_sintoma.value, input_regiao.value)
            caminho = gerar_pagina_html_completa(input_sintoma.value, input_regiao.value, conteudo)
            resultado.value = f"Sucesso! Arquivo gerado em: {caminho}"
        except Exception as ex:
            resultado.value = f"Falha na geração: {str(ex)}"
        page.update()

    def acao_publicar(e):
        if not resultado.value or "Sucesso! Arquivo gerado em:" not in resultado.value:
            resultado.value = "ERRO: Gere um arquivo antes de publicar!"
        else:
            caminho = resultado.value.split(": ")[1]
            resultado.value = "Publicando no GitHub..."
            page.update()
            resp = publicar_no_github(caminho)
            resultado.value = resp
        page.update()

    def acao_indexar(e):
        if not input_url.value:
            resultado.value = "ERRO: Digite a URL."
        else:
            resultado.value = "Indexando..."
            page.update()
            try:
                resp = indexar_url(input_url.value)
                resultado.value = f"Resposta do Google: {resp}"
            except Exception as ex:
                resultado.value = f"Falha: {str(ex)}"
        page.update()

    input_regiao = ft.TextField(label="Região (Cidade/Bairro)")
    input_sintoma = ft.TextField(label="Sintoma/Dor do dia")
    input_endereco = ft.TextField(label="Endereço Presencial (Opcional)")
    input_url = ft.TextField(label="URL para indexar")
    
    btn_gerar = ft.FilledButton("Gerar Conteúdo", on_click=acao_gerar)
    btn_publicar = ft.FilledButton("Publicar no GitHub", on_click=acao_publicar, style=ft.ButtonStyle(bgcolor="blue"))
    btn_indexar = ft.FilledButton("Indexar no Google", on_click=acao_indexar, style=ft.ButtonStyle(bgcolor="green"))
    resultado = ft.Text(selectable=True)

    page.add(
        ft.Text("Painel de Geração e Indexação", size=20, weight="bold"),
        input_regiao, input_sintoma, input_endereco, btn_gerar, btn_publicar,
        ft.Divider(),
        input_url, btn_indexar,
        ft.Divider(),
        resultado
    )

ft.app(main)