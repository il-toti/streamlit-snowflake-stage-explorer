import streamlit as st

st.set_page_config(
    page_title="Snowflake Stages",
    page_icon="👋",
)

st.write("# Snowflake Stage Inspector")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    Stage Inspector helps you to analyse your Snowflake internal and external stages.

    ### Explorer
    - surf through your stages, check the parameters and get a list of files on your stages
    - manage files, upload, download or remove them

    ### Usage
    - look for the biggest files on your internal stages
"""
)