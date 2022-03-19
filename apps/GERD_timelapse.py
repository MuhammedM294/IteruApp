import streamlit as st
from iteru import Map, GERD_SAR_timelaspe
import base64


@st.cache(suppress_st_warning=True)
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

    with row1_col2:
        with st.expander("Customize timelapse"):

            with st.form('TEST'):
                submitted = st.form_submit_button("Submit")

                if submitted:
                    out_gif = GERD_SAR_timelaspe()
                    file_ = open(out_gif, "rb")
                    contents = file_.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    file_.close()
                    st.markdown(
                        f'<img src="data:image/gif;base64,{data_url}>',
                        unsafe_allow_html=True,
                    )
