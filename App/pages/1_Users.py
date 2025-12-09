import json
import pandas as pd
import streamlit as st

css  = '''
<style>
    .st-key-title_text {
        text-align: center;
    }
    .st-key-next_page_button{
        margin-left: auto;
    }
</style>
'''

with open('user_id_to_idx.json', 'r') as json_file:
    user_id_to_idx = json.load(json_file)

with open('user_rated_items.json', 'r') as json_file:
     user_rated_items = dict(json.load(json_file))

with open('user_id_to_name.json', 'r') as json_file:
     user_id_to_name = dict(json.load(json_file))

df = pd.DataFrame({
    'User ID': user_id_to_name.keys(),
    'User Name': user_id_to_name.values(),
    'User Index': [user_id_to_idx.get(uid) for uid in user_id_to_name.keys()],
    'Number of Reviewed Products': [len(user_rated_items[str(user_id_to_idx[uid])]) for uid in user_id_to_name.keys()]
})
df = df.set_index('User Index').sort_values(by=['User Index'])
pages = len(df) // 10 if len(df)%10 == 0 else len(df) // 10 + 1

if 'current_page' not in st.session_state:
        st.session_state.current_page =  1
if 'page_text' not in st.session_state:
        st.session_state.page_text =  f'{st.session_state.current_page} of {pages}'

def ChangePage(direction):
    global pages, df
    addition = 1
    if direction == 'previous':
        addition = -1
    if (addition == 1 and st.session_state.current_page < pages) or (addition == -1 and st.session_state.current_page > 1):
        st.session_state.current_page += addition
        st.session_state.page_text =  f'{st.session_state.current_page} of {pages}'


st.set_page_config(page_title='Product Recommendation', page_icon='🎁', layout='wide')

st.markdown(css, unsafe_allow_html=True)

with st.container(key="title_text"):
    st.title("Users")

with st.container():
    st.dataframe(df[(st.session_state.current_page-1)*10:st.session_state.current_page*10])
    left_column, center_column, right_column = st.columns(3) #The () is the size
    with left_column:
        st.button('Previous Page', key='previous_page_button', on_click=ChangePage, args=('previous',))
    with center_column:
        st.markdown(f"<p style='text-align: center;'>{st.session_state.page_text}</p>", unsafe_allow_html=True)
    with right_column:
        st.button('Next Page', key='next_page_button', on_click=ChangePage, args=('next',))





