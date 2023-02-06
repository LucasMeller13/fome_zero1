# Importing libraries
import folium
import pandas as pd
import streamlit as st
from folium import Icon, IFrame, Popup
from folium.plugins import MarkerCluster
from PIL import Image
import inflection
from streamlit_folium import folium_static

# Importing dataset
df_raw = pd.DataFrame(pd.read_csv('./dataset/zomato.csv'))

# Cleaning dataset
def clean_dataset(dataframe):
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

    def usd_currencies(number, code):
        return number*currency_code[code]

    dataframe['Currency_usd'] = dataframe[['Average Cost for two','Currency']].apply(lambda a: usd_currencies(a['Average Cost for two'],
                                                                                                a['Currency']), axis=1)

    dataframe = dataframe[dataframe['Restaurant ID'] != 16608070]

    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }

    def color_name(color_code):
        return COLORS[color_code]

    dataframe['color'] = dataframe['Rating color'].apply(lambda x: color_name(x))
    dataframe['country'] = dataframe['Country Code'].apply(lambda x: country_name(x))
    dataframe['price_tye'] = dataframe['Price range'].apply(lambda x: create_price_tye(x))

    dataframe = dataframe.dropna(axis=0)
    
    dataframe["Cuisines"] = dataframe.loc[:, "Cuisines"].apply(lambda x: x.split(",")[0])

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

    dataframe = rename_columns(dataframe)

    return dataframe


df = clean_dataset(df_raw)
df_all = clean_dataset(df_raw)

# ===========================
#         Main Page
# ===========================

# --------- Sidebar ---------

st.set_page_config(layout="wide", page_title='Main Page')

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
                   default=['Brazil','Philippines','Turkey','Sri Lanka','Canada']))
    
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('# Powered by Lucas Meller')
    
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(df_raw)

    st.header('Dados Tratados')
    st.download_button(label='Download',data=csv, file_name='data.csv')
    
    df = df.query('country in @countries')


# --------- Body ---------
    
st.header('Fome Zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')

col3, col4, col5, col6, col7 = st.columns(5)

with col3:
    restaurant_nunique = df_all['restaurant_name'].nunique()
    st.metric('Restaurantes cadastrados:', value=restaurant_nunique)

with col4:
    country_nunique = df_all['country'].nunique()
    st.metric('Países cadastrados:', value=country_nunique)

with col5:
    cities_nunique = df_all['city'].nunique()
    st.metric('Cidades cadastradas:', value=cities_nunique)
    
with col6:
    count_votes = df_all['votes'].sum()
    st.metric('Avaliações feitas na plataforma:', value=f'{count_votes:,}')
    
with col7:
    cuisines_nunique = df_all['cuisines'].nunique()
    st.metric('Tipos de culinárias oferecidas:', value=cuisines_nunique)
    

with st.container():
    df_map = df.loc[df[['restaurant_name','address','longitude','latitude','locality','cuisines']].duplicated() == False]
    list_location = []
    df_map[['latitude','longitude']].apply(lambda x: list_location.append([x['latitude'], x['longitude']]), axis=1)
    #restaurant_name = df_map['restaurant_name'].values.tolist()

    map1 = folium.Map()

    marker_cluster = MarkerCluster().add_to(map1)

    for i in range(len(df_map)):
        iframe = IFrame('<br><b>'+ str(df_map.iloc[i,1]) +'</b><br><br>Price: '+ str(df_map.iloc[i,10]) +' '+str(df_map.iloc[i,11])+' para dois<br>Type: '+str(df_map.iloc[i,9])+'<br>Aggregate rating: '+str(df_map.iloc[i,17])+'/5.0')
        popup = Popup(iframe, min_width=300, max_width=300)
        folium.Marker([list_location[i][0],list_location[i][1]], popup=popup, icon=Icon(color=df_map.iloc[i,22], prefix="fa-sharp fa-solid fa-house")).add_to(marker_cluster)

    folium_static(map1, width=1024, height=600)
