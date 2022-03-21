import streamlit as st
import base64
from iteru import GERD_aoi, GERD_SAR_timelaspe, Map
import datetime

st.header('Create Timelapse')
st.text('Create Timelapse')


row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    m = Map(zoom=10, center=(10.65, 35.2))
    m.remove_layer(m.layers[1])
    m.to_streamlit()


with row1_col2:

    with st.form('TEST'):
        st.subheader('Customize Timelaspe')
        submitted = st.form_submit_button("Submit")

        if submitted:
            out_gif = GERD_SAR_timelaspe(GERD_aoi)
            file_ = open(out_gif, "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
                unsafe_allow_html=True,
            )
