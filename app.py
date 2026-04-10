import streamlit as st
import os
from datetime import datetime
from config import SEARCH_ENGINES, DATE_FILTERS, CITATION_FORMATS
from search.duckduckgo_search import DuckDuckGoBackend
from search.arxiv_search import ArxivBackend
from search.semantic_scholar import SemanticScholarBackend
from history.search_history import SearchHistory
from export.pdf_generator import PDFReportGenerator
from export.citations import CitationFormatter
from utils.validators import is_valid_query, sanitize_query

# Page configuration
st.set_page_config(
    page_title="🔍 Feynman Search - Academic Research",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "search_history_manager" not in st.session_state:
    st.session_state.search_history_manager = SearchHistory()

if "last_results" not in st.session_state:
    st.session_state.last_results = None

if "last_query" not in st.session_state:
    st.session_state.last_query = None

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# Search backends
BACKENDS = {
    "web": DuckDuckGoBackend(),
    "arxiv": ArxivBackend(),
    "scholar": SemanticScholarBackend(),
}

# CSS styling
st.markdown(
    """
<style>
    .search-result {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .result-title {
        font-size: 18px;
        font-weight: bold;
        color: #1f1f1f;
    }
    .result-snippet {
        font-size: 14px;
        color: #555;
        margin-top: 5px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.title("🔍 Feynman Search")
st.markdown(
    "**Advanced Academic Research Engine** - Multi-source search with academic citations"
)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Search engine selection
    selected_engines = st.multiselect(
        "Select search engines:",
        options=list(SEARCH_ENGINES.values()),
        default=[SEARCH_ENGINES["web"]],
        help="Choose which search engines to use",
    )

    engine_keys = [k for k, v in SEARCH_ENGINES.items() if v in selected_engines]

    # Number of results
    max_results = st.slider(
        "Results per engine:", min_value=5, max_value=50, value=10, step=5
    )

    # Date filter
    date_filter = st.selectbox(
        "Date filter:",
        options=list(DATE_FILTERS.keys()),
        help="Filter results by publication date",
    )

    # PDF export settings
    st.subheader("📄 PDF Export Settings")
    citation_style = st.selectbox(
        "Citation format:",
        options=CITATION_FORMATS,
        help="Choose citation style for PDF export",
    )

    # History
    st.subheader("📚 Search History")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 View History"):
            st.session_state.show_history = not st.session_state.show_history

    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state.search_history_manager.clear_history()
            st.success("History cleared!")
            st.rerun()

    # Statistics
    stats = st.session_state.search_history_manager.get_stats()
    st.markdown(f"""
    **📊 Statistics:**
    - Total searches: **{stats["total"]}**
    - Engines used: {len(stats["engines"])}
    """)

# Main search interface
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "¿Qué quieres buscar?",
        placeholder="Escribe tu pregunta de investigación...",
        key="search_input",
        help="Enter your research query",
    )

with col2:
    search_button = st.button("🔍 Buscar", use_container_width=True)

# Execute search
if search_button and query:
    if not is_valid_query(query):
        st.error("Query must be between 2 and 500 characters.")
    else:
        query = sanitize_query(query)
        st.session_state.last_query = query

        all_results = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, engine_key in enumerate(engine_keys):
            try:
                backend = BACKENDS[engine_key]
                status_text.info(f"🔍 Searching {backend.get_name()}...")

                results = backend.search(query, max_results=max_results)
                all_results.extend(results)

                st.session_state.search_history_manager.add_search(
                    query=query, engine=backend.get_name(), results=results
                )

                progress_bar.progress((idx + 1) / len(engine_keys))

            except Exception as e:
                st.error(f"Error searching {backend.get_name()}: {str(e)}")

        status_text.empty()
        progress_bar.empty()
        st.session_state.last_results = all_results

        if all_results:
            st.success(
                f"✅ Found {len(all_results)} results from {len(engine_keys)} source(s)"
            )
        else:
            st.warning("No results found. Try a different query.")

# Display results
if st.session_state.last_results:
    st.subheader(f'📊 Results for: "{st.session_state.last_query}"')

    # Export options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Export as PDF"):
            with st.spinner("Generating PDF report..."):
                try:
                    pdf_gen = PDFReportGenerator(
                        title="Research Report - Feynman Search",
                        query=st.session_state.last_query,
                    )
                    pdf_bytes = pdf_gen.generate(
                        st.session_state.last_results, style=citation_style
                    ).getvalue()

                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

    with col2:
        if st.button("📋 Show Bibliography"):
            st.session_state.show_biblio = not st.session_state.get(
                "show_biblio", False
            )

    with col3:
        st.caption(f"Total Results: {len(st.session_state.last_results)}")

    # Bibliography
    if st.session_state.get("show_biblio"):
        st.subheader("Bibliography")
        bibliography = CitationFormatter.format_bibliography(
            st.session_state.last_results, citation_style
        )
        st.code(bibliography, language="text")

    # Display results
    st.subheader("Results")

    for i, result in enumerate(st.session_state.last_results, 1):
        with st.container():
            st.markdown(f"### {i}. {result.title}")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Source:** {result.source}")

                if result.date:
                    st.markdown(f"📅 {result.date.strftime('%Y-%m-%d')}")

                if result.authors:
                    authors_str = ", ".join(result.authors[:3])
                    if len(result.authors) > 3:
                        authors_str += ", et al."
                    st.markdown(f"👥 {authors_str}")

                st.markdown(f"_{result.snippet}_")
                st.markdown(f"🔗 [View Paper]({result.url})")

            with col1:
                if st.button("Copy Citation", key=f"cite_{i}"):
                    citation = (
                        CitationFormatter.format_apa(result)
                        if citation_style == "APA"
                        else CitationFormatter.format_ieee(result)
                    )
                    st.code(citation, language="text")

            st.divider()

# Show history if requested
if st.session_state.show_history:
    st.subheader("📚 Search History")

    history = st.session_state.search_history_manager.get_history(limit=20)

    if history:
        for entry in history:
            with st.expander(
                f"🔍 {entry['query']} - {entry['engine']} ({entry['timestamp'][:10]})"
            ):
                st.markdown(f"**Engine:** {entry['engine']}")
                st.markdown(f"**Results:** {entry['results_count']}")
                st.markdown(f"**Time:** {entry['timestamp']}")
    else:
        st.info("No search history yet.")
