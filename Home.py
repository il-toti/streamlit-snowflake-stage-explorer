import streamlit as st

# Page config params
st.set_page_config(
    page_title="Snowflake Stage Inspector",
    page_icon="🔬",
    layout="wide",
)

# Sidebar info panels
st.sidebar.info("[GitHub](https://github.com/il-toti/streamlit-snowflake-stage-explorer)", icon="💻")
st.sidebar.info("[We are Infinite Lambda](https://infinitelambda.com/)", icon="👩🏻‍💻")

# Hone page body
st.title("Snowflake Stage Inspector")
st.markdown(
    """
    🔬Stage Inspector helps you to analyse your ❄️Snowflake internal and external stages.

    ### Explorer
    - Surf through your stages, check the parameters
    - Get a list of files on your stages
    - Even you can manage your stage files: upload, download or remove them

    ### Usage
    - Overall size of your internal stages
    - Getting familiar your biggest files

    
    You can check our [GitHub repository](https://github.com/il-toti/streamlit-snowflake-stage-explorer) or feel free to contact us!
    We are [Infinite Lambda](https://infinitelambda.com/).
"""
)
