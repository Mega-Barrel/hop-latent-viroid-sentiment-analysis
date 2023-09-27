import streamlit as st

from src.pages import (
    home as hp,
    compare as cp
)

# Page Config
st.set_page_config(layout="wide")
st.title('Twitter Sentiment Analytics')

# Sidebar navigation
pages_name_to_funcs = {
    "Tweet Analysis": hp.home_page,
    "Compare Keywords": cp.sample_page
}

if __name__ == '__main__':
    # Sidebar
    demo_name = st.sidebar.selectbox(
        "Choose a demo", 
        pages_name_to_funcs.keys()
    )
    pages_name_to_funcs[demo_name]()
