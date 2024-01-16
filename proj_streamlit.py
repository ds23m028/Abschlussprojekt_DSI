import streamlit as st
import pandas as pd
import json
import plotly.express as px

@st.cache_data
def load_data():
    data = pd.read_csv('clean_vie_data.csv').set_index('Unnamed: 0')
    data['DISTRICT_CODE'] = data['DISTRICT_CODE'].astype(str).str[:3]
    #print(data)
    return data


def render_info():
    st.title('Income & Birth rate')
    st.header('Impact of net income on birth rates by district of Vienna')


def filter_by_year(data):
    # adding a range slider, allowing to choose values in range
    range = st.slider('Year', min(data['REF_YEAR']), max(data['REF_YEAR']), (2002,2021))
    return data[(data['REF_YEAR'].between(*range))]

def render_map(data):
    json_data = open('BEZIRKSGRENZEOGD (1).json', 'r')
    borders = json.load(json_data)

    st.subheader('Average net income by district of Vienna')

    tab1, tab2 = st.tabs(["Total", "Male vs. Female"])
    with tab1:
        fig_t = px.choropleth_mapbox(data, geojson=borders, color='INC_TOT_VALUE',
                                   locations="DISTRICT_CODE", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                   center={"lat": 48.210033, "lon": 16.363449},
                                   mapbox_style="carto-positron", zoom=9.8,
                                   opacity=0.5,
                                   color_continuous_scale = 'rdbu',
                                   labels={"INC_TOT_VALUE": "Netto income"})
        fig_t.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_t, theme="streamlit", use_container_width=False)
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("Male")
            fig_m = px.choropleth_mapbox(data, geojson=borders, color='INC_MAL_VALUE',
                                        locations="DISTRICT_CODE", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                        center={"lat": 48.210033, "lon": 16.363449},
                                        mapbox_style="carto-positron", zoom=9,
                                        opacity=0.5,
                                        color_continuous_scale = 'rdbu',
                                        labels={"INC_MAL_VALUE": "Netto income"},
                                        title='Male',
                                        range_color =[min(data['INC_FEM_VALUE']), max(data['INC_MAL_VALUE'])])
            fig_m.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_m, theme="streamlit", use_container_width=True)
        with col2:
            st.write("Female")
            fig_f = px.choropleth_mapbox(data, geojson=borders, color='INC_FEM_VALUE',
                                         locations="DISTRICT_CODE", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                         center={"lat": 48.210033, "lon": 16.363449},
                                         mapbox_style="carto-positron", zoom=9,
                                         opacity=0.5,
                                         color_continuous_scale = 'rdbu',
                                         labels={"INC_FEM_VALUE": "Netto income"},
                                         title='Female',
                                         range_color =[min(data['INC_FEM_VALUE']), max(data['INC_MAL_VALUE'])])
            fig_f.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_f, theme="streamlit", use_container_width=True)
    st.subheader('Births by district of Vienna')

    fig_b = px.choropleth_mapbox(data, geojson=borders, color='BIR',
                                 locations="DISTRICT_CODE", featureidkey="properties.STATAUSTRIA_BEZ_CODE",
                                 center={"lat": 48.210033, "lon": 16.363449},
                                 mapbox_style="carto-positron", zoom=9.8,
                                 opacity=0.5,
                                 color_continuous_scale = 'rdbu',
                                 labels={"BIR": "Birth rate"})
    fig_b.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_b, theme="streamlit", use_container_width=True)

    json_data.close()


render_info()

with st.spinner('Loading data..'):
    data = load_data()

data=filter_by_year(data)

with st.spinner('Rendering map..'):
    render_map(data)