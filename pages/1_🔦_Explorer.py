import streamlit as st
from snowflake.connector import DictCursor

import common.sidebar as sb
import common.db as db
import common.utils as ut

from datetime import datetime

# -----------------------------------------------
# App starts here
st.set_page_config(page_title="ILSFAPP", layout="wide")
session = db.init_connection()
st.title('Stage explorer')
sb.info_panel()
if "remove_file_confirmed" not in st.session_state:
    st.session_state["remove_file_confirmed"] = False

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
    if st.session_state.get("remove_file_confirm"):
        st.session_state["remove_file_confirm"] = False
    st.cache_data.clear()
    st.experimental_rerun()

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

# Managing files
if selected_stage_type == "EXTERNAL":
    tab_files.info("Managing files is not available on external stages!")
else:
    # Choose and Download/Remove a file
    columns_manage_files = tab_files.columns(2)
    columns_manage_files[0].write("Manage file:")
    
    # Create the dropdown box with a special "Select a file..." entry first
    option_dl_file = columns_manage_files[0].selectbox(
            "Download a file:",
            ["Select a file..."] + [ d["name"] for d in data_list_filtered ],
            label_visibility = "collapsed",
            key="file",
        )
    
    # Show the buttons if only it does make sense
    if option_dl_file and option_dl_file != "Select a file...":
        columns_dlrm_files = columns_manage_files[0].columns([1,2])
        f, filename = db.download_from_stage(session, option_dl_file, selected_stage_type, selected_stage)
        columns_dlrm_files[0].download_button(
                            label="Download",
                            data=f,
                            file_name=filename,
                            key='dlbutton',
                        )
        print("dlbutton", st.session_state["dlbutton"])
        button_remove_file = columns_dlrm_files[1].button("Remove file", on_click=ut.clear_checkbox_remove_file_confirm)
        columns_dlrm_files[1].checkbox("Sure, remove it", key="remove_file_confirm", value=False)
        if button_remove_file:
            db.remove_from_stage(session, option_dl_file, selected_stage_type, selected_stage)

    # Upload a file
    cont = columns_manage_files[1].container()
    uploaded_file = cont.file_uploader("Upload new file to this stage:", on_change=ut.clear_cache)
    if uploaded_file is not None:
        db.upload_file_to_stage(session, uploaded_file, selected_stage)


# -- Integration tab
# Show the integration details
if selected_stage_type == "EXTERNAL":
    data_integration = db.run_query_dict(session, "show storage integrations like '{integration}'".format(integration=str(data_selected_stage["storage_integration"])))
    data_integration_desc = db.run_query_dict(session, "desc storage integration {integration}".format(integration=str(data_selected_stage["storage_integration"])))
    tab_integration.dataframe(data_integration)
    tab_integration.dataframe(data_integration_desc)
else:
    tab_integration.info("Not available on internal stages!")
