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
    st.title("Product Recommendation System")

st.write('The purpose of this project is to build and experiment with a fully functioning product recommender system. Recommender systems can have powerful effects on how companies improve sales, offer customers better options and improve customer experience.  It’s a common feature of the online shopping experience at present. The purpose of this is both to build a functional product recommender application, and also to demonstrate best practices when building a product recommender system using Natural Language processing and machine learning.')


    
