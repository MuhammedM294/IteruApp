import datetime
import streamlit as st
import base64
from iteru import GERD_aoi, GERD_SAR_timelaspe, Map, dates_params
import time


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

        with st.form('timelapse',clear_on_submit=True):

            st.subheader('Customize Timelaspe')
            valid_start_date = datetime.date(2020, 1, 1)
            valid_end_date = datetime.date.today()
            start_date = st.date_input(
                'Select Start Date', valid_start_date)

            end_date = st.date_input(
                'Select End Date', valid_end_date)

            temp_freq = st.selectbox('Set Temporal Frequency',
                                     ('Native Temporal Resolution (12 days)',
                                      'Monthly',
                                      'Quarterly'))

            temp_freq_dict = {'Native Temporal Resolution (12 days)': None,
                              'Monthly': 'monthly',
                              'Quarterly': 'quarterly'}

            vis_method = st.selectbox('Selecet Visualiation Method',
                                      ('RGB',
                                       'RGB + Water Mosaic',
                                       'Single Band (Water Mask)',
                                       'Single Band VH',
                                       'Single Band VV'))

            vis_methods = {'RGB': 'rgb',
                           'Water Mask': 'water_mask_only',
                           'RGB + Water Mosaic': 'rgb_water_mosaic',
                           'Single Band VH': 'single_band_VH',
                           'Single Band VV': 'single_band_VV'}

            if vis_method == 'Water Mask':
                copywrite_font_color = 'white'
            else:
                copywrite_font_color = 'black'

            framepersecond = st.slider(
                'Frame Per Second (Animation Speed)', max_value=5, min_value=1, value=3)

            date_font_size = st.slider(
                'Date Label Font Size', max_value=50, min_value=10, value=25)

            date_font_color = st.color_picker(
                'Date Label Font Color', '#000000')

            dimension = st.slider(
                'GIF Dimensions', max_value=1080, min_value=720, value=900)

            submitted = st.form_submit_button("Submit")
            if submitted:
                with st.spinner('Loading...'):
                    time.sleep(10)
                try:
                    out_gif = GERD_SAR_timelaspe(GERD_aoi,
                                                 startYear=start_date.year,
                                                 startMonth=start_date.month,
                                                 startDay=start_date.day,
                                                 endYear=end_date.year,
                                                 endMonth=end_date.month,
                                                 endDay=end_date.day,
                                                 temp_freq=temp_freq_dict[temp_freq],
                                                 vis_method=vis_methods[vis_method],
                                                 dates_font_size=date_font_size,
                                                 dates_font_color=date_font_color,
                                                 framesPerSecond=framepersecond,
                                                 copywrite_font_color=copywrite_font_color,
                                                 dimensions=dimension
                                                 )
                    if out_gif is None:
                        if start_date < valid_start_date:
                            st.error(
                                f'The start date should not be before {valid_start_date}')
                            st.stop()
                        elif end_date > valid_end_date:
                            st.error(
                                f'The end date should not be after {valid_end_date}')
                            st.stop()
                        elif (end_date - start_date).days < 0:
                            st.error(
                                'The start date should be prior the end date')
                            st.stop()
                        elif 0 <= (end_date - start_date).days < 30:
                            st.error(
                                'It should be at least one month between the start date and the end date')
                            st.stop()
                        else:
                            st.error(
                                'Too much data requested: reduce the gif dimensions or the timespan')
                            st.stop()
                except Exception as e:
                    st.exception(e)
                else:

                    try:

                        file_ = open(out_gif, "rb")
                        contents = file_.read()
                        data_url = base64.b64encode(contents).decode("utf-8")
                        file_.close()

                        with row1_col1:

                            st.markdown(
                                f'<img src="data:image/gif;base64,{data_url}>',
                                unsafe_allow_html=True,
                            )
                            with row1_col2:
                                st.success('Done!')
                                st.download_button(
                                    label="Download GIF",
                                    data=out_gif,
                                    file_name='GERD_timelapse.gif',
                                    mime='application/octet-stream',
                                )
                    except Exception:
                        st.error('Nope! Something went wrong!')
