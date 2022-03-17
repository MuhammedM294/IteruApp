from posixpath import basename
from turtle import position, width
from folium import LayerControl
import iteru
import streamlit as st
import ipyleaflet

st.set_page_config(page_title="Iteru", layout="wide")
st.title('Iteru: A Google Earth Engine-Based Web Application for Continuously Monitoring The GERD Reservoir Water')
Map = iteru.Map()

Map.add_control(ipyleaflet.ScaleControl(position='bottomleft'))
Map.to_streamlit(height=600)
