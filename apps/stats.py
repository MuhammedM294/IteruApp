import datetime
from matplotlib.pyplot import show
from matplotlib.widgets import Widget
import streamlit as st
import base64
from ipyleaflet import FullScreenControl
from iteru import *
from ipywidgets import HTML
import ee
from statistics import mode


def app():

    st.header('Compute waterbody statistcis')
    st.markdown(
        'This app is for computing the surface water area and the waterbody volume of the GERD reservoir.')

    row1_col1, row1_col2 = st.columns([2, 1])

    # with row1_col1:

    #     m = Map(zoom=10, center=(10.75, 35.2))
    #     m.remove_layer(m.layers[1])
    #     m.addLayer(GERD_aoi_dam, {'color': 'red',
    #                               }, 'GERD-AOI')
    #     m.layers[1].opacity = 0.1
    #     m.to_streamlit(height=650, width=800, responsive=True)

    
