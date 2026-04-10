import streamlit as st
import os
from duckduckgo_search import DDGS
from datetime import datetime

st.set_page_config(page_title="Feynman Search", page_icon="🔍", layout="wide")

st.title("🔍 Feynman Search")
st.markdown("Buscador de investigación personal con citeo de fuentes")

query = st.text_input(
    "¿Qué quieres buscar?", placeholder="Escribe tu pregunta...", key="search_input"
)

if query:
    with st.spinner("Buscando..."):
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=10)

            st.success(f"Resultados para: **{query}**")

            for i, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"### {i}. {result.get('title', 'Sin título')}")
                    st.markdown(
                        f"📄 [{result.get('href', '#')}]({result.get('href', '#')})"
                    )
                    st.markdown(f"_{result.get('body', 'Sin descripción')}_")
                    st.divider()

        except Exception as e:
            st.error(f"Error en la búsqueda: {str(e)}")

with st.sidebar:
    st.header("⚙️ Configuración")
    st.info("""
    **Feynman Search**
    
    Powered by:
    - DuckDuckGo Search API
    - Streamlit
    
    Para usar Feynman CLI completo,
    instálalo localmente:
    `curl -fsSL https://feynman.is/install | bash`
    """)

    st.markdown("---")
    st.markdown(f"Última búsqueda: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
