import streamlit as st

import snowflake.connector
from snowflake.connector import DictCursor
import os
from pathlib import Path

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake_stdemo"], client_session_keep_alive=True
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


# Remove a file from stage
def remove_from_stage(session, filename_with_path, selected_stage_type, selected_stage):
    if st.session_state.remove_file_confirmed:
        if selected_stage_type == "USER'S":
            sql = f'REMOVE \'@{selected_stage}/{filename_with_path}\''
        elif selected_stage_type == "INTERNAL":
            # remove the first part, which is exactly the stage name
            filename_with_path = filename_with_path[filename_with_path.find("/")+1:]
            sql = f'REMOVE \'@{selected_stage}/{filename_with_path}\''
        else:
            sql = ""

        if sql:
            # st.warning(sql)
            run_query_dict(session, sql)
            st.session_state["remove_file_confirmed"] = False
            st.cache_data.clear()
            st.experimental_rerun()
            # st.success('Successfully removed! Please refresh the list!', icon="🔄")
    else:
        st.error("To remove the file you have to check the confirmation checkbox!", icon="🚨")


# Download a file from stage
def download_from_stage(session, filename_with_path, selected_stage_type, selected_stage):
    if selected_stage_type == "USER'S":
        filename = os.path.basename(filename_with_path)
        sql = f"GET @~/{filename_with_path} file://./tmp"
    elif selected_stage_type == "INTERNAL":
        filename = os.path.basename(filename_with_path)
        # remove the first part, which is exactly the stage name
        filename_with_path = filename_with_path[filename_with_path.find("/")+1:]
        print(f"filename={filename}")
        print(f"filename_with_path={filename_with_path}")
        sql = f"GET \'@{selected_stage}/{filename_with_path}\' file://./tmp"
    else:
            sql = ""

    # Create the local tmp dir if it does not exist
    Path("./tmp/").mkdir(parents=True, exist_ok=True)
    # Get (copy) the file from our Snowflake stage
    with session.cursor(DictCursor) as cur:
        cur.execute(sql)
    #  Open the local file and send it to the browser
    f = open(f"./tmp/{filename}", "rb")

    return f, filename


# Upload file to stage
def upload_file_to_stage(session, uploaded_file, selected_stage):
    # st.write("uploaded_file.name=", uploaded_file.name)
    print(selected_stage)
    with session.cursor(DictCursor) as cur:
        cur.execute(f'PUT file://this_directory_path/is_ignored/{uploaded_file.name} \'@{selected_stage}\'', file_stream=uploaded_file)
    st.success('Successfully uploaded! To refresh the list please click the X of the uploaded file.', icon="🔄")
