import datetime
import streamlit as st
import base64
from iteru import GERD_aoi, GERD_SAR_timelaspe, Map


def app():

    st.header('Create Timelapse')
    st.markdown(
        'This app for creating the GERD timelapses from 2020-01-01 so far.')

    row1_col1, row1_col2 = st.columns([2, 1])
    with row1_col1:

        m = Map(zoom=10, center=(10.7, 35.2))
        m.remove_layer(m.layers[1])
        m.to_streamlit(height=600)

    with row1_col2:

        with st.form('TEST'):
            st.subheader('Customize Timelaspe')

            start_date = st.date_input(
                'Select Start Date', datetime.date(2020, 1, 1))
            end_date = st.date_input(
                'Select End Date', datetime.date.today())

            temp_freq = st.selectbox('Set Temporal Frequency',
                                     ('Native Temporal Resolution (12 days)', 'Monthly',
                                      'Quarterly'))

            vis_method = st.selectbox('Selecet Visualiation Method',
                                      ('RGB', 'Water Mask', 'RGB + Water Mosaic',
                                       'Single Band VH', 'Single Band VV'))
            framepersecond = st.slider(
                'Frame Per Second', max_value=5, min_value=1, value=3)

            date_font_size = st.slider(
                'Image Date Font Size', max_value=50, min_value=10, value=25)

            date_font_color = st.color_picker(
                'Image Date Font Color', '#1717E2')

            submitted = st.form_submit_button("Create")
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
