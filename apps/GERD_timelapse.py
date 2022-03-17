import streamlit as st


def app():
    from iteru import Map
    st.title("Create Sentinel-1 SAR GRD Timelapse for GERD")
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:

        '''    m = Map()
           m.center = (10.69399656037844, 35.22541966722389)
           m.zoom = 10
           map_layers = m.layers
           m.remove_layer(map_layers[1])
           m.to_streamlit(height=570) '''

    with row1_col2:
        with st.expander("Customize timelapse"):
            st.write('test test test')

            pass
