import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pymongo import MongoClient


@st.cache_data
def load_data():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("connected successfully")
    except:
        print ("could not connect to mongoDB")
    db_Mongo = client.get_database('DSI_Abschlussprojekt')
    collection= db_Mongo.Geburten_nach_Einkommen_Wien
    df = pd.DataFrame(list(collection.find()))
    #data = pd.read_csv('clean_vie_data.csv').set_index('Unnamed: 0')
    df['District_code'] = df['District_code'].astype(str).str[:3]
    #print(data)
    return df


def render_info():
    st.title('Income & Birth rate')
    st.header('Impact of net income on birth rates by district of Vienna')


def filter_by_year(data):
    # adding a range slider, allowing to choose values in range
    range = st.slider('Year', min(data['Year']), max(data['Year']), (2002,2021))
    return data[(data['Year'].between(*range))]

def render_map(data):
    json_data = open('BEZIRKSGRENZEOGD (1).json', 'r')
    borders = json.load(json_data)

    st.subheader('Average net income by district of Vienna')

    tab1, tab2 = st.tabs(["Total", "Male vs. Female"])
    with tab1:
        fig_t = px.choropleth_mapbox(data, geojson=borders, color='Total_Salary',
                                   locations="District_code", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                   center={"lat": 48.210033, "lon": 16.363449},
                                   mapbox_style="carto-positron", zoom=9.8,
                                   opacity=0.5,
                                   color_continuous_scale = 'rdbu',
                                   labels={"Total_Salary": "Netto income"})
        fig_t.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_t, theme="streamlit", use_container_width=False)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Male")
            fig_m = px.choropleth_mapbox(data, geojson=borders, color='Male_Salary',
                                        locations="District_code", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                        center={"lat": 48.210033, "lon": 16.363449},
                                        mapbox_style="carto-positron", zoom=9,
                                        opacity=0.5,
                                        color_continuous_scale = 'rdbu',
                                        labels={"Male_Salary": "Netto income"},
                                        title='Male',
                                        range_color =[min(data['Female_Salary']), max(data['Male_Salary'])])
            fig_m.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_m, theme="streamlit", use_container_width=True)
        with col2:
            st.write("Female")
            fig_f = px.choropleth_mapbox(data, geojson=borders, color='Female_Salary',
                                         locations="District_code", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                         center={"lat": 48.210033, "lon": 16.363449},
                                         mapbox_style="carto-positron", zoom=9,
                                         opacity=0.5,
                                         color_continuous_scale = 'rdbu',
                                         labels={"Female_Salary": "Netto income"},
                                         title='Female',
                                         range_color =[min(data['Female_Salary']), max(data['Male_Salary'])])
            fig_f.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_f, theme="streamlit", use_container_width=True)
    st.subheader('Births by district of Vienna')

    fig_b = px.choropleth_mapbox(data, geojson=borders, color='Births',
                                 locations="District_code", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                 center={"lat": 48.210033, "lon": 16.363449},
                                 mapbox_style="carto-positron", zoom=9.8,
                                 opacity=0.5,
                                 color_continuous_scale = 'rdbu',
                                 labels={"Births": "Birth rate"})
    fig_b.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_b, theme="streamlit", use_container_width=True)

    json_data.close()


render_info()

with st.spinner('Loading data..'):
    data = load_data()

data=filter_by_year(data)

with st.spinner('Rendering map..'):
    render_map(data)