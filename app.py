import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="AI Readiness Assessment", layout="centered")

st.image("logo.png", width=300)
st.title("AI Readiness Assessment")

st.markdown("Please complete the following questions to assess your organization's AI readiness.")

with st.form("readiness_form"):
    # DATA FOUNDATIONS
    has_data_catalog = st.checkbox("We use a data catalog")
    quality_automation = st.checkbox("We have data quality automation")
    integrated_sources = st.checkbox("Our data is integrated across systems")
    no_data_silos = st.checkbox("We do not have data silos")

    # AI INFRASTRUCTURE
    model_registry = st.checkbox("We use a model registry")
    pipeline_orchestration = st.checkbox("We use ML pipeline orchestration")
    cloud_platforms = st.checkbox("We use cloud platforms for AI/ML")
    real_time_deployment = st.checkbox("We support real-time AI deployments")

    # USE CASE MATURITY
    live_models = st.slider("How many AI models are currently in production?", 0, 10, 0)
    pocs = st.slider("How many AI/ML proof-of-concepts (PoCs) have you run?", 0, 10, 0)
    roi_tracking = st.checkbox("We track ROI on AI initiatives")
    user_adoption = st.checkbox("Our users regularly interact with AI tools")

    # GOVERNANCE / SECURITY
    rbac = st.checkbox("We use role-based access control (RBAC)")
    audit_logs = st.checkbox("We maintain audit logs for AI usage")
    model_explainability = st.checkbox("Our models are explainable")
    bias_checks = st.checkbox("We check AI systems for bias")

    # ORG CULTURE
    exec_support = st.checkbox("We have strong executive support for AI")
    cross_functional_teams = st.checkbox("We have cross-functional AI teams")
    training_programs = st.checkbox("We provide AI training programs")
    ai_champion = st.checkbox("We have an internal AI champion or leader")

    submitted = st.form_submit_button("Run Assessment")

if submitted:
    st.info("Submitting assessment to Lambda...")

    api_url = st.secrets["api_url"]  # should be set in .streamlit/secrets.toml

    payload = {
        "has_data_catalog": has_data_catalog,
        "quality_automation": quality_automation,
        "integrated_sources": integrated_sources,
        "no_data_silos": no_data_silos,
        "model_registry": model_registry,
        "pipeline_orchestration": pipeline_orchestration,
        "cloud_platforms": cloud_platforms,
        "real_time_deployment": real_time_deployment,
        "live_models": live_models,
        "pocs": pocs,
        "roi_tracking": roi_tracking,
        "user_adoption": user_adoption,
        "rbac": rbac,
        "audit_logs": audit_logs,
        "model_explainability": model_explainability,
        "bias_checks": bias_checks,
        "exec_support": exec_support,
        "cross_functional_teams": cross_functional_teams,
        "training_programs": training_programs,
        "ai_champion": ai_champion,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()

        st.success("Assessment Complete!")

        scores = result.get("scores", {})
        commentary = result.get("commentary", {})

        st.markdown("### 📊 Readiness Score Breakdown:")

        def show_score(label, key):
            st.markdown(f"**{label}: {scores.get(key, 0)}/20**")
            st.caption(commentary.get(key, ""))

        show_score("Data Foundations", "data_foundations")
        show_score("Ai Infrastructure", "ai_infrastructure")
        show_score("Use Case Maturity", "use_case_maturity")
        show_score("Governance Security", "governance_security")
        show_score("Org Culture", "org_culture")

        total = sum(scores.values())
        st.markdown(f"✅ **Total Score: {total}/100**")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
