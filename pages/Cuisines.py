# Importing libraries
import folium
import inflection
import pandas as pd
import plotly.express as px
import streamlit as st
from folium import Icon, IFrame, Popup
from folium.plugins import MarkerCluster
from PIL import Image
from streamlit_folium import folium_static

# Importing dataset
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


# ------- Cleaning dataset and functions
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


def df_best_italian():
    best_italian = (df_all.loc[df_all['cuisines'].apply(lambda x: False if str(x).find('Italian') == -1 else True),:]
                    .groupby(['restaurant_name','country','average_cost_for_two','currency','city'])[['aggregate_rating']].mean().reset_index()
                    .sort_values('aggregate_rating', ascending=False))
    
    return best_italian
      
        
def text_help_italian():
    help_italian = f'''
        País: {df_best_italian().iloc[0,1]} \n
        Cidade : {df_best_italian().iloc[0,4]} \n
        Média prato para dois: {df_best_italian().iloc[0,2]} {df_best_italian().iloc[0,3]}'''
        
    return help_italian


def df_best_american():
    best_american = (df_all.loc[df_all['cuisines'].apply(lambda x: False if str(x).find('American') == -1 else True),:]
                    .groupby(['restaurant_name','country','average_cost_for_two','currency','city'])[['aggregate_rating']].mean().reset_index()
                    .sort_values('aggregate_rating', ascending=False))
    
    return best_american
      
        
def text_help_american():
    help_american = f'''
        País: {df_best_american().iloc[0,1]} \n
        Cidade : {df_best_american().iloc[0,4]} \n
        Média prato para dois: {df_best_american().iloc[0,2]} {df_best_american().iloc[0,3]}'''
        
    return help_american


def df_best_arabian():
    best_arabian = (df_all.loc[df_all['cuisines'].apply(lambda x: False if str(x).find('Arabian') == -1 else True),:]
                    .groupby(['restaurant_name','country','average_cost_for_two','currency','city'])[['aggregate_rating']].mean().reset_index()
                    .sort_values('aggregate_rating', ascending=False))
    
    return best_arabian

def text_help_arabian():
    help_arabian = f'''
        País: {df_best_arabian().iloc[0,1]} \n
        Cidade : {df_best_arabian().iloc[0,4]} \n
        Média prato para dois: {df_best_arabian().iloc[0,2]} {df_best_arabian().iloc[0,3]}'''
        
    return help_arabian


def df_best_japanese():
    best_japanese = (df_all.loc[df_all['cuisines'].apply(lambda x: False if str(x).find('Japanese') == -1 else True),:]
                    .groupby(['restaurant_name','country','average_cost_for_two','currency','city'])[['aggregate_rating']].mean().reset_index()
                    .sort_values('aggregate_rating', ascending=False))

    return best_japanese

def text_help_japanese():
    help_japanese = f'''
        País: {df_best_japanese().iloc[0,1]} \n
        Cidade : {df_best_japanese().iloc[0,4]} \n
        Média prato para dois: {df_best_japanese().iloc[0,2]} {df_best_japanese().iloc[0,3]}'''
        
    return help_japanese


def df_best_author():
    best_author = (df_all.loc[df_all['cuisines'].apply(lambda x: False if str(x).find('Author') == -1 else True),:]
                .groupby(['restaurant_name','country','average_cost_for_two','currency','city'])[['aggregate_rating']].mean().reset_index()
                .sort_values('aggregate_rating', ascending=False))
    
    return best_author

def text_help_author():
    help_author = f'''
        País: {df_best_author().iloc[0,1]} \n
        Cidade : {df_best_author().iloc[0,4]} \n
        Média prato para dois: {df_best_author().iloc[0,2]} {df_best_author().iloc[0,3]}'''
    
    return help_author


def rank_restarant():
    top_restaurant = (df[['restaurant_id','restaurant_name','country','city','cuisines',
                        'average_cost_for_two','aggregate_rating','votes']].sort_values('aggregate_rating', ascending=False)
                        .sort_values(['aggregate_rating','restaurant_id'], ascending=[False,False]).drop_duplicates()).drop_duplicates()
    return top_restaurant


def fig_df_top10_best_cuisines():
    df_top10_best_cuisines = (df_all.groupby('cuisines')[['aggregate_rating']].mean().reset_index().sort_values('aggregate_rating', ascending=False).iloc[:10,:])
    df_top10_best_cuisines['aggregate_rating'] = df_top10_best_cuisines['aggregate_rating'].apply(lambda x: round(x,1))
    fig1 = px.bar(df_top10_best_cuisines,
            x='cuisines',
            y='aggregate_rating',
            text='aggregate_rating',
            title='Top 10 Melhores Tipos de Culinárias',
            color='cuisines',
            labels={'aggregate_rating':'Avaliação Média','cuisines':'Tipos de Culinária'})
    fig1.update_layout(showlegend=False)
    fig1.update_traces(hovertemplate='Tipo Culinário: %{x}<br>Avaliação Média: %{y}<extra></extra>') 
    
    return fig1


def fig_df_top10_worst_cuisines():
    df_top10_worst_cuisines = (df_all.groupby('cuisines')[['aggregate_rating']].mean().reset_index().sort_values('aggregate_rating').iloc[2:12,:])
    df_top10_worst_cuisines['aggregate_rating'] = df_top10_worst_cuisines['aggregate_rating'].apply(lambda x: round(x,1))
    fig2 = px.bar(df_top10_worst_cuisines,
            x='cuisines',
            y='aggregate_rating',
            text='aggregate_rating',
            title='Top 10 Piores Tipos de Culinárias',
            color='cuisines',
            labels={'aggregate_rating':'Avaliação Média','cuisines':'Tipos de Culinária'})
    fig2.update_layout(showlegend=False)
    fig2.update_traces(hovertemplate='Tipo Culinário: %{x}<br>Avaliação Média: %{y}<extra></extra>') 
    
    return fig2


df = clean_dataset(df_raw)
df_all = clean_dataset(df_raw)

plotly_config = {"displayModeBar": False, "showTips": False}

# ===========================
#         Main Page
# ===========================

# --------- Sidebar ---------

st.set_page_config(layout="wide", page_title='Cuisines')

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
    
    qt_restaurant = st.slider(label='Selecione a quantidade de Restaurantes que deseja visualizar', min_value=1, max_value=20, value=10)
    
    cuisines = (st.multiselect(options=df['cuisines'].unique(),
                               label='Escolha os Tipos de Culinária',
                               default=['BBQ', 'Japanese', 'Arabian', 'Brazilian', 'Author']))

    st.sidebar.markdown('''---''')
    st.sidebar.markdown('# Powered by Lucas Meller')
    
    df = df.query('country in @countries and cuisines in @cuisines')
    
# --------- Body ---------

st.markdown('# Visão Culinárias')

st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap='large')
    
    with col1:
        st.metric(label=f'Italiana: {df_best_italian().iloc[0,0]}',
                  value=f'{df_best_italian().iloc[0,5]}/5.0',
                  help=text_help_italian())
        
    with col2:
        st.metric(label=f'Americana: {df_best_american().iloc[0,0]}',
                  value=f'{df_best_american().iloc[0,5]}/5.0',
                  help=text_help_american())
        
    with col3:
        st.metric(label=f'Arábica: {df_best_arabian().iloc[0,0]}',
                  value=f'{df_best_arabian().iloc[0,5]}/5.0',
                  help=text_help_arabian())
        
    with col4:
        st.metric(label=f'Japonesa: {df_best_japanese().iloc[0,0]}',
                  value=f'{df_best_japanese().iloc[0,5]}/5.0',
                  help=text_help_japanese())
        
    with col5:
        st.metric(label=f'Autoral: {df_best_author().iloc[0,0]}',
                  value=f'{df_best_author().iloc[0,5]}/5.0',
                  help=text_help_author())

with st.container():
    st.markdown(f'# Top {qt_restaurant} Restaurantes')
    st.dataframe(rank_restarant().iloc[:qt_restaurant,:], use_container_width=True)

with st.container():
    col6, col7 = st.columns(2, gap='large')
    
    with col6:
        st.plotly_chart(fig_df_top10_best_cuisines(), config=plotly_config, use_container_width=True)
        
    with col7:
        st.plotly_chart(fig_df_top10_worst_cuisines(), config=plotly_config, use_container_width=True)
        
