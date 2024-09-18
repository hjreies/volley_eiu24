import streamlit as st



st.set_page_config(layout="wide")


def creds_entered():
    if st.session_state["user"].strip() == "admi" and st.session_state["password"].strip() =="admi":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if not st.session_state["password"]:
            st.warning("Please enter password")
        elif not st.session_state["user"]:
            st.warning("Please enter username")
        else:
            st.error("Invalid User/Password")
        
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Username :", value="", key="user", on_change=creds_entered)
        st.text_input(label="Password :", value="", key="password", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Username :", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password :", value="", key="password", on_change=creds_entered)
            return False

if authenticate_user():
        # page setup__________________________
        main_page = st.Page( 
            page="pages/EIU.py",
            title="EIU 2024 Season",
            default=True,
        )

        game1_page = st.Page(
            page="pages/eiu24_match1.py",
            title="non-conference 1",
        )

        game2_page = st.Page(
            page="pages/eiu24_match2.py",
            title="non-conference 2",
        )
        
        game3_page = st.Page(
            page="pages/eiu24_match3.py",
            title="non-conference 3",
        )

        game4_page = st.Page(
            page="pages/eiu24_match4.py",
            title="non-conference 4",
        )

        game5_page = st.Page(
            page="pages/eiu24_match5.py",
            title="non-conference 5",
        )
        
        game6_page = st.Page(
            page="pages/eiu24_match6.py",
            title="non-conference 6",
        )
        
        game7_page = st.Page(
            page="pages/eiu24_match7.py",
            title="non-conference 7",
        )
        
        # navigation setup [without sections]
        pg = st.navigation([main_page, game1_page, game2_page, game3_page, game4_page, game5_page, game6_page, game7_page ])
                        

        st.sidebar.text("by Hector Jose Reyes")


        # run navigation
        pg.run()
