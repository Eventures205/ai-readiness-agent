import streamlit as st
import requests
import json
import uuid
from datetime import datetime

st.set_page_config(page_title="AI Readiness Assessment", layout="centered")

st.image("streamlit_logo_large.png", width=300)
st.markdown("<h3 style='text-align: center;'>Capital E Ventures</h3>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'><img src='streamlit_logo_large.png' width='300'></div>", unsafe_allow_html=True)

st.title("🧠 AI Readiness Assessment")
st.write("Answer a few quick questions to see how ready your organization is to scale AI.")

form = st.form("readiness_form")

with form:
    company = st.text_input("Company Name")

    st.subheader("📊 Data Foundations")
    has_data_catalog = st.checkbox("Do you have a data catalog?")
    quality_automation = st.checkbox("Do you use automated data quality checks?")
    integrated_sources = st.checkbox("Are your data sources integrated?")
    no_data_silos = st.checkbox("Is your data free from silos?")

    st.subheader("⚙️ AI Infrastructure")
    model_registry = st.checkbox("Do you use a model registry?")
    pipeline_orchestration = st.checkbox("Do you orchestrate pipelines (e.g., Airflow, Workflows)?")
    cloud_platforms = st.checkbox("Do you use cloud platforms (e.g., AWS, GCP, Azure)?")
    real_time_deployment = st.checkbox("Do you deploy AI in real-time systems?")

    st.subheader("🚀 Use Case Maturity")
    live_models = st.slider("How many live AI models do you currently use?", 0, 10, 1)
    pocs = st.slider("How many AI/automation PoCs have you completed?", 0, 10, 1)
    roi_tracking = st.checkbox("Do you track ROI for AI initiatives?")
    user_adoption = st.checkbox("Is AI actively used by business users?")

    st.subheader("🔐 Governance & Security")
    rbac = st.checkbox("Do you use role-based access controls?")
    audit_logs = st.checkbox("Are system or data access logs maintained?")
    model_explainability = st.checkbox("Do you ensure model explainability (e.g., SHAP, LIME)?")
    bias_checks = st.checkbox("Do you perform bias/fairness audits?")

    st.subheader("🏢 Organizational Culture")
    exec_support = st.checkbox("Do your executives support AI initiatives?")
    cross_functional_teams = st.checkbox("Are AI efforts cross-functional?")
    training_programs = st.checkbox("Do you have AI/data training for teams?")
    ai_champion = st.checkbox("Is there an internal AI 'champion' or lead?")

    submitted = st.form_submit_button("Run Assessment")

if submitted:
    with st.spinner("Running assessment..."):
        client_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        # ✅ FIX: Add company_name to inputs as well as top-level
        inputs = {
            "company_name": company,
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
            "ai_champion": ai_champion
        }

        payload = {
            "company_name": company,
            "client_id": client_id,
            "timestamp": timestamp,
            "inputs": inputs
        }

        try:
            api_url = st.secrets["api_url"]
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                result = response.json()
                st.success("Assessment Complete!")

                st.markdown("### 📈 Readiness Score Breakdown:")
                for k, v in result["scores"].items():
                    st.write(f"**{k.replace('_', ' ').title()}**: {v}/20")

                st.markdown(f"**✅ Total Score:** {sum(result['scores'].values())}/100")

                st.markdown("### 🧠 AI Readiness Commentary:")
                for section, comment in result["commentary"].items():
                    st.markdown(f"**{section.replace('_', ' ').title()}**: {comment}")

            else:
                st.error("Failed to get a valid response. Please check your Lambda API or try again later.")

        except Exception as e:
            st.error(f"Error: {e}")
