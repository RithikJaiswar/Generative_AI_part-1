import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

# ------------------ MODEL ------------------

model = ChatMistralAI(model="mistral-small-2506",api_key=st.secrets["bvnlYoDywX0r2lAyItV5x8UObpKuUGd0"])

# ------------------ SCHEMA ------------------

class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

# ------------------ PROMPT ------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract movie information from the paragraph.

{format_instructions}
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])

# ------------------ PAGE ------------------

st.set_page_config(
    page_title="Movie Extractor",
    page_icon="🎬",
    layout="wide"
)

# ------------------ STYLING ------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:700;
    margin-bottom:20px;
}

.result-card{
    padding:15px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.15);
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------

st.sidebar.title("ℹ️ About")

st.sidebar.info(
    """
This app extracts structured movie information using:

• LangChain
• Mistral AI
• Pydantic Schema

The sidebar also displays the machine-friendly JSON output.
"""
)

# ------------------ HEADER ------------------

st.markdown(
    '<div class="main-title">🎬 Movie Information Extractor</div>',
    unsafe_allow_html=True
)

# ------------------ INPUT ------------------

paragraph = st.text_area(
    "Movie Description",
    height=250,
    placeholder="Paste movie description here..."
)

# ------------------ BUTTON ------------------

if st.button("🚀 Extract Information", use_container_width=True):

    if not paragraph.strip():
        st.warning("Please enter a movie description.")
        st.stop()

    chain = prompt | model | parser

    with st.spinner("Analyzing movie information..."):

        result = chain.invoke({
            "paragraph": paragraph,
            "format_instructions": parser.get_format_instructions()
        })

    st.balloons()

    # ---------- MAIN OUTPUT ----------

    st.header(result.title)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Release Year", result.release_year)

    with col2:
        st.metric("Director", result.director)

    with col3:
        st.metric("Rating", result.rating)

    st.subheader("🎭 Genres")

    if result.genre:
        st.write(", ".join(result.genre))

    st.subheader("🎬 Cast")

    for actor in result.cast:
        st.write(f"• {actor}")

    st.subheader("📝 Summary")
    st.info(result.summary)

    # ---------- SIDEBAR JSON ----------

    st.sidebar.subheader("Machine-Friendly JSON")

    st.sidebar.json(
        result.model_dump()
    )
