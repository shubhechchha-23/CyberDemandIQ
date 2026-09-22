import streamlit as st

st.set_page_config(
    page_title="CyberDemandIQ",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}

.hero {
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #263244;
    margin-bottom: 25px;
}

.hero h1 {
    margin: 0 0 6px 0;
    font-size: 2.2rem;
}

.hero p {
    color: #94a3b8;
    margin: 0;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)


pages = {
    "📊 Overview": "modules.overview",
    "🚨 Threat Intelligence": "modules.threats",
    "🤖 AI Detection": "modules.ai_detection",
    "🔎 Network Investigation": "modules.flows",
    "⚠️ Risk Analytics": "modules.risk",
    "📈 Security Demand": "modules.demand",
    "🧠 Response Intelligence": "modules.response",
    "🧪 ML Model Monitoring": "modules.model_monitoring",
    "🗄️ Database Explorer": "modules.database"
}


with st.sidebar:

    st.markdown("## 🛡️ CyberDemandIQ")

    st.caption(
        "Cybersecurity Intelligence Platform"
    )

    st.divider()

    selected = st.radio(
        "SECURITY OPERATIONS",
        list(pages.keys())
    )

    st.divider()

    st.markdown("### SYSTEM STATUS")

    st.success("API")
    st.success("PostgreSQL")
    st.success("XGBoost")

    st.divider()

    st.caption("CyberDemandIQ v1.0")


st.markdown(
    """
    <div class="hero">
        <h1>🛡️ CyberDemandIQ</h1>
        <p>
            AI-Powered Cybersecurity Detection,
            Risk Intelligence & Security Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


try:

    module = __import__(
        pages[selected],
        fromlist=["show"]
    )

    module.show()

except Exception as e:

    st.error(
        "Unable to load this dashboard module."
    )

    st.code(
        str(e),
        language="text"
    )