import json
import torch
import pandas as pd
import streamlit as st

class CF_Model(torch.nn.Module):
    def __init__(self, num_users, num_items, latent_dim=32):
        super(CF_Model, self).__init__()
        self.user_embedding = torch.nn.Embedding(num_users, latent_dim)
        self.item_embedding = torch.nn.Embedding(num_items, latent_dim)
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(latent_dim * 2, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 1)
        )

    def forward(self, user, item):
        user_vec = self.user_embedding(user)
        item_vec = self.item_embedding(item)
        x = torch.cat([user_vec, item_vec], dim=-1)
        return self.fc(x).squeeze()

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
    st.title("Recommend")

if 'user_id' not in st.session_state:
    st.session_state.user_id = ''

if 'user_name' not in st.session_state:
    st.session_state.user_name = ''

if 'num_recommend' not in st.session_state:
    st.session_state.num_recommend = ''

if 'results' not in st.session_state:
    st.session_state.results = False

if 'cached_results' not in st.session_state:
    st.session_state.cached_results = False

if 'recon_cache' not in st.session_state:
    st.session_state.recon_cache = ()
    

def SwitchMode():
    if (not st.session_state.results) and (st.session_state.num_recommend == '' or (st.session_state.user_id == '' and st.session_state.user_name == '')):
        return
    st.session_state.results = not st.session_state.results
    st.session_state.cached_results = False

def SetUpSearch():
    st.session_state.results = False
    st.session_state.cached_results = False
    with st.container():
        left_column, right_column = st.columns(2) #The () is the size
        with left_column:
            st.text_input('Enter User ID:', key="user_id")
        with right_column:
            st.text_input('Or Enter User Name:', key="user_name")
    st.text_input('Enter Number of Recommendations:', key='num_recommend')
    
    st.button('Submit', on_click=SwitchMode)

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

def LoadRecommendations():
    N = int(st.session_state.num_recommend)
    user_id = st.session_state.user_id
    user_name = st.session_state.user_name.strip().lower()
    
    user_id_to_idx, idx_to_title, user_rated_items, user_id_to_name = LoadData()
    
    if user_id != '' and user_id in user_id_to_idx.keys():
        user_idx = user_id_to_idx[user_id]
    else:
        key = [key for key, value in user_id_to_name.items() if value.strip().lower() == user_name]
        user_id = key[0]
        user_idx = user_id_to_idx[user_id]
        
    user_name = user_id_to_name[user_id]
    num_users = len(user_id_to_idx.keys())
    num_items = len(idx_to_title.keys())

    model = CF_Model(num_users, num_items)
    state_dict = torch.load('./model_weights.pth')
    model.load_state_dict(state_dict)

    model.eval()
    if user_idx is None: # Catch issues here is user_id entered is not found, then print 'Uers ID not found.'
        print(f"User ID {user_id} not found.")
        return

    rated_items = user_rated_items.get(str(user_idx), set())
    scores = []

    for item_idx in range(num_items):
        if item_idx in rated_items:
            continue  # Skip items already rated

        with torch.no_grad():
            score = model(torch.tensor(user_idx), torch.tensor(item_idx)).item()
        scores.append((item_idx, score))

    top_items = sorted(scores, key=lambda x: x[1], reverse=True)[:N]

    top_items = pd.DataFrame({
        'Recommendations': [idx_to_title.get(str(item[0]), 'Unknown Item') for item in top_items],
        'Scores': [round(item[1], 2) for item in top_items]
    })
    
    st.session_state.recon_cache = (top_items, user_name, N)
    return top_items, user_name, N, user_id
    

placeholder = st.empty()

if st.session_state.results:
    if st.session_state.cached_results and len(st.session_state.recon_cache) == 4:
        top_items, user_name, N, user_id = st.session_state.recon_cache
        st.write(f'Top {N} recommendations for user {user_name}, ID: {user_id}')
        st.dataframe(top_items)
        st.button('Search', on_click=SwitchMode)
    else:
        try:
            top_items, user_name, N, user_id = LoadRecommendations()
            st.session_state.cached_results = True
            st.write(f'Top {N} recommendations for user {user_name}, ID: {user_id}')
            st.dataframe(top_items)
            st.button('Search', on_click=SwitchMode)
        except:
            SetUpSearch()
else:
    SetUpSearch()
