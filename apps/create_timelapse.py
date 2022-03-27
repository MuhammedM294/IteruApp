import datetime
from matplotlib.widgets import Widget
import streamlit as st
import base64
from ipyleaflet import FullScreenControl
from iteru import GERD_aoi, GERD_SAR_timelaspe, Map, GERD_water_stats
from ipywidgets import HTML



st.cache()
def app():

    st.header('Create Timelapse')
    st.markdown(
        'This app for creating the GERD timelapses from 2020-01-01 so far.')

    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        placeholder = st.empty()
        m = Map(zoom=10, center=(10.75, 35.2))
        m.remove_layer(m.layers[1])
        m.addLayer(GERD_aoi, {'color': 'red',
                              }, 'GERD-AOI')
        m.layers[1].opacity = 0.1
        x = m.to_streamlit(height=650, width=800, responsive=True)
       
        def zoom_to_GERD():
            m.zoom = 10
            m.center = (10.75, 35.2)
        zoom = st.button('Zoom to The GERD', on_click=zoom_to_GERD)
        
        
        
        
        
        

    with row1_col2:

        with st.form('timelapse'):

            st.subheader('Customize Timelaspe')
            valid_start_date = datetime.date(2020, 1, 1)
            valid_end_date = datetime.date.today()
            start_date = st.date_input(
                'Select Start Date', valid_start_date, key='start_date')

            end_date = st.date_input(
                'Select End Date', valid_end_date, key='end_date')

            temp_freq = st.selectbox('Set Temporal Frequency',
                                     ('Native Temporal Resolution (12 days)',
                                      'Monthly',
                                      'Quarterly'), key='temp_freq')

            temp_freq_dict = {'Native Temporal Resolution (12 days)': None,
                              'Monthly': 'monthly',
                              'Quarterly': 'quarterly'}

            vis_method = st.selectbox('Select Visualiation Method',
                                      ('RGB',
                                       'RGB + Water Mosaic',
                                       'Single Band (Water Mask)',
                                       'Single Band VH (B&W)',
                                       'Single Band VV (B&W)',
                                       'Single Band VH (W&B)',
                                       'Single Band VV (W&B)',
                                       ),
                                      key='vis_method'
                                      )

            vis_methods = {'RGB': 'rgb',
                           'Single Band (Water Mask)': 'water_mask_only',
                           'RGB + Water Mosaic': 'rgb_water_mosaic',
                           'Single Band VH (B&W)': 'single_band_VH',
                           'Single Band VV (B&W)': 'single_band_VV',
                           'Single Band VH (W&B)': 'single_band_VH_R',
                           'Single Band VV (W&B)': 'single_band_VV_R'
                           }

            if vis_method == 'Water Mask':
                copywrite_font_color = 'white'
            else:
                copywrite_font_color = 'black'

            framepersecond = st.slider(
                'Frame Per Second (Animation Speed)',
                max_value=5,
                min_value=1,
                value=3,
                key='framepersecond'
            )

            date_font_size = st.slider(
                'Date Label Font Size',
                max_value=50,
                min_value=10,
                value=25,
                key='date_font_size'

            )

            date_font_color = st.color_picker(
                'Date Label Font Color', '#000000',
                key='date_font_color')

            dimension = st.slider(
                'GIF Dimensions',
                max_value=1080,
                min_value=720,
                value=900,
                key=' dimension'
            )
            
            timelapse_button = st.form_submit_button("Create Timelapse")


            if timelapse_button:
                del x

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
                            
                            m.image_overlay(url=out_gif,
                                             bounds=((10.522199, 35.008243), (11.266588, 35.387092)),
                                             name = 'GERD_Timelapse')   
                            
                            row1_col1.empty()
                                

                            with row1_col1:

                                st.markdown(
                                    f'<img src="data:image/gif;base64,{data_url}" alt="GERD gif">',
                                    unsafe_allow_html=True,
                                )
                                with row1_col2:
                                    st.success('Done!')

                    except Exception:
                        st.error('Nope! Something went wrong!')

            st.subheader('Compute Water Statistics')
            water_area = st.checkbox('Water Surface Area',
                                     key='water_area')
            water_level = st.checkbox('Water Maximum Level',
                                      key='water_level')
            water_volume = st.checkbox('Water Volume',
                                       key='water_volume')
            statistics_button = st.form_submit_button("Compute Statistics")

            if statistics_button:

                water_stats = GERD_water_stats(GERD_aoi,
                                               startYear=st.session_state.start_date.year,
                                               startMonth=st.session_state.start_date.month,
                                               startDay=st.session_state.start_date.day,
                                               endYear=st.session_state.end_date.year,
                                               endMonth=st.session_state.end_date.month,
                                               endDay=st.session_state.end_date.day,
                                               temp_freq=temp_freq_dict[st.session_state.temp_freq],
                                               water_area=st.session_state.water_area,
                                               water_level=st.session_state.water_level,
                                               water_volume=st.session_state.water_volume,
                                               )

                if water_stats:

                    with row1_col1:

                        st.table(water_stats)
                        