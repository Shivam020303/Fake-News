
"""
AI-Powered Multimodal Fake News Detector - Enhanced Output Formatting
Advanced Streamlit Application with clear result categorization and detailed analysis
"""

from typing import Dict, Any, List
import streamlit as st
from PIL import Image
import io
import time
from datetime import datetime
import traceback
import json

# Import our custom modules
from gemini_client import GeminiClient
from result_parser import ResultParser

# Configure page
st.set_page_config(
    page_title="AI Fake News Detector 2.5",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for clear result formatting
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #1f1f23;
    padding: 1rem 0;
    margin-bottom: 2rem;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: bold;
}

/* Clear Result Categorization Styles */
.result-real {
    border: 3px solid #28a745;
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
}

.result-fake {
    border: 3px solid #dc3545;
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.result-manipulated {
    border: 3px solid #ffc107;
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 1.5rem 0;
    text-align: center;
    box-shadow: 0 4px 8px rgba(255, 193, 7, 0.3);
}

.result-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-subtitle {
    font-size: 1.2rem;
    margin: 0 0 1.5rem 0;
    opacity: 0.8;
}

.confidence-display {
    font-size: 3rem;
    font-weight: bold;
    margin: 1rem 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.detailed-analysis-btn {
    background: linear-gradient(45deg, #667eea, #764ba2);
    border: none;
    color: white;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    margin: 1rem 0;
}

.detailed-analysis-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.factor-analysis {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.factor-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #495057;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 0.5rem;
}

.factor-item {
    background: #f8f9fa;
    border-left: 4px solid #007bff;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 5px;
}

.quick-summary {
    background: rgba(255,255,255,0.9);
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

def get_clear_categorization(classification: str, score: int) -> Dict[str, str]:
    """
    Get clear, specific categorization for the result

    Args:
        classification (str): AI classification
        score (int): Confidence score

    Returns:
        Dict[str, str]: Clear categorization details
    """
    if classification == "AUTHENTIC" and score >= 80:
        return {
            "category": "REAL",
            "css_class": "result-real",
            "icon": "✅",
            "title": "Content is REAL",
            "subtitle": "This content appears to be authentic and trustworthy",
            "color": "#28a745"
        }
    elif classification == "FAKE" or score < 30:
        return {
            "category": "FAKE",
            "css_class": "result-fake", 
            "icon": "❌",
            "title": "Content is FAKE",
            "subtitle": "This content appears to be false or fabricated",
            "color": "#dc3545"
        }
    else:
        return {
            "category": "PARTIALLY MANIPULATED",
            "css_class": "result-manipulated",
            "icon": "⚠️", 
            "title": "Content is PARTIALLY MANIPULATED",
            "subtitle": "This content may contain some manipulation or requires verification",
            "color": "#ffc107"
        }

def display_clear_result(result_data, analysis_type="Analysis"):
    """Display results with clear categorization as specified"""

    classification = result_data.get('classification', 'UNCERTAIN')
    score = result_data.get('score', 0)

    # Get clear categorization
    category_info = get_clear_categorization(classification, score)

    # Main result display
    st.markdown(f"""
    <div class="{category_info['css_class']}">
        <div class="result-title" style="color: {category_info['color']};">
            {category_info['icon']} {category_info['title']}
        </div>
        <div class="result-subtitle">
            {category_info['subtitle']}
        </div>
        <div class="confidence-display" style="color: {category_info['color']};">
            {score}% Confidence
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick summary
    st.markdown(f"""
    <div class="quick-summary">
        <h4>📋 Quick Summary</h4>
        <p><strong>Analysis Type:</strong> {analysis_type}</p>
        <p><strong>Result:</strong> {category_info['category']}</p>
        <p><strong>Confidence Level:</strong> {ResultParser.get_confidence_level(score)}</p>
        <p><strong>Risk Level:</strong> {ResultParser.get_risk_level(classification, score)}</p>
    </div>

    # Detailed Analysis Button
    if st.button(
        with st.expander(f"🔍 Detailed Analysis — Why this is {category_info['category']}?"):
    show_detailed_factor_analysis(result_data, category_info)
)

def show_detailed_factor_analysis(result_data, category_info):
    """Show detailed factor-by-factor analysis"""

    st.markdown("---")
    st.markdown(f"## 🔬 Detailed Factor Analysis: Why is this content {category_info['category']}?")

    # Factor 1: Key Findings Analysis
    findings = result_data.get('key_findings', [])
    if findings:
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">🎯 Key Detection Factors</div>
        </div>
        """, unsafe_allow_html=True)

        for i, finding in enumerate(findings, 1):
            st.markdown(f"""
            <div class="factor-item">
                <strong>Factor {i}:</strong> {finding}
            </div>
            """, unsafe_allow_html=True)

    # Factor 2: Evidence Analysis
    evidence = result_data.get('evidence', [])
    if evidence:
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">📊 Evidence Supporting Classification</div>
        </div>
        """, unsafe_allow_html=True)

        for i, item in enumerate(evidence, 1):
            st.markdown(f"""
            <div class="factor-item">
                <strong>Evidence {i}:</strong> {item}
            </div>
            """, unsafe_allow_html=True)

    # Factor 3: Red Flags Analysis
    red_flags = result_data.get('red_flags', [])
    if red_flags:
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">🚩 Warning Indicators</div>
        </div>
        """, unsafe_allow_html=True)

        for i, flag in enumerate(red_flags, 1):
            st.markdown(f"""
            <div class="factor-item">
                <strong>Red Flag {i}:</strong> {flag}
            </div>
            """, unsafe_allow_html=True)

    # Factor 4: Technical Analysis
    reasoning = result_data.get('reasoning_chain', '')
    if reasoning:
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">🧠 AI Reasoning Process</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="factor-item">
            <strong>Analysis Logic:</strong> {reasoning}
        </div>
        """, unsafe_allow_html=True)

    # Factor 5: Cross-Modal Consistency (for multimodal)
    consistency = result_data.get('cross_modal_consistency', '')
    if consistency and consistency != "Not Assessed":
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">🔗 Text-Image Consistency Analysis</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="factor-item">
            <strong>Consistency Assessment:</strong> {consistency}
        </div>
        """, unsafe_allow_html=True)

    # Factor 6: Recommendation
    recommendation = result_data.get('recommendation', '')
    if recommendation:
        st.markdown("""
        <div class="factor-analysis">
            <div class="factor-title">💡 Expert Recommendation</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="factor-item">
            <strong>Recommended Action:</strong> {recommendation}
        </div>
        """, unsafe_allow_html=True)

    # Complete technical analysis
    with st.expander("📋 Complete Technical Analysis Report"):
        st.text_area("Full AI Analysis", result_data.get('raw_analysis', ''), height=400, disabled=True)

def main():
    """Main application with enhanced formatting"""

    # Application header
    st.markdown('<h1 class="main-header">🔍 AI Fake News Detector</h1>', 
                unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; font-size: 1.2rem; color: #666;">
        <p>🚀 <strong>Enhanced with Gemini 2.5 Flash</strong> - Clear, Precise Results</p>
        <p>📊 Get definitive answers: REAL, FAKE, or PARTIALLY MANIPULATED</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("🔧 Gemini 2.5 Configuration")

        api_key = st.text_input(
            "🔑 Google Gemini API Key",
            type="password",
            help="Get your API key from: https://makersuite.google.com/app/apikey",
            placeholder="Enter your Gemini API key..."
        )

        use_grounding = st.checkbox(
            "🌐 Enable Google Search Grounding",
            value=True,
            help="Uses real-time web search for enhanced accuracy"
        )

        analysis_mode = st.radio(
            "📊 Analysis Mode",
            ["Text Analysis", "Image Analysis", "Multimodal Analysis"],
            help="Choose your analysis type"
        )

        st.markdown("---")
        st.markdown("""
        ### 🎯 Result Categories:

        **✅ REAL**
        - Content is authentic
        - High confidence (80%+)
        - Verified sources

        **❌ FAKE** 
        - Content is fabricated
        - Clear misinformation
        - Low confidence (<30%)

        **⚠️ PARTIALLY MANIPULATED**
        - Some manipulation detected
        - Mixed signals
        - Requires verification
        """)

    # Main content area
    if not api_key:
        st.info("""
        ### 🚀 Get Started with Clear Results

        1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. **Enter Key**: Paste it in the sidebar
        3. **Upload Content**: Add text or image
        4. **Get Clear Answer**: REAL, FAKE, or PARTIALLY MANIPULATED
        """)
        return

    # Initialize client
    try:
        client = GeminiClient(api_key)
        st.success("✅ Gemini 2.5 Flash ready for analysis!")
    except Exception as e:
        st.error(f"❌ Failed to initialize: {str(e)}")
        return

    # Content input section
    st.markdown("## 📝 Content Input")

    text_input = ""
    uploaded_image = None

    if analysis_mode in ["Text Analysis", "Multimodal Analysis"]:
        st.subheader("📄 Text Content")
        text_input = st.text_area(
            "Enter news article text:",
            height=200,
            placeholder="Paste the news article text here...",
            help="Enter the complete text you want to verify"
        )

    if analysis_mode in ["Image Analysis", "Multimodal Analysis"]:
        st.subheader("🖼️ Image Content")
        uploaded_image = st.file_uploader(
            "Upload news image:",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload the image you want to analyze"
        )

        if uploaded_image:
            image = Image.open(uploaded_image)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(image, caption="Uploaded Image", use_container_width=True)

    # Analysis execution
    st.markdown("---")
    st.markdown("## 🔍 Analysis Results")

    # Analysis buttons
    if analysis_mode == "Text Analysis":
        if st.button("🚀 Analyze Text Content", type="primary", use_container_width=True, disabled=not text_input.strip()):
            if text_input.strip():
                with st.spinner("🤖 Analyzing content with Gemini 2.5..."):
                    try:
                        analysis_result = client.analyze_text(text_input, use_grounding)
                        parsed_result = ResultParser.parse_analysis(analysis_result)
                        display_clear_result(parsed_result, "Text Content Analysis")
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

    elif analysis_mode == "Image Analysis":
        if st.button("🔬 Analyze Image Content", type="primary", use_container_width=True, disabled=uploaded_image is None):
            if uploaded_image:
                with st.spinner("🤖 Analyzing image with enhanced AI vision..."):
                    try:
                        image = Image.open(uploaded_image)
                        analysis_result = client.analyze_image(image, text_input or "")
                        parsed_result = ResultParser.parse_analysis(analysis_result)
                        display_clear_result(parsed_result, "Image Content Analysis")
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

    elif analysis_mode == "Multimodal Analysis":
        if st.button("🔄 Perform Multimodal Analysis", type="primary", use_container_width=True, disabled=not text_input.strip() or uploaded_image is None):
            if text_input.strip() and uploaded_image:
                with st.spinner("🤖 Performing comprehensive multimodal analysis..."):
                    try:
                        image = Image.open(uploaded_image)
                        analysis_result = client.multimodal_analysis(text_input, image, use_grounding)
                        parsed_result = ResultParser.parse_analysis(analysis_result)
                        display_clear_result(parsed_result, "Multimodal Analysis")
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 2rem 0;">
        <p>🛡️ <strong>Clear, Precise Fake News Detection</strong> | Powered by Gemini 2.5 Flash</p>
        <p>✅ REAL | ❌ FAKE | ⚠️ PARTIALLY MANIPULATED</p>
        <p>⚠️ <em>Always verify critical information through multiple authoritative sources.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
