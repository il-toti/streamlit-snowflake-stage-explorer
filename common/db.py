import streamlit as st

import snowflake.connector
from snowflake.connector import DictCursor

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


# Run a sql query and return a dict
@st.cache_data(ttl=3600)
def run_query_dict(_session, query):
    with _session.cursor(DictCursor) as cur:
        try:
            cur.execute(query)
            return cur.fetchall()
        except snowflake.connector.errors.ProgrammingError as e:
            st.error(str(e) + query, icon="🚨")
            st.warning('SQL query = "' + query +'"')
        finally:
            cur.close()


# Run a sql query and return a dict
@st.cache_data(ttl=3600)
def run_query_dict_error(_session, query):
    with _session.cursor(snowflake.connector.DictCursor) as cur:
        try:
            cur.execute(query)
            return cur.fetchall()
        except snowflake.connector.errors.ProgrammingError as e:
            pass
        finally:
            cur.close()
