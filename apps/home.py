import streamlit as st


def app():
    st.title("Iteru")

    st.markdown(
        """
    A [Google Earth Engine](https://earthengine.google.com/)-Based Interactive Web Application for Continuously
    Monitoring the [GERD](https://en.wikipedia.org/wiki/Grand_Ethiopian_Renaissance_Dam) Reservoir in Ethiopia Using 
    [Sentinel-1 SAR GRD](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD), [Iteru](https://github.com/MuhammedM294/Iteru), and [geemap](https://geemap.org/).
    
    """
    )

    st.subheader('Sentinel-2 RGB(Acquired on 09-05-2022)')
    st.image(
        'https://github.com/MuhammedM294/data/raw/main/gifs/S2_2022_05_09.png')
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:

        st.subheader('Single Band VV')
        st.image("https://github.com/MuhammedM294/data/raw/main/gifs/VV.gif")

    with row1_col2:
        st.subheader('RGB')
        st.image(
            "https://github.com/MuhammedM294/data/raw/main/gifs/RGB.gif")
