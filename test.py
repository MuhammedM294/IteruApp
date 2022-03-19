import PIL
from geemap import sentinel2_timelapse
import streamlit as st
import base64
from iteru import *


from geemap import sentinel2_timelapse
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:

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
