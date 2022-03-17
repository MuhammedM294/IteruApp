import streamlit as st
from iteru import *


def app():

    st.title("Create Sentinel-1 SAR GRD Timelapse for GERD")
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:

        m = Map()
        m.center = (10.69399656037844, 35.22541966722389)
        m.zoom = 10
        map_layers = m.layers
        m.remove_layer(map_layers[1])
        m.to_streamlit(height=570)

        GERD_aoi = ee.Geometry.Polygon([[[
            35.008243,
            10.522199
        ],
            [
            35.008243,
            11.266588
        ],
            [
            35.387092,
            11.266588
        ],
            [
            35.387092,
            10.522199
        ],
            [
            35.008243,
            10.522199
        ]]])
    with row1_col2:
        with st.expander("Customize timelapse"):
            st.write('test')

            pass
