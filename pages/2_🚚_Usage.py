import streamlit as st
import snowflake.connector

import common.sidebar as sb

from datetime import datetime
import math

# -----------------------------------------------
# Helper functions

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )


# Convert byte to KB, MB,...
def convert_size_byte(size_bytes):
   if size_bytes == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


# Run a sql query and return a dict
@st.cache_data(ttl=3600)
def run_query_dict(query):
    with session.cursor(snowflake.connector.DictCursor) as cur:
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
def run_query_dict_error(query):
    with session.cursor(snowflake.connector.DictCursor) as cur:
        try:
            cur.execute(query)
            return cur.fetchall()
        except snowflake.connector.errors.ProgrammingError as e:
            pass
        finally:
            cur.close()


# -----------------------------------------------
# App starts here
st.set_page_config(page_title="ILSFAPP", layout="wide")
session = init_connection()
st.title('Stage usage')
sb.info_panel()

# Get all the stages under this account
data_stages = run_query_dict('show stages in account')

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
    list_items = run_query_dict_error('ls @~/')
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
            list_items = run_query_dict_error(f'ls \'@{sn}\'')
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
    dd["File size"] = convert_size_byte(d["size"])
    dd["Last modified"] = datetime. strptime(d["last_modified"], '%a, %d %b %Y %H:%M:%S %Z').strftime("%Y-%m-%d %H:%M:%S")
    all_stages_list_tight.append(dd)

internal_stages_usage_tight = []
for d in internal_stages_usage_sorted:
    dd = {}
    dd["Stage name"] = d["stage_name"]
    dd["Stage size"] = convert_size_byte(d["size"])
    internal_stages_usage_tight.append(dd)

# Show the overall usage
st.write("Stages:")
st.dataframe(internal_stages_usage_tight, use_container_width=True)
# Show the dataframe
st.write("Files across your internal stages:")
st.dataframe(all_stages_list_tight, use_container_width=True)
