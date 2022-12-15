# ========================
# IMPORTS (LIBRARIES)
# ========================

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
import folium
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Restaurantes', page_icon='pizza', layout='wide')

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

def distance(df1, fig):
    """ Recebe um dataframe e gera a visualização do dataframe em uma tabela
    
        Processo: 
        1. Seleciona as colunas
        2. Cria a coluna 'distance'
        3. Seleciona os dados que vão compor essa nova coluna criada
        4. Calcula a média da distancia das entregas até o local de destino
        5. Retorna o calculo da média em todas as linhas da coluna 'distance'
    
    """
    
    if fig == False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude'] 
        df1['distance'] = ( df1.loc[:, cols].apply(lambda x:
                                                    haversine( (x['Delivery_location_latitude'], x['Delivery_location_longitude']),
                                                               (x['Restaurant_latitude'], x['Restaurant_longitude'])), axis=1 ) )
        avg_distance = np.round(df1['distance'].mean(),2)
        
        return avg_distance
    
    else:
        
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude'] 

        df1['distance'] = (df1.loc[:, cols].apply(lambda x : 
                                              haversine( (x['Delivery_location_latitude'], x['Delivery_location_longitude']),
                                                         (x['Restaurant_latitude'], x['Restaurant_longitude']) ), axis=1 ))
        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
        
        return fig

def avg_std_time_delivery(df1, festival, op):
    """ Esta função calcula o tempo médio e o desvio padrçao do tempo de entrega

        Parâmetros:
            Input:
            - df: Dataframe com os dados necessários para cálculo
            - op: Tipo de operação que precisa ser calculado
                'avg_time': Calcula o tempo médio
                'std_time': Calcula o desvio padrão do tempo
            Outpu:
                - df: Dataframe com 2 colunas e 1 linha

    """

    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)':['mean', 'std']}))
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op] ,2)

    return df_aux

def avg_std_time_graph(df1):
    df_aux = df1.loc[:, ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(name='Control', x=df_aux['City'], y=df_aux['avg_time'],
                         error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig

def avg_std_time_traffic(df1):
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg( {'Time_taken(min)' : ['mean', 'std']} )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                     color='std_time', color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(df_aux['std_time']))

    return fig
  

df = pd.read_csv('dataset/train.csv')

df1 = clean_code(df)

# ========================
# SIDEBAR NO STREAMLIT
# ========================

st.header('Marketplace - Visão Restaurantes')

image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('### Cury Company')
st.sidebar.text('Fastest Delivery in Town')

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
        
        col1, col2, col3, col4, col5, col6 = st.columns(6, gap='large')
        
        with col1:
            delivery_unique = df1.loc[:, 'Delivery_person_ID'].nunique()
            col1.metric(label='Entregadores Únicos', value=delivery_unique)
            
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric(label='Distância Média', value=avg_distance)            
            
            
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric(label='Tempo Médio de Entrega', value=df_aux)         
            
            
        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes','std_time')
            col4.metric(label='Desvio Padrão de Entrega', value=df_aux)
            
            
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric(label='Tempo Médio de Entrega', value=df_aux)
            
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric(label='Desvio Padrão de Entrega', value=df_aux)
            
    with st.container():
        
        col1, col2 = st.columns(2)
        st.markdown('---')
        
        with col1:
            col1.markdown('##### Distribuição do tempo por cidade')
            fig = avg_std_time_graph(df1)
            col1.plotly_chart(fig, use_container_width=True)
            
        with col2:
            col2.markdown('##### Distribuição da distância')
            df_aux = (df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                      .groupby(['City', 'Type_of_order'])
                      .agg( {'Time_taken(min)' : ['mean', 'std']} ))

            df_aux.columns = ['avg_time', 'avg_std']
            df_aux.reset_index()
            col2.dataframe(df_aux)
        
            
    with st.container():
        
        col1, col2 = st.columns(2, gap='small')
        
        with col1:
            col1.markdown('##### Tempo médio de entrega por cidade')
            fig = distance(df1, fig=True)
            col1.plotly_chart(fig, use_container_width=True)
           
        with col2:
            col2.markdown('##### Tempo médio por tipo de entrega (Sunsuburst)')
            fig = avg_std_time_traffic(df1)
            col2.plotly_chart(fig, use_container_width=True)             
            
