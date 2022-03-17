import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("Iteru")

    st.markdown(
        """
    A [Google Earth Engine](https://earthengine.google.com/) -Based Interactive Web Application for Continuously
    Monitoring The [GERD](https://en.wikipedia.org/wiki/Grand_Ethiopian_Renaissance_Dam) Reservoir Waterbody Using 
    [Sentinel-1 SAR GRD](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD), Google Earth Engine
    Python API, [iteru](https://github.com/MuhammedM294/Iteru), [geemap](https://geemap.org/).
    
    """
    )

    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        st.subheader('RGB')
        st.image("https://github.com/MuhammedM294/common_data/raw/main/gifs/rgb.gif")

    with row1_col2:
        st.subheader('RGB+Water Mask')
        st.image(
            "https://github.com/MuhammedM294/common_data/raw/main/gifs/rgb_water.gif")
    with row1_col3:
        st.subheader('Water Mask')
        st.image(
            "https://github.com/MuhammedM294/common_data/raw/main/gifs/water.gif")
