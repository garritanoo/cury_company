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

st.set_page_config(page_title='Visão Entregadores', page_icon='motorcycle', layout='wide')

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


def top_delivers(df1, top_asc=False):
    df_slow = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['Time_taken(min)', 'City'], ascending=top_asc).reset_index()

    df_metro = df_slow.loc[df_slow['City'] == 'Metropolitian', :].head(10) 
    df_urban = df_slow.loc[df_slow['City'] == 'Urban', :].head(10) 
    df_semi = df_slow.loc[df_slow['City'] == 'Semi-Urban', :].head(10) 

    df_top = pd.concat([df_metro, df_urban, df_semi]).reset_index(drop=True)
    
    return df_top


def metric_ratings_by_weather (df1):
    """ Recebe um dataframe e retorna a visualização do dataframe
    
        1. Seleciona as colunas
        2. Agrupa as colunas pelas condções climáticas
        3. Calcula a média e o desvio padrão
        4. Renomeia o nome das colunas
        5. Reseta o index
        6. Cria a visualização do dataframe
    
    """
    df_weather = ( df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                  .groupby('Weatherconditions')
                  .agg( {'Delivery_person_Ratings' : ['mean', 'std']} ) )
    df_weather.columns = ['delivery_mean', 'delivery_std']
    df_weather.reset_index()
    
    return df_weather
    
def metric_ratings_by_traffic(df1):
    """ Recebe um dataframe e retorna a visualização do dataframe
    
        1. Seleciona as colunas
        2. Agrupa as colunas pela densidade de tráfego
        3. Calcula a média e o desvio padrão
        4. Renomeia o nome das colunas
        5. Reseta o index
        6. Cria a visualização do dataframe
    
    """
    df_traffic = ( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings' : ['mean', 'std']}))
    df_traffic.columns = ['delivery_mean', 'delivery_std']
    df_traffic.reset_index()
    
    return df_traffic

# Careegando o dataset
df = pd.read_csv('dataset/train.csv')

# Limpando o dataset
df1 = clean_code(df)

# ========================
# SIDEBAR NO STREAMLIT
# ========================

st.header('Marketplace - Visão Entregadores')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('### Cury Company')
st.sidebar.text('Fastest Delivery in Town')

st.markdown('---')

st.sidebar.markdown('### Selecione a data limite')
data_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY')

traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

weather_options = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy', 'condtions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy', 'condtions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'])

st.sidebar.markdown('---')
st.sidebar.text('Powered by Comunidade DS')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de clima
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas, :]

# ========================
# LAYOUT NO STREAMLIT
# ========================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap='large')
        
        with col1:
            max_idade = df1.loc[:, "Delivery_person_Age"].max()
            col1.metric(label='Maior idade', value=max_idade, delta=None)
        with col2:
            min_idade = df1.loc[:, "Delivery_person_Age"].min()
            col2.metric(label='Menor idade', value=min_idade, delta=None)
            
        with col3:
            melhor_condicao = df1.loc[:, "Vehicle_condition"].max()
            col3.metric(label='Melhor veículo', value=melhor_condicao, delta=None)
            
        with col4:
            pior_condicao = df1.loc[:, "Vehicle_condition"].min()
            col4.metric(label='Pior veículo', value=pior_condicao, delta=None)
            
    with st.container():
        st.markdown('---')
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Avaliações médias')
            df_avaliacao_media_entregador = df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avaliacao_media_entregador)
            
        with col2:
            st.markdown('##### Avaliações médias por trânsito')
            by_traffic = metric_ratings_by_traffic(df1)
            st.dataframe(by_traffic)
                        
            st.markdown('##### Avaliações médias por clima')
            by_weather = metric_ratings_by_weather(df1)
            st.dataframe(by_weather)
            
    with st.container():
        st.markdown('---')
        st.title('Velocidade de entrega')
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            fast_delivers = top_delivers(df1, top_asc=True)      
            st.dataframe(fast_delivers)
            
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            slow_delivers = top_delivers(df1, top_asc=False)
            st.dataframe(slow_delivers)

with tab2:
    st.markdown('# Não há dados para visualização')
    
with tab3:
    st.markdown('# Não há dados para visualização')