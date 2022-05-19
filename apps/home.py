import streamlit as st


def app():
    st.title("Iteru")

    st.markdown(
        """
    A [Google Earth Engine](https://earthengine.google.com/)-Based Interactive Web Application for Continuously
    Monitoring The [GERD](https://en.wikipedia.org/wiki/Grand_Ethiopian_Renaissance_Dam) Reservoir in Ethiopia Using 
    [Sentinel-1 SAR GRD](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD), [Iteru](https://github.com/MuhammedM294/Iteru), and [geemap](https://geemap.org/).
    
    """
    )

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader('Single Band VV')
        st.image("https://github.com/MuhammedM294/common_data/raw/main/gifs/VV.gif")

        st.subheader('RGB(Area 6)')
        st.image(
            "https://github.com/MuhammedM294/common_data/raw/main/gifs/RGB_AREA6.gif")

    with row1_col2:
        st.subheader('RGB')
        st.image(
            "https://github.com/MuhammedM294/common_data/raw/main/gifs/RGB.gif")
        st.subheader('RGB(Area 6)')
        st.image(
            "https://github.com/MuhammedM294/common_data/raw/main/gifs/RGB_AREA62.gif")
