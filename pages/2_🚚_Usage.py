import streamlit as st

import common.sidebar as sb
import common.db as db
import common.utils as ut

from datetime import datetime

# -----------------------------------------------
# App starts here
st.set_page_config(page_title="ILSFAPP", layout="wide")
session = db.init_connection()
st.title('Stage usage')
sb.info_panel()

# Get all the stages under this account
data_stages = db.run_query_dict(session, 'show stages in account')

# Show the filters
filter_col1, filter_col2 = st.columns([1,4])
usage_selected_stage_type = filter_col1.selectbox(
        "Choose a stage type",
        ["USER'S", "INTERNAL"],
        label_visibility = "collapsed",
    )

# Get the files, iterate trhough the stages
all_stages_list = []
internal_stages_usage = []
if usage_selected_stage_type == "USER'S":
    list_items = db.run_query_dict_error(session, 'ls @~/')
    if list_items:
        stage_usage = {}
        stage_usage["stage_name"] = "~"
        stage_usage["size"] = 0
        for item in list_items:
            item["stage_name"] = "~"
            all_stages_list.append(item)
            stage_usage["size"] += item["size"]

        internal_stages_usage.append(stage_usage)

elif usage_selected_stage_type == "INTERNAL":
    for stage in data_stages:
        # if stage["type"] in ["~","INTERNAL"]:
        if usage_selected_stage_type == stage["type"]:
            sn = stage["database_name"] + "." + stage["schema_name"] + "." + '"'+stage["name"]+'"' if stage["name"].find(" ") else stage["name"]
            # st.write(sn)
            list_items = db.run_query_dict_error(session, f'ls \'@{sn}\'')
            stage_usage = {}
            stage_usage["stage_name"] = sn
            stage_usage["size"] = 0
            if list_items:
                for item in list_items:
                    item["stage_name"] = sn
                    all_stages_list.append(item)
                    stage_usage["size"] += item["size"]
                
                internal_stages_usage.append(stage_usage)

# Sort by size desc order
all_stages_list_sorted = sorted(all_stages_list, key=lambda d: d['size'], reverse=True)
internal_stages_usage_sorted = sorted(internal_stages_usage, key=lambda d: d['size'], reverse=True)

# Create the tight list format
all_stages_list_tight = []
for d in all_stages_list_sorted:
    dd = {}
    dd["Stage name"] = d["stage_name"]
    dd["File name"] = d["name"]
    dd["File size"] = ut.convert_size_byte(d["size"])
    dd["Last modified"] = datetime. strptime(d["last_modified"], '%a, %d %b %Y %H:%M:%S %Z').strftime("%Y-%m-%d %H:%M:%S")
    all_stages_list_tight.append(dd)

internal_stages_usage_tight = []
for d in internal_stages_usage_sorted:
    dd = {}
    dd["Stage name"] = d["stage_name"]
    dd["Stage size"] = ut.convert_size_byte(d["size"])
    internal_stages_usage_tight.append(dd)

# Show the overall usage
st.write("Stages:")
st.dataframe(internal_stages_usage_tight, use_container_width=True)
# Show the dataframe
st.write("Files across your internal stages:")
st.dataframe(all_stages_list_tight, use_container_width=True)
