import pickle
from pathlib import Path

import streamlit_authenticator as stauth


names = ["admi", "manolo"]
usernames = ["admi", "manoloeiu"]
passwords = ["admi", "eiu2024!"]

hashed_passwords = stauth.Hasher(passwords).generate()



