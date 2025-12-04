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

st.set_page_config(page_title='Movie Recommendation', page_icon='🎁', layout='wide')

st.markdown(css, unsafe_allow_html=True)

with st.container(key="title_text"):
    st.title("Review History")

if 'history_id' not in st.session_state:
    st.session_state.history_id = ''
    

def LoadData():
    with open('./user_id_to_idx.json', 'r') as json_file:
        user_id_to_idx = json.load(json_file)
    
    with open('idx_to_title.json', 'r') as json_file:
        idx_to_title = dict(json.load(json_file))
    
    with open('user_rated_items.json', 'r') as json_file:
         user_rated_items = dict(json.load(json_file))
    
    with open('user_id_to_name.json', 'r') as json_file:
         user_id_to_name = dict(json.load(json_file))

    return user_id_to_idx, idx_to_title, user_rated_items, user_id_to_name

def SearchHistory(id_input):
    st.session_state.history_id = id_input


id_input = st.text_input('Enter User ID:')

st.button('Submit', on_click=SearchHistory, args=(id_input, ))



if st.session_state.history_id == '':
    df = pd.DataFrame({'Titles Reviewed': []})
    st.dataframe(df)
else:
    user_id_to_idx, idx_to_title, user_rated_items, user_id_to_name = LoadData()
    user_id = user_id_to_idx[st.session_state.history_id]
    items = user_rated_items[str(user_id)]
    df = pd.DataFrame({'Titles Reviewed': [idx_to_title[str(idx)] for idx in items]})
    st.dataframe(df)
    st.session_state.history_id = ''
    

    







