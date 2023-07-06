# ========================
# IMPORTS (LIBRARIES)
# ========================

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import folium
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

st.set_page_config(page_title='Visão Empresa', page_icon='factory', layout='wide')

# ========================
# FUNÇÕES
# ========================

def clean_code(df1):
    """Está função tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. remocação dos dados NA
        2. Mudança do tipo da coluna de dados
        3. Remocação dos espaços em branco das variáveis de texto
        4. Formatação da coluna de data
        5. Limpeza da coluna de tempo (min)
        
        Input: Dataframe
        Output: Dataframe
    
    """
# 1. REMOVENDO NaN E CONVERTENDO TIPO DE DADOS
    # coluna Delivery_person_Age
    linhas_vazias = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype('int64')

    # coluna Delivery_person_Ratings
    linhas_vazias = df1['Delivery_person_Ratings'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype('float64')

    # coluna multiple_deliveries
    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype('int64')

    # coluna Road_traffic_density 
    linhas_vazias  = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()

    # coluna Festival 
    linhas_vazias = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()

    # coluna City 
    linhas_vazias = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()

    # 2. CONVERTENDO STRING > DATETIME
    linhas_vazias = df1['Order_Date'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 3. REMOVENDO ESPAÇOS SOBRESALENTE NAS COLUNAS DO DATASET
    df1['ID'] = df1['ID'].str.strip()
    df1['Delivery_person_ID'] = df1['Delivery_person_ID'].str.strip()
    df1['City'] = df1['City'].str.strip()
    df1['Festival'] = df1['Festival'].str.strip()
    df1['Type_of_vehicle'] = df1['Type_of_vehicle'].str.strip()
    df1['Type_of_order'] = df1['Type_of_order'].str.strip()
    df1['Road_traffic_density'] = df1['Road_traffic_density'].str.strip()
    df1['Weatherconditions'] = df1['Weatherconditions'].str.strip()

    # 4. REMOVENDO TEXTOS DA COLUNA Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min) ' )[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

def order_metric(df1):
    """ Recebe um dataframe, executa um dataframe, gera um gráfico e faz a visualização do gráfico
    
        Processo:
        1. Seleciona as colunas
        2. Agrupa as colunas de acordo com a data do pedido
        3. Plota o gráfico
        4. Retorna a visualização do gráfico
    """
    
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x='Order_Date', y='ID')

    return fig       

def traffic_order_share(df1):
    """ Recebe um dataframe, executa um dataframe, gera um gráfico e retorna a visualização do gráfico
        
        Processo:
        1. Seleciona as colunas
        2. Agrupa as colunas de acordo com a data do pedido
        3. Calcula o percentual das entregas
        3. Plota o gráfico
        4. Retorna a visualização do gráfico
    """
    
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['delivery_percentual'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values='delivery_percentual', names='Road_traffic_density')

    return fig

def traffic_order_city(df1):
    """ Recebe um dataframe, executa o dataframe, gera um gráfico e retorna a visualização do gráfico
    
        Processo:
        1. Seleciona as colunas
        2. Agrupa as colunas de acordo com a cidade e a densidade de tráfego
        3. Faz a contagem dos dados
        4. Plota o gráfico
        5. Retorna a visualização do gráfico
    """
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def order_by_week(df1):
    """ Recebe um dataframe, executa o dataframe, gera um gráfico e retorna a visualização do gráfico
    
        Processo:
        1. Cria a coluna com a semana do ano
        2. Agrupa as colunas de acordo com o a semana do ano
        3. Faz a contagem dos dados
        4. Plota o gráfico
        5. Retorna a visualização do gráfico
    
    """
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:, ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig

def order_share_by_week(df1):
    """ Recebe um dataframe, executa o dataframe, gera um gráfico e retorna a visualização do gráfico
    
        Processo:
        df_aux_01:
        1. Seleciona as colunas
        2. Agrupa as colunas de acordo com o a semana do ano
        3. Faz a contagem dos dados
        4. Mescla os dataframes
        5. Cria a coluna com o percentual de entregas feitas por cada entregador
        6. Plota o gráfico
        7. Retorna a visualização do gráfico
    
    """
    df_aux01 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    df_aux = pd.merge(df_aux01, df_aux02, how='inner')
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    fig = px.line(df_aux, x='week_of_year', y='order_by_delivery')

    return fig
        
def country_maps(df1):
    """ Recebe um dataframe, executa o dataframe e gera a visualização do mapa com as entregas
    
        1. Seleciona as colunas
        2. Agrupa as colunas de acordo com o cidade e densidade de tráfego
        3. Seleciona as 20 primeiras ocorrências
        4. Gera o mapa
        5. Percorre cada localização que foram feitas as entregas
        6. Gera a visualização do mapa      
    
    """
    cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()
    df_aux = df_aux.head(20)
    mapa = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [ location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude'] ],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to(mapa)

    folium_static(mapa, width=960, height=600)

    return None
# ------------------------------------- INICIO DA ESTRUTURA LÓGICA ---------------------------------------------

# Carregando os dados
df = pd.read_csv('dataset/train.csv')

# Limpando os dados
df1 = clean_code(df)

# ========================
# SIDEBAR NO STREAMLIT
# ========================

st.header('Marketplace - Visão Empresa')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('### Cury Company')
st.sidebar.text('Fastest Delivery in Town')

st.markdown('---')

st.sidebar.markdown('### Selecione a data limite')
data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY')

traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown('---')
st.sidebar.text('Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ========================
# LAYOUT NO STREAMLIT
# ========================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        # Order metric
        st.markdown('## Orders by Day')
        fig = order_metric(df1)
        st.plotly_chart(fig, use_container_width=True)    
    
    with st.container():
        col1, col2 = st.columns(2)
    
        with col1:
            st.markdown('## Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('## Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
                        
with tab2:
    with st.container():
        st.markdown('## Order by Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)  
        
            
    with st.container():
        st.markdown('## Order Share by Week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
            

with tab3:
    with st.container():
        st.markdown('## Country Maps')
        country_maps(df1)
            



