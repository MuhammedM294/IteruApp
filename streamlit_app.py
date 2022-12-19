import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, stats, timelapse

st.set_page_config(page_title="Iteru", layout="wide")


apps = {
    "home": {"title": "Home", "icon": "house"},
    "timelapse": {"title": "Timelapse", "icon": "map"},
    "stats": {"title": "Statistics", "icon": "calculator"}
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
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This web [app](https://share.streamlit.io/muhammedm294/iteruapp) is maintained by Muhammed Abdelaal. 
        You can follow me on:[GitHub](https://github.com/MuhammedM294) [Linkedin](https://www.linkedin.com/in/m294/).
        You can reach me at muhammedaabdelaal@gmail.com. 
        Source code: [Iteru](https://github.com/MuhammedM294/Iteru)
                     [IteruApp](https://github.com/MuhammedM294/IteruApp)

    """
    )

for app in apps:
    if apps[app]["title"] == selected:
        eval(f"{app}.app()")
        break
