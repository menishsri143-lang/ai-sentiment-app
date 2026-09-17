import streamlit as st
import streamlit_authenticator as stauth
from textblob import TextBlob

# 1. Credentials for Authentication
hashed_admin = stauth.Hasher.hash('admin123')
hashed_demo = stauth.Hasher.hash('demo123')

credentials = {
    'usernames': {
        'admin': {'name': 'Admin User', 'password': hashed_admin, 'email': 'admin@gmail.com'},
        'demo': {'name': 'Demo User', 'password': hashed_demo, 'email': 'demo@gmail.com'}
    }
}

# 2. Login Authenticator
authenticator = stauth.Authenticate(credentials, 'my_cookie_name', 'my_signature_key', 30)
authenticator.login(location='main')

authentication_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.title("API Key-illadha AI Sentiment Analyzer")
    st.write(f"Welcome, **{name}**!")

    prompt = st.text_area("Enter your sentence/feedback in English:")

    if st.button("Analyze Sentiment"):
        if prompt.strip():
            # TextBlob AI Analysis (No API Key Required)
            blob = TextBlob(prompt)
            polarity = blob.sentiment.polarity

            if polarity > 0:
                st.success("Positive Sentiment 😊 (நேர்மறையான கருத்து)")
            elif polarity < 0:
                st.error("Negative Sentiment 😡 (எதிர்மறையான கருத்து)")
            else:
                st.info("Neutral Sentiment 😐 (நடுநிலையான கருத்து)")
        else:
            st.warning("Please enter text first!")

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")