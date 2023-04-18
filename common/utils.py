import streamlit as st
import math


# Convert byte to KB, MB,...
def convert_size_byte(size_bytes):
   if size_bytes == 0:
       return "0 B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


# Clear the confirmation checkbox
def clear_checkbox_remove_file_confirm():
    if st.session_state.get("remove_file_confirm"):
        st.session_state["remove_file_confirm"] = False
        st.session_state["remove_file_confirmed"] = True


# Clear the cache
def clear_cache():
    st.cache_data.clear()
