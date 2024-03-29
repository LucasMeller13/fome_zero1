# Importing libraries
import folium
import pandas as pd
import streamlit as st
from folium import Icon, IFrame, Popup
from folium.plugins import MarkerCluster
from PIL import Image
import inflection
from streamlit_folium import folium_static
import plotly.express as px

# Importing dataset and declaring variables
df_raw = pd.DataFrame(pd.read_csv('./dataset/zomato.csv'))

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"}

currency_code = {'Botswana Pula(P)':0.078,
                'Brazilian Real(R$)':0.2,
                'Dollar($)':1,
                'Emirati Diram(AED)':0.27,
                'Indian Rupees(Rs.)':0.012,
                'Indonesian Rupiah(IDR)':0.000067,
                'NewZealand($)':0.64,
                'Pounds(£)':1.23,
                'Qatari Rial(QR)':0.27,
                'Rand(R)':0.057,
                'Sri Lankan Rupee(LKR)':0.0027,
                'Turkish Lira(TL)':0.053}

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred"}

# Cleaning dataset and functions

def clean_dataset(dataframe):
    dataframe['Currency_usd'] = (dataframe[['Average Cost for two','Currency']]
                                 .apply(lambda a: usd_currencies(a['Average Cost for two'],
                                a['Currency']), axis=1))
    
    dataframe = dataframe[dataframe['Restaurant ID'] != 16608070]
    dataframe['color'] = dataframe['Rating color'].apply(lambda x: color_name(x))
    dataframe['country'] = dataframe['Country Code'].apply(lambda x: country_name(x))
    dataframe['price_tye'] = dataframe['Price range'].apply(lambda x: create_price_tye(x))
    dataframe = dataframe.dropna(axis=0)
    dataframe["Cuisines"] = dataframe.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])
    dataframe = rename_columns(dataframe)

    return dataframe


def country_name(country_id):
    return COUNTRIES[country_id]


def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    

def usd_currencies(number, code):
    return number*currency_code[code]


def color_name(color_code):
    return COLORS[color_code]


def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


def fig_country_name():
    df_country_name = df.groupby('country')[['restaurant_name']].nunique().reset_index().sort_values('restaurant_name',ascending=False)
    fig1 = px.bar(df_country_name,
                x='country',
                y='restaurant_name',
                color='country',
                text='restaurant_name',
                labels={'country': 'Países', 'restaurant_name': 'Quantidade de Restaurantes'},
                title='Quantidade de Restaurantes Registrados por País')
    fig1.update_layout(showlegend=False)   
    fig1.update_traces(hovertemplate='<b>País:</b> %{x}<br><b>Quantidade de restaurantes:</b> %{y}<extra></extra>') 
    
    return fig1


def fig_country_city():
    df_country_city = df.groupby('country')[['city']].nunique().reset_index().sort_values('city',ascending=False)
    fig2 = px.bar(df_country_city,
                x='country',
                y='city',
                color='country',
                text='city',
                labels={'country':'País','city':'Quantidade de Cidades'},
                title='Quantidade de Cidades Registradas por País')
    fig2.update_layout(showlegend=False,xaxis_title='Países')  
    fig2.update_traces(hovertemplate='<b>País:</b> %{x}<br><b>Quantidade de cidades:</b> %{y}<extra></extra>') 
    
    return fig2


def fig_country_rating():
    df_country_rating = df.groupby('country')[['votes']].mean().reset_index().sort_values('votes',ascending=False)
    df_country_rating['votes'] = df_country_rating['votes'].astype(int)
    fig3 = px.bar(df_country_rating,
                x='country',
                y='votes',
                color='country',
                text='votes',
                title='Média de Avaliações feitas por País',
                labels={'country':'País','votes':'Quantidade de Avaliações'})
    fig3.update_layout(showlegend=False,xaxis_title='Países')
    fig3.update_traces(hovertemplate='<b>País:</b> %{x}<br><b>Quantidade de avaliações:</b> %{y}<extra></extra>') 
    
    return fig3


def fig_country_currency_usd():
    df_country_currency_usd = df.groupby('country')[['currency_usd']].mean().reset_index().sort_values('currency_usd',ascending=False)
    df_country_currency_usd['currency_usd'] = df_country_currency_usd['currency_usd'].astype(int)
    fig4 = px.bar(df_country_currency_usd,
                x='country',
                y='currency_usd',
                color='country',
                text='currency_usd',
                title='Preço médio de um prato para duas pessoas por País',
                labels={'country':'País', 'currency_usd':'Preço médio'})
    fig4.update_layout(showlegend=False,xaxis_title='Países')
    fig4.update_traces(hovertemplate='<b>País:</b> %{x}<br><b>Preço médio:</b> %{y} dólares <extra></extra>')   
    
    return fig4  


df = clean_dataset(df_raw)

plotly_config = {"displayModeBar": False, "showTips": False}

# ===========================
#         Main Page
# ===========================

# --------- Sidebar ---------

st.set_page_config(layout="wide", page_title='Countries')

image_path = 'logo.png'
image = Image.open(image_path)

with st.sidebar:
    with st.container():
        col1, col2 = st.columns([1,3])
        
        with col1:
            st.image(image, width=50)
        
        with col2:
            st.markdown('# Fome Zero')
    
    st.header('Filtros')    
    
    countries = (st.multiselect(options=df['country'].unique(),
                   label='Escolha os Paises que Deseja visualizar os Restaurantes',
                   default=['Brazil','Philippines','Turkey','Sri Lanka','India']))

    st.sidebar.markdown('''---''')
    st.sidebar.markdown('# Powered by Lucas Meller')
    
    df = df.query('country in @countries')
    
# --------- Body ---------

st.header('Visão Países')

with st.container():
    st.plotly_chart(fig_country_name(), use_container_width=True, config=plotly_config)

with st.container():
    st.plotly_chart(fig_country_city(), use_container_width=True, config=plotly_config)
    
with st.container():
    col3, col4 = st.columns(2, gap='large')
    
    with col3:
        st.plotly_chart(fig_country_rating(), use_container_width=True, config=plotly_config)
    
    with col4:
        st.plotly_chart(fig_country_currency_usd(), use_container_width=True, config=plotly_config)
