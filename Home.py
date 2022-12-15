import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon='chart_with_upwards_trend'
)

image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('---')

st.markdown('# Cury Company Growth Dashboard')

st.markdown(
"""
Growth Dashboard foi construido para acompanhar o crescimento dos entregadores e restaurantes.
### Como utilizar esse Growth Dashboard?
- Visão Empresa:
    - Visão Gerencial: Métricas gerais de comportamento.
    - Visão Tática: Indicadores semanais de crescimento.
    - Visão Geográfica: Insights de geolocalização.
- Visão Entregador:
    - Acompanhamentos dos indicadores semanais de crescimento
- Visão Restaurante:
    - Indicadores semanais de crescimentos dos restaurantes
    
    ### Ask for help
    - Time de Data Science no Discord: @juarez
""" )