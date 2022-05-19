import datetime
from matplotlib.widgets import Widget
from requests import session
import streamlit as st
import base64
from ipyleaflet import FullScreenControl
from iteru import *
from ipywidgets import HTML


def app():

    st.header('Create Timelapse')
    st.markdown(
        'This app is for creating the GERD time-lapses from 2020-07-01 so far.')

    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:

        m = Map(zoom=10, center=(10.75, 35.2))
        m.remove_layer(m.layers[1])
        m.addLayer(GERD_aoi, {'color': 'red',
                              }, 'GERD AOI(Zoom 11)')
        m.addLayer(aois['zoom_14_1'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 1)')
        m.addLayer(aois['zoom_14_2'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 2)')
        m.addLayer(aois['zoom_14_3'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 3)')
        m.addLayer(aois['zoom_14_4'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 4)')
        m.addLayer(aois['zoom_14_5'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 5)')
        m.addLayer(aois['zoom_14_7'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 6)')
        m.addLayer(aois['zoom_14_8'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 7)')
        m.addLayer(aois['zoom_14_6'], {'color': 'blue',
                                       }, 'GERD AOI(Zoom 14 Area 8)')
        m.layers[1].opacity = 0.2
        for i in range(2, 10):
            m.layers[i].opacity = 0.2
        m.to_streamlit(height=650, width=800, responsive=True)

    with row1_col2:

        with st.form('timelapse'):

            st.subheader('Customize Timelaspe')
            valid_start_date = datetime.date(2020, 7, 1)
            valid_end_date = datetime.date.today()
            study_areas = {'The Whole Reservoir(Zoom Level 11)': GERD_aoi,
                           'Area 1(Zoom Level 14)': aois['zoom_14_1'],
                           'Area 2(Zoom Level  14)': aois['zoom_14_2'],
                           'Area 3(Zoom Level 14)': aois['zoom_14_3'],
                           'Area 4(Zoom Level 14)': aois['zoom_14_4'],
                           'Area 5(Zoom Level 14)': aois['zoom_14_5'],
                           'Area 6(Zoom Level 14)': aois['zoom_14_7'],
                           'Area 7(Zoom Level 14)': aois['zoom_14_8'],
                           'Area 8(Zoom Level 14)': aois['zoom_14_6'],
                           }
            study_area = st.radio('1. Select study area',
                                  list(study_areas.keys()),
                                  key='study_area')
            if 'study_area' not in st.session_state:
                st.session_state.study_area = study_area

            start_date = st.date_input(
                '2. Select start date (NOT before 1 July 2020)', valid_start_date, key='start_date')

            end_date = st.date_input(
                '3. Select end date', valid_end_date, key='end_date')

            temp_freq = st.selectbox('4. Set temporal frequency',
                                     ('Native temporal resolution (12 days)',
                                      'Monthly',
                                      'Quarterly'), key='temp_freq')

            temp_freq_dict = {'Native temporal resolution (12 days)': None,
                              'Monthly': 'monthly',
                              'Quarterly': 'quarterly'}

            vis_method = st.selectbox('5. Select visualiation method',
                                      ('RGB',
                                       'Single Band VV',
                                       'Single Band VH',
                                       ),
                                      key='vis_method'
                                      )

            vis_methods = {'RGB': 'rgb',
                           'Single Band VH': 'single_band_VH',
                           'Single Band VV': 'single_band_VV',
                           }

            if vis_method == 'Water Mask':
                copywrite_font_color = 'white'
            else:
                copywrite_font_color = 'black'

            framepersecond = st.slider(
                '6. Frame per second (animation speed)',
                max_value=5,
                min_value=1,
                value=3,
                key='framepersecond'
            )

            date_font_size = st.slider(
                '7. Font size(date label)',
                max_value=50,
                min_value=10,
                value=25,
                key='date_font_size'

            )

            date_font_color = st.color_picker(
                '8. Font color(date label)', '#000000',
                key='date_font_color')

            dimension = st.slider(
                '9. GIF dimensions',
                max_value=1080,
                min_value=720,
                value=900,
                key=' dimension'
            )

            timelapse_button = st.form_submit_button("Submit")

            if timelapse_button:

                if 'start_date' not in st.session_state:
                    st.session_state.start_date = start_date
                if 'end_date' not in st.session_state:
                    st.session_state.end_date = end_date

                if st.session_state.start_date < valid_start_date:
                    st.error(
                        f'The start date should not be before {valid_start_date}')
                    st.stop()
                elif st.session_state.end_date > valid_end_date:
                    st.error(
                        f'The end date should not be after {valid_end_date}')
                    st.stop()
                elif (st.session_state.end_date - st.session_state.start_date).days < 0:
                    st.error(
                        'The start date should be before the end date')
                    st.stop()
                elif 0 <= (st.session_state.end_date - st.session_state.start_date).days < 30:
                    st.error(
                        'It should be at least one month between the start and end dates')
                    st.stop()

                try:
                    if study_areas[st.session_state.study_area] == GERD_aoi:
                        zoom_level = "Zoom Level: 11"
                    else:
                        zoom_level = "Zoom Level: 14"
                    out_gif = GERD_SAR_timelaspe(study_areas[st.session_state.study_area],
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
                                                 dimensions=dimension,
                                                 zoom_level_font_size=15,
                                                 zoom_level=zoom_level
                                                 )
                    if out_gif is None:
                        st.error(
                            'Many images requested; reduce the gif dimensions or timespan')
                        st.stop()
                except Exception as e:
                    print(e)
                else:

                    try:

                        file_ = open(out_gif, "rb")
                        contents = file_.read()
                        data_url = base64.b64encode(contents).decode("utf-8")
                        file_.close()

                        m.image_overlay(url=out_gif,
                                        bounds=((10.522199, 35.008243),
                                                (11.266588, 35.387092)),
                                        name='GERD_Timelapse')

                        row1_col1.empty()

                        with row1_col1:

                            st.markdown(
                                f'<img src="data:image/gif;base64,{data_url}" alt="GERD gif">',
                                unsafe_allow_html=True,
                            )
                            with row1_col2:
                                st.success('Done!☺')

                    except Exception:
                        st.error('Nope! Something went wrong!')

    with row1_col2:

        st.subheader('Compute statistics')

        with st.form('image_dates'):

            st.subheader('1. Select a time span (at least a month)')
            valid_start_date = datetime.date(2020, 7, 1)
            valid_end_date = datetime.date.today()
            start_date = st.date_input(
                'Select Start Date (NOT before 1 July 2020)', valid_start_date, key='start_date')

            end_date = st.date_input(
                'Select end date', valid_end_date, key='end_date')
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

                    dates = st.radio('The available images',
                                     list(dates_dict.keys()),
                                     key='dates'
                                     )

            st.subheader('3. Compute statistcis')
            compute_stats = st.form_submit_button("Compute")
            if compute_stats:
                try:

                    if 'dates' not in st.session_state:
                        st.session_state.dates = dates
                    system_start_time = st.session_state.dates_dict[st.session_state.dates]
                    stats, layers = SAR_VV_stats_single_img(
                        system_start_time, GERD_aoi_dam)

                    st.subheader('4. Results')

                    st.markdown('1. Image acquisition date')
                    st.write(st.session_state.dates)

                    st.markdown('2. Surface water area (km²)')
                    st.write(round(stats['Area'], 3))

                    predicted_volume = poly_expected_value(
                        obvserved_area_54, observed_volume_54, stats['Area'])

                    if abs(predicted_volume-stats['Volume']) > 2:

                        st.markdown(
                            '3. Waterbody predicted volume (billion m³)')
                        st.caption(
                            '(Predicted based on area change)')
                        st.write(round(predicted_volume, 3))

                    else:
                        st.markdown(
                            '3. Waterbody predicted volume (billion m³)')
                        st.caption(
                            '(Predicted based on area change)')
                        st.write(round(predicted_volume, 3))

                        st.markdown(
                            '4. Waterbody observed volume (billion m³)')
                        st.caption('(Observed from the image)')
                        st.write(round(stats['Volume'], 3))

                    with row1_col1:

                        m = Map(zoom=10, center=(10.75, 35.2))
                        m.remove_layer(m.layers[1])

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
