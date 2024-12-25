import streamlit as st
import qrcode
import io
import phonenumbers

# Código para mover o texto para o rodapé
footer = """
<style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
    }
    /* Garantindo que o rodapé fique no topo de outros elementos */
    .main > div {
        padding-bottom: 150px; /* ajuste conforme necessário */
    }

    /* Estilização do botão flutuante do WhatsApp */
    .whatsapp-button {
        position: fixed;
        bottom: 80px;
        right: 20px;
        background-color: #25D366;
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        transition: transform 0.3s;
        text-decoration: none;
        border: none;
    }

    .whatsapp-button:hover {
        transform: scale(1.1);
    }

    .whatsapp-icon {
        font-size: 36px;
        color: white;
    }
</style>

<div class="footer">
    Desenvolvido por: 🛡️ <a href="https://www.panavarro.com.br" target="_blank">Panavarro</a> | 📩 <a href="mailto:thiago@panavarro.com.br">Suporte</a>
</div>
<a href="https://wa.me/5516993253920" target="_blank" class="whatsapp-button">
    <i class="fab fa-whatsapp whatsapp-icon"></i>
</a>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
"""

st.set_page_config(
    page_title="Panavarro - QRCODE",
    page_icon="🫒",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'http://www.panavarro.com',
        'Report a bug': "http://www.panavarro.com",
        'About': "# Geração de QRCODE por Telefone, Site, Localização."
    }
)

def generate_qr_code(data, size=(3000, 3000), fill_color='black', back_color='white'):
    # Gerar QR code com tamanho e cores especificadas
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color=fill_color, back_color=back_color).resize(size)
    return image

def format_phone_number(phone_number):
    """Formata o número de telefone para o padrão (XX) XXXXX-XXXX"""
    if len(phone_number) == 11:  # Formato: 11999999999
        return f"({phone_number[:2]}) {phone_number[2:7]}-{phone_number[7:]}"
    elif len(phone_number) == 10:  # Formato: 1199999999
        return f"({phone_number[:2]}) {phone_number[2:6]}-{phone_number[6:]}"
    return phone_number  # Retorna sem formatação se não corresponder

def main():
    st.title("Gerador de QR Code")

    # Criação de colunas para o layout
    col1, col2 = st.columns(2)

    # Utilização de um único botão de rádio para seleção exclusiva
    with st.container():
        selected_option = col1.radio(
            "Selecione uma opção:",
            ("Telefone", "Site"),
            key="radio_opcao"
        )

    # Inicializa as variáveis de entrada
    phone_number = None
    website = None
    localizacao = None
    data = None  # Inicializa a variável data

    if selected_option == "Telefone":
        phone_number_input = col1.text_input('Digite seu número de telefone (ex: +5511999999999):', key="input_telefone")
        formatted_phone_number = format_phone_number(phone_number_input)
        if formatted_phone_number:
            try:
                parsed_number = phonenumbers.parse(formatted_phone_number, None)
                if phonenumbers.is_valid_number(parsed_number):
                    data = "https://api.whatsapp.com/send?phone=" + phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)[1:]
                else:
                    st.error("Número de telefone inválido.")
            except phonenumbers.NumberParseException:
                st.error("Formato de número de telefone inválido.")

    elif selected_option == "Site":
        website = col1.text_input('Digite o site:', key="input_site")
        if website:
            data = website

    elif selected_option == "Localização":
        localizacao = col1.text_input('Digite a localização:', key="input_localizacao")
        if localizacao:
            data = localizacao

    # Adicionando seleção de cores
    fill_color = col1.color_picker("Escolha a cor do QR Code", "#000000")  # Cor de preenchimento

    if col1.button("Gerar QR Code"):
        if selected_option != "Nenhuma" and data:  # Verifica se uma opção foi selecionada e dados inseridos
            # Geração do QR Code
            qr_image = generate_qr_code(data, fill_color=fill_color)

            # Converter a imagem para bytes
            buf = io.BytesIO()
            qr_image.save(buf, format='PNG')
            byte_im = buf.getvalue()
            st.session_state.byte_im = byte_im  # Armazena a imagem gerada no session_state
        else:
            st.warning("Por favor, selecione uma opção e insira os dados para gerar o QR Code.")

    # Exibir a imagem do QR Code na segunda coluna
    with col2:
        if 'byte_im' in st.session_state:
            st.image(st.session_state.byte_im, caption='QR Code gerado', use_container_width=True)


    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()