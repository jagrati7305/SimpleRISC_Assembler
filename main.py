import streamlit as st

st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');

    /* Apply font to app text */
    .stApp, h1, h2, h3, h4, h5, h6, p, span, label, div {
        font-family: 'JetBrains Mono', monospace;
    }

    /* DO NOT override icon fonts */
    .material-icons {
        font-family: 'Material Icons' !important;
    }

    div.stButton > button:first-child{
                background-color : #ffffff;
                color: #181818;
                border-radius: 8px;
                width: 100%;
                height:3em;
                font-size:16px;
                }

    div.stButton > button:hover{
                background-color : #0D0D0D;
                color: #ffffff; 
                border: 2px solid white;           
                }  

    .team-name{
                background-color: #0D0D0D;
                color: #646464;
                padding: 16px;
                border-radius: 8px;
                font-size: 100%;   
                border:2px #646464 solid;       
                }
    </style>
            """,unsafe_allow_html=True)
# --- SIDEBAR --- #
with st.sidebar:
    st.markdown(
    "<h1 style='color:white; font-size:48px; font-family:\"JetBrains Mono\";text-align:center;'>TinyRISC</h1>",
    unsafe_allow_html=True
    )
    st.markdown(
    "<h1 style='color:#6AD475; font-size:32px; font-family:\"JetBrains Mono\";line-height:0.7;text-align:center;'>Assembler</h1>",
    unsafe_allow_html=True
    )
    st.markdown("---")

    # --- SESSION STATE --- #
    if "page" not in st.session_state:
        st.session_state.page = "main"

    # --- NAV BUTTONS --- #
    if st.button("Assembler",width="stretch",icon=":material/code:"):
          st.session_state.page = "main"

    if st.button("Explanation Page",width="stretch",icon=":material/speaker_notes:"):
          st.session_state.page = "explanation"
    
    st.link_button("View Source Code","https://github.com/jagrati7305/SimpleRISC_Assembler",width="stretch",icon=":material/link_2:")
        
    st.markdown("""
    <div class = "team-name">
    Team : </br>
    Jagrati (2401EC56)</br>
    Pragya (2401EC63)</br>
    Krittika (2402VL02)</br>
    </div>
    """,unsafe_allow_html=True)

    # --- PAGE RENDER --- #
if st.session_state.page == "main":
        exec(open("views/main_page.py", encoding="utf-8").read())
else:
        exec(open("views/explanation_page.py", encoding="utf-8").read())