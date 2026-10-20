##Chatbot
import os
from pathlib import Path
import streamlit as st
from openai import OpenAI
import base64


st.set_page_config(page_title="ChatBot com IA", page_icon="💬", layout="centered")

caminho_fundo = Path(__file__).resolve().parent / "Banner1.jpg"

if caminho_fundo.exists():

    with open(caminho_fundo, "rb") as imagem:
        imagem_base64 = base64.b64encode(imagem.read()).decode()

    st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{imagem_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;}}

        [data-testid="stHeader"] {{
            background: transparent;}}
        </style>""", unsafe_allow_html=True)

# CONFIGURAÇÃO DA API GEMINI
PASTA_PROJETO = Path(__file__).resolve().parent

chave_api = os.getenv("GEMINI_API_KEY", "").strip()

if not chave_api:
    try:
        chave_api = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        chave_api = ""

# Leitura alternativa do secrets.toml
if not chave_api:
    arquivo_secrets = (PASTA_PROJETO / ".streamlit" / "secrets.toml")

    if arquivo_secrets.exists():
        try:
            import tomllib

            with open(arquivo_secrets, "rb") as arquivo:
                configuracoes = tomllib.load(arquivo)

            chave_api = str(configuracoes.get("GEMINI_API_KEY", "")).strip()

        except Exception:
            chave_api = ""

# INICIALIZAÇÃO DA SESSÃO
if "cadastro_concluido" not in st.session_state:
    st.session_state.cadastro_concluido = False

if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = ""

if "foto_usuario" not in st.session_state:
    st.session_state.foto_usuario = None

if "lista_mensagens" not in st.session_state:
    st.session_state.lista_mensagens = []

# CONEXÃO COM A INTELIGÊNCIA ARTIFICIAL
def responder_ia(mensagens):

    if not chave_api:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada. " "Verifique o arquivo .streamlit/secrets.toml.")

    cliente = OpenAI(
        api_key=chave_api,
        base_url=(
            "https://generativelanguage.googleapis.com/"
            "v1beta/openai/"), timeout=60.0, max_retries=1)

    resposta = cliente.chat.completions.create(
        model="gemini-3.5-flash-lite",
        messages=mensagens)

    return (
        resposta.choices[0].message.content
        or "Não foi possível gerar uma resposta.")

# TERMOS DE USO DO CHATBOT
@st.dialog("📄 Termos de Uso e Privacidade")
def visualizar_termos():

    st.markdown("""
    ### 1. Apresentação do projeto

    O ChatBot com IA é uma aplicação desenvolvida
    como projeto acadêmico, com finalidade exclusivamente
    educacional e demonstrativa.

    O projeto tem como objetivo aplicar conhecimentos
    de programação, desenvolvimento de interfaces
    e integração com inteligência artificial.

    ### 2. Tecnologias utilizadas

    A aplicação foi desenvolvida utilizando:

    - Python: linguagem principal de programação.
    - Streamlit: desenvolvimento da interface web.
    - Google Gemini: inteligência artificial responsável
      pela geração das respostas.
    - Biblioteca OpenAI: utilizada para realizar a
      comunicação com a API compatível do Google Gemini.

    O projeto é independente e não representa um
    produto oficial do Google ou da OpenAI.

    ### 3. Funcionamento da inteligência artificial

    As mensagens enviadas pelo usuário são encaminhadas
    à API do Google Gemini para processamento e
    geração de respostas.

    As respostas são produzidas automaticamente e
    podem apresentar informações incorretas,
    incompletas ou desatualizadas.

    ### 4. Privacidade e dados pessoais

    O sistema solicita informações de cadastro,
    como nome, data de nascimento, CPF e foto de perfil.

    Na versão atual, o nome e a foto são utilizados
    para personalizar a experiência do usuário.
    As mensagens são mantidas no estado da sessão
    do Streamlit durante a utilização da aplicação.

    O histórico de mensagens é enviado à API Gemini
    para manter o contexto da conversa.

    O tratamento das informações encaminhadas à API
    também está sujeito às políticas do Google.

    Recomenda-se não compartilhar senhas, dados
    bancários ou outras informações sensíveis.

    ### 5. Responsabilidade pelo uso

    O chatbot é destinado a estudos e demonstrações.
    Suas respostas não substituem orientações
    médicas, jurídicas, financeiras ou profissionais.

    ### 6. Finalidade acadêmica

    Este sistema foi criado para demonstrar a
    aplicação prática de conhecimentos em Python,
    interfaces web e inteligência artificial.

    O projeto poderá receber melhorias e novas
    funcionalidades durante seu desenvolvimento.

    ### 7. Aceitação dos termos

    Ao aceitar os presentes termos, o usuário
    declara estar ciente da finalidade acadêmica
    da aplicação, do funcionamento da inteligência
    artificial e das limitações do sistema.""")

    if st.button("Fechar", use_container_width=True):
        st.rerun()


# TELA 1: CADASTRO
if not st.session_state.cadastro_concluido:
    st.title("💬 ChatBot com IA")
    st.write("Bem-vindo!")
    st.write("Antes de começar, informe seus dados " "e escolha uma foto para seu perfil.")

    with st.form("formulario_cadastro"):
        nome = st.text_input("Seu nome:", placeholder="Digite seu nome")
        data = st.text_input( "Data de Nascimento:", placeholder="09/09/1997")
        documento = st.text_input("CPF:", placeholder="000.000.000-00")

        foto = st.file_uploader("Sua foto de perfil", type=["png", "jpg", "jpeg"])

        aceitou_termos = st.checkbox("Li e concordo com os Termos de Uso " "e a Política de Privacidade.")
        confirmar = st.form_submit_button("Entrar no bate-papo 💬", use_container_width=True)

# BOTÃO INDEPENDENTE DOS CAMPOS DE CADASTRO
    if st.button("📄 Visualizar Termos de Uso", use_container_width=True):
        visualizar_termos()

# VALIDAÇÃO DO CADASTRO
    if confirmar:
        if not nome.strip():
            st.warning("Digite seu nome para continuar.")

        elif foto is None:
            st.warning("Selecione uma foto para continuar.")

        elif not aceitou_termos:
            st.warning("Você precisa aceitar os Termos de Uso " "para continuar.")

        else:
            st.session_state.nome_usuario = nome.strip()
            st.session_state.foto_usuario = foto.getvalue()
            st.session_state.cadastro_concluido = True
            st.session_state.lista_mensagens = []

            st.rerun()

# TELA 2: BATE-PAPO
else:
    nome = st.session_state.nome_usuario
    foto = st.session_state.foto_usuario

    col_foto, col_info = st.columns(
        [1, 5],
        vertical_alignment="center")

    with col_foto:
        st.image(foto, width=72)

    with col_info:
        st.title("ChatBot com IA")
        st.caption(f"Conversando como {nome}")

    if st.button("Trocar usuário"):

        st.session_state.cadastro_concluido = False
        st.session_state.nome_usuario = ""
        st.session_state.foto_usuario = None
        st.session_state.lista_mensagens = []

        st.rerun()

    st.divider()

    if not chave_api:
        st.warning(
            "A chave da API não foi encontrada. "
            "Configure GEMINI_API_KEY para ativar a IA.")

    # EXIBIR HISTÓRICO DE MENSAGENS

    for mensagem in st.session_state.lista_mensagens:

        if mensagem["role"] == "user":

            with st.chat_message("user", avatar=foto):
                st.markdown(f"**{nome}**")
                st.write(mensagem["content"])

        else:

            with st.chat_message("assistant", avatar="🤖"):
                st.write(mensagem["content"])


    # CAMPO PARA ENVIAR MENSAGENS

    mensagem_usuario = st.chat_input(
        "Escreva sua mensagem aqui")

    if mensagem_usuario:

        with st.chat_message("user", avatar=foto):

            st.markdown(f"**{nome}**")
            st.write(mensagem_usuario)

        nova_mensagem = {"role": "user", "content": mensagem_usuario}

        st.session_state.lista_mensagens.append(nova_mensagem)

        if not chave_api:

            st.error(
                "Não foi possível conectar à IA. "
                "Verifique sua chave GEMINI_API_KEY.")

        else:

            try:

                with st.spinner("A IA está respondendo..."):

                    resposta_ia = responder_ia(
                        st.session_state.lista_mensagens)

                with st.chat_message(
                    "assistant",
                    avatar="🤖"):
                    st.write(resposta_ia)

                st.session_state.lista_mensagens.append({
                    "role": "assistant",
                    "content": resposta_ia})

            except Exception as erro:

                erro_texto = str(erro)

                if "429" in erro_texto:

                    st.warning(
                        "⏳ O limite de utilização da API "
                        "foi atingido. Aguarde e tente novamente.")

                elif "503" in erro_texto:

                    st.warning(
                        "⚠️ O serviço Gemini está "
                        "temporariamente indisponível.")

                elif "401" in erro_texto or "403" in erro_texto:

                    st.error(
                        "❌ A chave da API foi rejeitada "
                        "ou não possui permissão para "
                        "utilizar o modelo.")

                elif "404" in erro_texto:

                    st.error(
                        "❌ O modelo de IA não foi encontrado "
                        "ou não está disponível para sua chave.")

                else:

                    st.error(
                        "❌ Não foi possível obter uma "
                        "resposta da inteligência artificial.")

                    with st.expander(
                        "Ver detalhes técnicos do erro"):
                        st.code(erro_texto)

                # Remove a mensagem que falhou do histórico
                # enviado à API, evitando duplicação.
                st.session_state.lista_mensagens.pop()
