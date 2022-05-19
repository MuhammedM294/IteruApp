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


@st.cache
def app():

    st.header('Compute Waterbody Statistcis')
    st.markdown(
        'This app is for computing the surface water area and the waterbody volume of the GERD reservoir.')

    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:

        m = Map(zoom=10, center=(10.75, 35.2))
        m.remove_layer(m.layers[1])
        m.addLayer(GERD_aoi_dam, {'color': 'red',
                                  }, 'GERD-AOI')
        m.layers[1].opacity = 0.1
        m.to_streamlit(height=650, width=800, responsive=True)

    with row1_col2:

        with st.form('image_dates'):

            st.subheader('1. Select a time span (at least a month)')
            valid_start_date = datetime.date(2020, 7, 1)
            valid_end_date = datetime.date.today()
            start_date = st.date_input(
                'Select Start Date (NOT before 1 July 2020)', valid_start_date, key='start_date')

            end_date = st.date_input(
                'Select End Date', valid_end_date, key='end_date')
            st.subheader('2. Select an image')
            show_images = st.form_submit_button("Show available images")

            if show_images:
                try:
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
                            'The start date should be before the end date')
                        st.stop()
                    elif 0 <= (end_date - start_date).days < 30:
                        st.error(
                            'It should be at least one month between the start and end dates')
                        st.stop()
                except:
                    pass
                else:

                    user_start_date = f'{st.session_state.start_date.year}-{st.session_state.start_date.month}-{st.session_state.start_date.day}'
                    user_end_date = f'{st.session_state.end_date.year}-{st.session_state.end_date.month}-{st.session_state.end_date.day}'
                    SAR = ee.ImageCollection('COPERNICUS/S1_GRD')\
                        .filter(ee.Filter.equals('relativeOrbitNumber_start', 50))\
                        .filter(ee.Filter.eq('instrumentMode', 'IW'))\
                        .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))\
                        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))\
                        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))\
                        .filter(ee.Filter.eq('resolution_meters', 10))\
                        .filterBounds(GERD_aoi)\
                        .filterDate(user_start_date, user_end_date)\
                        .select(['VV'])
                    dates_dict = get_imgCol_dates_dict(SAR)

                    if dates_dict not in st.session_state:
                        st.session_state.dates_dict = dates_dict

                    dates = st.radio('The Available Images',
                                     list(dates_dict.keys()),
                                     key='dates'
                                     )

            st.subheader('3. Compute Statistcis')
            compute_stats = st.form_submit_button("Compute Statistics")
            if compute_stats:
                try:

                    if 'dates' not in st.session_state:
                        st.session_state.dates = dates
                    system_start_time = st.session_state.dates_dict[st.session_state.dates]
                    stats, layers = SAR_VV_stats_single_img(
                        system_start_time, GERD_aoi_dam)

                    st.subheader('4. Results')

                    st.markdown('1. Image Acquisition Date')
                    st.write(st.session_state.dates)

                    st.markdown('2. Surface Water Area (km²)')
                    st.write(round(stats['Area'], 3))

                    predicted_volume = poly_expected_value(
                        obvserved_area_54, observed_volume_54, stats['Area'])

                    if abs(predicted_volume-stats['Volume']) > 2:

                        st.markdown(
                            '3. Waterbody Predicted Volume (Billion m³)')
                        st.caption(
                            '(predicted based on area change)')
                        st.write(round(predicted_volume, 3))

                    else:
                        st.markdown(
                            '3. Waterbody Predicted Volume (Billion m³)')
                        st.caption(
                            '(predicted based on area change)')
                        st.write(round(predicted_volume, 3))

                        st.markdown(
                            '4. Waterbody Observed Volume (Billion m³)')
                        st.caption('(observed from the image)')
                        st.write(round(stats['Volume'], 3))

                    with row1_col1:

                        m.add_ee_layer(
                            layers['SAR_VV'], {'min': -30, 'max': 5, 'bands': ['VV_Filtered']}, 'SAR_Image')
                        m.add_ee_layer(ee.FeatureCollection(
                            layers['Waterbody'].geometry()), {'color': 'blue'}, 'Waterbody')
                        m.addLayer(GERD_aoi_dam, {'color': 'red',
                                                  }, 'GERD-AOI')
                        m.to_streamlit(height=650, width=800, responsive=True)
                    with row1_col2:
                        st.success('Done!☺')

                except:
                    st.error(
                        'Select an image from the available images first')
