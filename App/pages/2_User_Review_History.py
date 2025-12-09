import json
import pandas as pd
import streamlit as st

css  = '''
<style>
    .st-key-title_text {
        text-align: center;
    }
</style>
'''

st.set_page_config(page_title='Product Recommendation', page_icon='🎁', layout='wide')

st.markdown(css, unsafe_allow_html=True)

with st.container(key="title_text"):
    st.title("Review History")

if 'history_id' not in st.session_state:
    st.session_state.history_id = ''

if 'history_name' not in st.session_state:
    st.session_state.history_name = ''
    

def LoadData():
    with open('user_id_to_idx.json', 'r') as json_file:
        user_id_to_idx = json.load(json_file)
    
    with open('idx_to_title.json', 'r') as json_file:
        idx_to_title = dict(json.load(json_file))
    
    with open('user_rated_items.json', 'r') as json_file:
         user_rated_items = dict(json.load(json_file))
    
    with open('user_id_to_name.json', 'r') as json_file:
         user_id_to_name = dict(json.load(json_file))

    return user_id_to_idx, idx_to_title, user_rated_items, user_id_to_name

def SearchHistory(id_input, name_input):
    st.session_state.history_id = id_input
    st.session_state.history_name = name_input.strip().lower()


with st.container():
    left_column, right_column = st.columns(2) #The () is the size
    with left_column:
        id_input = st.text_input('Enter User ID:')
    with right_column:
        name_input = st.text_input('Or Enter User Name:')

st.button('Submit', on_click=SearchHistory, args=(id_input,name_input ))



if (st.session_state.history_id == '' and st.session_state.history_name == ''):
    df = pd.DataFrame({'Titles Reviewed': []})
    st.dataframe(df)
else:
    try:
        user_id_to_idx, idx_to_title, user_rated_items, user_id_to_name = LoadData()
        if st.session_state.history_id != '' and st.session_state.history_id in user_id_to_idx.keys():
            user_id = user_id_to_idx[st.session_state.history_id]
        else:
            key = [key for key, value in user_id_to_name.items() if value.strip().lower() == st.session_state.history_name]
            user_id = user_id_to_idx[key[0]]
        items = user_rated_items[str(user_id)]
        df = pd.DataFrame({'Titles Reviewed': [idx_to_title[str(idx)] for idx in items]})
        st.dataframe(df)
    except:
        df = pd.DataFrame({'Titles Reviewed': []})
        st.dataframe(df)
    st.session_state.history_id = ''
    st.session_state.history_name = ''
    
