import streamlit as st
from streamlit_star_rating import st_star_rating
import uuid


def on_click_rating(**on_click_kwargs_dict):
    # st.session_state['rating'] = value
    st.session_state['dr_job_id'] = on_click_kwargs_dict['dr_job_id']

st.write(st.session_state)

placeholder = st.empty()

on_click_kwargs_dict = {
    "dr_job_id" : uuid.uuid4(),
    "param2" : "Another param!"
}

with placeholder.container():
    # st.markdown("""
    # #### Rating
    # Notez la détection afin de nous aider à améliorer notre modèle !
    # """)
    # stars = st_star_rating('Rating', 5, 3, 20, read_only=False, on_click=on_click_rating, customCSS="h3 {display: none;}")
    # stars = st_star_rating("Please rate you experience", 5, 3, 20, key="rating_widget",  on_click=on_click_rating, on_click_kwargs=on_click_kwargs_dict)
    stars = st.slider('Vote', 0, 5, 3, step=1, key="rating_widget", on_change=on_click_rating, kwargs=on_click_kwargs_dict)
    if st.button('Submit'):
        with placeholder.container():
            st.success(f"Rating is : {st.session_state.rating_widget}")


# if isinstance(st.session_state['rating'], int) :
#     with placeholder:
#         st.success(f"Rating is : {st.session_state.rating}")
    
# if st.session_state['dr_job_id'] is not None :
#     with placeholder:
#         st.success(f"Rating is : {st.session_state.rating_widget}")  

st.write(st.session_state)

# if st.session_state.rating is None:
#     if st.button('Submit'):
#         st.session_state['rating'] = stars
# else :
#     with placeholder.container():
#         st.success(f"Rating is : {st.session_state.rating}")

