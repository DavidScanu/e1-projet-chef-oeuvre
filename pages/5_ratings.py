import streamlit as st
from streamlit_star_rating import st_star_rating


if 'rating' not in st.session_state:
    st.session_state.rating = None

def on_click_rating(value):
    st.session_state.rating = {value}
    # print(st.session_state.rating)
    # st.write(f"on_click {value}")
    # st.write(type(st.session_state.rating))
    st.success(f"Merci pour votre évaluation ! {st.session_state['rating']}")

st.write(st.session_state.rating)

# Ratings                
if st.session_state.rating == None :
    st.markdown("""
    #### Rating
    Notez la détection afin de nous aider à améliorer notre modèle !
    """)
    stars = st_star_rating('Rating', 5, 3, 20, read_only=False, on_click=on_click_rating, customCSS="h3 {display: none;}")
    st.write(stars)