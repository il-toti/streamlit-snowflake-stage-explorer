import streamlit as st
from snowflake.connector import DictCursor

import common.sidebar as sb
import common.db as db
import common.utils as ut

from datetime import datetime
import streamlit.components.v1 as components
import base64
import os
from pathlib import Path

# -----------------------------------------------
# Helper functions for this page

# Remove a file from stage
def remove_from_stage():
    filename_with_path = st.session_state.file
    if st.session_state.remove_file_confirm:
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
            db.run_query_dict(session, sql)
            ut.clear_cache()
            st.session_state.remove_file_confirm = False
    else:
        st.error("To remove the file you have to check the confirmation checkbox!")


# Generate a download button to the page
# Solution Source: https://discuss.streamlit.io/t/automatic-download-select-and-download-file-with-single-button-click/15141/4
def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """
    # if isinstance(object_to_download, pd.DataFrame):
    #     object_to_download = object_to_download.to_csv(index=False)

    # # Try JSON encode for everything else
    # else:
    #     object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


# Download a file from stage
def download_from_stage():
    print(os.listdir("./tmp/"))
    # Get the pure filename and the filename with full stage path
    filename_with_path = st.session_state.file

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
    print(os.listdir("./tmp/"))
    st.write(os.listdir("./tmp/"))
    st.write(f)
    components.html(
        download_button(f.read(), filename),
        height=0,
    )


# Upload file to stage
def upload_file_to_stage(uploaded_file):
    # st.write("uploaded_file.name=", uploaded_file.name)
    print(selected_stage)
    with session.cursor(DictCursor) as cur:
        cur.execute(f'PUT file://this_directory_path/is_ignored/{uploaded_file.name} \'@{selected_stage}\'', file_stream=uploaded_file)


# -----------------------------------------------
# App starts here
st.set_page_config(page_title="ILSFAPP", layout="wide")
session = db.init_connection()
st.title('Stage explorer')
sb.info_panel()

# Get all the stages under this account
data_stages = db.run_query_dict(session, 'show stages in account')

# If you need the raw data...
# expand_stages = st.expander("Stages raw table")
# expand_stages.write(data_stages)

# Show the filters
filter_col1, filter_col2 = st.columns([1,4])
selected_stage_type = filter_col1.selectbox(
        "Choose a stage type",
        ["USER'S", "INTERNAL", "EXTERNAL"],
        label_visibility = "collapsed",
    )

# Create the stage list for the dropwdown list, adding the user's stage as well
stages = []
if selected_stage_type == "USER'S":
    stages.append("~")
else:
    for stage in data_stages:
        if selected_stage_type == stage["type"]:
            stages.append(stage["database_name"] + "." + stage["schema_name"] + "." + 
                          '"'+stage["name"]+'"' if stage["name"].find(" ") else stage["name"]
                         )
    stages.sort()

# Show the stage dropdown
selected_stage = filter_col2.selectbox(
        "Choose a stage",
        stages,
        label_visibility = "collapsed",
    )

# Create three tabs for the different info subpages
tab_files, tab_stage, tab_integration = st.tabs(["Files","Stage details","Integration"])

# Show the choosen stage details if it is not the user's
if selected_stage_type == "USER'S":
    tab_stage.info("Not available on user's stage!")
if selected_stage_type in ["INTERNAL", "EXTERNAL"]:
    # Stage details
    for stage in data_stages:
        if selected_stage == (stage["database_name"] + "." + stage["schema_name"] + "." + '"'+stage["name"]+'"' if stage["name"].find(" ") else stage["name"]):
            data_selected_stage = stage
    
    tab_stage.text(    "Owner: " + str(data_selected_stage["owner"])
              + "\nCreated: " + data_selected_stage["created_on"].strftime("%Y-%m-%d %H:%M:%S")
              + "\nComment: " + str(data_selected_stage["comment"])
              )
if selected_stage_type == "EXTERNAL":
    tab_stage.text(    "Cloud/region: " + str(data_selected_stage["cloud"]) + "/" + str(data_selected_stage["region"])
              + "\nURL: " + str(data_selected_stage["url"])
              + "\nHas credentials: " + str(data_selected_stage["has_credentials"])
              + "\nStorage integration: " + str(data_selected_stage["storage_integration"])
              )

# Get the files on the choosen stage
data_list = db.run_query_dict(session, f'ls \'@{selected_stage}\'')

# Show the checkboxes
list_params_col1, list_params_col2 = tab_files.columns(2)
if list_params_col1.button("Refresh"):
    # clear the whole cache
    ut.clear_cache()

if selected_stage_type == "USER'S":
    show_worksheet_data = list_params_col2.checkbox('Hide worksheet_data* entries', value=True)

# Filter the dirlist if it is needed
data_list_filtered = []
if selected_stage_type == "USER'S":
    if show_worksheet_data:
        for d in data_list:
            if "worksheet_data/" not in d["name"]:
                data_list_filtered.append(d)
    else:
        data_list_filtered = data_list
else:
    data_list_filtered = data_list

# Creat the tight list format
data_list_tight = []
for d in data_list_filtered:
    dd = {}
    dd["File name"] = d["name"]
    dd["File size"] = ut.convert_size_byte(d["size"])
    dd["Last modified"] = datetime. strptime(d["last_modified"], '%a, %d %b %Y %H:%M:%S %Z').strftime("%Y-%m-%d %H:%M:%S")
    data_list_tight.append(dd)

# Show the list of the stage files
tab_files.write("Files on your stage:")
tab_files.dataframe(data_list_tight, use_container_width=True)

# -- Choose and Download a file
columns_manage_files = tab_files.columns(2)
if selected_stage_type == "EXTERNAL":
    columns_manage_files[0].info("Downloading or removing file is not available on external stages!")
else:
    form_manage_files = columns_manage_files[0].form("file_form", clear_on_submit=False)
    form_manage_files.write("Manage file:")

    option_dl_file = form_manage_files.selectbox(
            "Download a file:",
            [ d["name"] for d in data_list_filtered ],
            label_visibility = "collapsed",
            key="file",
        )
    columns_dlrm_files = form_manage_files.columns([1,2])
    submit = columns_dlrm_files[0].form_submit_button("Download file", on_click=download_from_stage)
    submit = columns_dlrm_files[1].form_submit_button("Remove file", on_click=remove_from_stage)
    submit_confirm = columns_dlrm_files[1].checkbox("Sure, remove it", key="remove_file_confirm", value=False)

# -- Upload a file
cont = columns_manage_files[1].container()
uploaded_file = cont.file_uploader("Upload file to this stage:", on_change=ut.clear_cache)
if uploaded_file is not None:
    upload_file_to_stage(uploaded_file)

# -- Integration tab
# Show the integration details
if selected_stage_type == "EXTERNAL":
    data_integration = db.run_query_dict(session, "show storage integrations like '{integration}'".format(integration=str(data_selected_stage["storage_integration"])))
    data_integration_desc = db.run_query_dict(session, "desc storage integration {integration}".format(integration=str(data_selected_stage["storage_integration"])))
    tab_integration.dataframe(data_integration)
    tab_integration.dataframe(data_integration_desc)
else:
    tab_integration.info("Not available on internal stages!")
