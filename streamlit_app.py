import streamlit as st
from streamlit_option_menu import option_menu
from .apps import home, heatmap

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = {
    "home": {"title": "Home", "icon": "house"},
    "heatmap": {"title": "Heatmap", "icon": "map"},
}

titles = [app["title"] for app in apps.values()]
icons = [app["icon"] for app in apps.values()]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Apps List",
        options=['Home', 'Heatmap'],
        icons=['house', 'map'],
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This web [app](https://share.streamlit.io/muhammedm294/iteruapp) is maintained by Muhammed Abdelaal. You can follow me on social media:
            [GitHub](https://github.com/MuhammedM294) | [Twitter](https://twitter.com/MuhammedM294).
        
        Source code: <https://github.com/MuhammedM294/IteruApp>

    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
