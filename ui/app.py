"""CarePath AI Interactive Streamlit UI Dashboard."""
import streamlit as st
import requests
import base64
from PIL import Image
import io

# Configure Page Layout & Modern Medical Design Tokens
st.set_page_config(
    page_title="CarePath AI | Medical Intelligence Platform",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .badge-urgent {
        background-color: #EF4444;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .badge-routine {
        background-color: #3B82F6;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .disclaimer-box {
        background-color: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        color: #991B1B;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = "http://127.0.0.1:8000/api/v1"

# Sidebar Navigation & System Status
with st.sidebar:
    st.image("https://img.icons8.com/color/96/medical-heart.png", width=64)
    st.markdown("## **CarePath AI**")
    st.markdown("*Multi-Modal Medical Intelligence Platform*")
    st.divider()

    st.markdown("### System Health")
    try:
        res = requests.get(f"{API_URL}/status", timeout=2)
        if res.status_code == 200:
            st.success("🟢 API Gateway: Online")
        else:
            st.warning("🟡 API Gateway: Degraded")
    except Exception:
        st.error("🔴 API Gateway: Offline (Run FastAPI backend)")

    st.divider()
    st.markdown("### Modules Status")
    st.markdown("- 📄 OCR Engine: `Active`")
    st.markdown("- 👁️ Vision Model: `PyTorch/MONAI`")
    st.markdown("- 🧠 Bio-NER NLP: `Active`")
    st.markdown("- 🔍 RAG Vector DB: `ChromaDB`")

# Header
st.markdown('<div class="main-title">CarePath AI Medical Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Clinical Decision Support, Diagnostic Imaging Analysis & Care Plan Generation</div>', unsafe_allow_html=True)

# Navigation Tabs
tab_carepath, tab_vision, tab_ocr, tab_rag = st.tabs([
    "🩺 Patient CarePath Synthesizer",
    "👁️ Computer Vision & DICOM",
    "📄 Document OCR Ingestion",
    "📚 Medical Guidelines RAG"
])

# ---------------------------------------------------------
# TAB 1: CarePath Synthesizer
# ---------------------------------------------------------
with tab_carepath:
    st.subheader("Multi-Modal Patient Case Synthesis")
    col1, col2 = st.columns([1, 1])

    with col1:
        notes_input = st.text_area(
            "Clinical Presentation & History",
            value="Patient is a 54-year-old male presenting with acute cough, fever of 38.5°C, and dyspnea for 3 days. Denies chest pain. History of Type 2 Diabetes on Metformin.",
            height=140
        )
        doc_upload = st.file_uploader("Upload Medical Document / Lab Report (Optional)", type=["png", "jpg", "jpeg", "pdf"], key="carepath_doc")
        img_upload = st.file_uploader("Upload Diagnostic X-Ray / DICOM Image (Optional)", type=["png", "jpg", "jpeg", "dcm"], key="carepath_img")

        btn_synthesize = st.button("🚀 Synthesize Complete Patient CarePath", type="primary", use_container_width=True)

    with col2:
        if btn_synthesize:
            with st.spinner("Synthesizing multi-modal clinical findings..."):
                try:
                    files = {}
                    data = {"clinical_notes": notes_input}
                    if doc_upload:
                        files["document_file"] = (doc_upload.name, doc_upload.getvalue(), doc_upload.type or "image/png")
                    if img_upload:
                        files["image_file"] = (img_upload.name, img_upload.getvalue(), img_upload.type or "image/png")

                    resp = requests.post(f"{API_URL}/diagnosis/synthesize", data=data, files=files if files else None, timeout=15)
                    if resp.status_code == 200:
                        synth = resp.json()
                        st.session_state["synth_result"] = synth
                    else:
                        st.error(f"Synthesis error: {resp.text}")
                except Exception as e:
                    st.error(f"Could not connect to FastAPI server: {e}")

        if "synth_result" in st.session_state:
            res = st.session_state["synth_result"]
            risk = res["risk_assessment"]

            st.markdown("### Risk Stratification & Summary")
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.metric("Patient Risk Score", f"{risk['risk_score']} / 100", delta=risk["risk_level"])
            with r_col2:
                st.info(f"Summary: {res['patient_summary']}")

            st.markdown("### Differential Diagnoses")
            for diff in res["differential_diagnoses"]:
                st.markdown(f"**{diff['condition']}** (ICD-10: `{diff['icd10_code'] or 'N/A'}`) - Confidence: **{int(diff['probability']*100)}%**")
                st.caption(diff["reasoning"])

            st.markdown("### Recommended Clinical Care Path Timeline")
            for step in res["recommended_care_path"]:
                badge = "badge-urgent" if step["urgency"] == "URGENT" else "badge-routine"
                st.markdown(f"""
                <div style="border-left: 4px solid #3B82F6; padding-left: 10px; margin-bottom: 10px;">
                    <span class="{badge}">{step['urgency']}</span> <strong>Step {step['step_number']} ({step['timeframe']})</strong>: {step['description']}
                </div>
                """, unsafe_allow_html=True)

            if res.get("drug_interaction_alerts"):
                st.warning("⚠️ **Drug Interaction Alerts:**\n- " + "\n- ".join(res["drug_interaction_alerts"]))

            st.markdown(f'<div class="disclaimer-box"><strong>Disclaimer:</strong> {res["disclaimer"]}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 2: Vision & DICOM Heatmap
# ---------------------------------------------------------
with tab_vision:
    st.subheader("Diagnostic Computer Vision & Grad-CAM Heatmap")
    v_col1, v_col2 = st.columns([1, 1])

    with v_col1:
        xray_file = st.file_uploader("Upload Chest X-Ray or DICOM File", type=["png", "jpg", "jpeg", "dcm"], key="v_file")
        if xray_file:
            st.image(xray_file, caption="Uploaded Original Image", use_container_width=True)
            btn_vision = st.button("🔍 Analyze Pathology & Generate Heatmap", type="primary")

    with v_col2:
        if xray_file and 'btn_vision' in locals() and btn_vision:
            with st.spinner("Running PyTorch MONAI vision model & Grad-CAM..."):
                try:
                    files = {"file": (xray_file.name, xray_file.getvalue(), xray_file.type or "image/png")}
                    res = requests.post(f"{API_URL}/vision/analyze", files=files, timeout=10)
                    if res.status_code == 200:
                        v_data = res.json()
                        st.markdown(f"### Finding: **{v_data['primary_finding']}** ({int(v_data['confidence']*100)}% Confidence)")
                        st.write(f"**Recommendation:** {v_data['recommendation']}")

                        if v_data.get("gradcam_heatmap_base64"):
                            st.markdown("#### Grad-CAM Explainable AI Heatmap Overlay")
                            b64_str = v_data["gradcam_heatmap_base64"]
                            img_data = base64.b64decode(b64_str)
                            heatmap_img = Image.open(io.BytesIO(img_data))
                            st.image(heatmap_img, caption="Red highlighting indicates localized lesion/consolidation area", use_container_width=True)
                except Exception as e:
                    st.error(f"Vision API error: {e}")

# ---------------------------------------------------------
# TAB 3: Document OCR Ingestion
# ---------------------------------------------------------
with tab_ocr:
    st.subheader("Medical Document & Prescription OCR Ingestion")
    o_col1, o_col2 = st.columns([1, 1])

    with o_col1:
        ocr_file = st.file_uploader("Upload Prescription / Lab Report", type=["png", "jpg", "jpeg", "pdf"], key="o_file")
        if ocr_file and st.button("📄 Extract Text & Structured Data", type="primary"):
            with st.spinner("Running OCR extraction..."):
                try:
                    files = {"file": (ocr_file.name, ocr_file.getvalue(), ocr_file.type or "image/png")}
                    res = requests.post(f"{API_URL}/ocr/extract", files=files, timeout=10)
                    if res.status_code == 200:
                        st.session_state["ocr_result"] = res.json()
                except Exception as e:
                    st.error(f"OCR error: {e}")

    with o_col2:
        if "ocr_result" in st.session_state:
            o_res = st.session_state["ocr_result"]
            st.markdown(f"**Document Type:** `{o_res['document_type']}` | **Confidence:** `{int(o_res['confidence_score']*100)}%`")
            st.text_area("Extracted Raw Text", o_res["raw_text"], height=160)

            if o_res.get("prescriptions"):
                st.markdown("#### Prescriptions Found")
                for rx in o_res["prescriptions"]:
                    st.success(f"💊 **{rx['drug_name']}** - Dosage: {rx['dosage']} | Freq: {rx['frequency']}")

            if o_res.get("lab_metrics"):
                st.markdown("#### Lab Metrics Found")
                for lab in o_res["lab_metrics"]:
                    st.info(f"🧪 **{lab['test_name']}**: {lab['value']} {lab['unit']} (Ref: {lab['reference_range']}) - Status: {lab['status']}")

# ---------------------------------------------------------
# TAB 4: RAG Knowledge Base Search
# ---------------------------------------------------------
with tab_rag:
    st.subheader("Medical Practice Guidelines Vector Search")
    q_input = st.text_input("Enter Clinical Question or Symptom Query", "What is the recommended empirical treatment for community-acquired pneumonia?")
    top_k = st.slider("Top Guidelines to Retrieve", 1, 5, 3)

    if st.button("🔍 Search Guidelines Vector Store", type="primary"):
        with st.spinner("Searching ChromaDB clinical vector store..."):
            try:
                res = requests.post(f"{API_URL}/rag/query", json={"query": q_input, "top_k": top_k}, timeout=10)
                if res.status_code == 200:
                    r_data = res.json()
                    st.markdown("### Evidence-Based Synthesis")
                    st.success(r_data["synthesized_guideline_answer"])

                    st.markdown("### Retrieved Guideline Chunks")
                    for chunk in r_data["retrieved_chunks"]:
                        with st.expander(f"📖 {chunk['title']} (Score: {chunk['relevance_score']})"):
                            st.write(chunk["content"])
                            st.caption(f"Source: {chunk['source']}")
            except Exception as e:
                st.error(f"RAG search error: {e}")
