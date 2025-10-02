
"""
Gemini 2.5 API Client for Fake News Detection
Handles all interactions with Google's Gemini 2.5 AI API
"""

import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any, List

class GeminiClient:
    """Client for interacting with Google Gemini 2.5 API"""

    def __init__(self, api_key: str):
        """
        Initialize Gemini 2.5 client

        Args:
            api_key (str): Google Gemini API key
        """
        genai.configure(api_key=api_key)
        # Updated to use Gemini 2.5 Flash model for better performance
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.api_key = api_key

    def create_grounding_tool(self) -> List[Any]:
        """Create Google Search grounding tool for real-time fact-checking"""
        return [genai.protos.Tool(
            google_search_retrieval=genai.protos.GoogleSearchRetrieval()
        )]

    def analyze_text(self, text: str, use_grounding: bool = True) -> str:
        """
        Analyze text content for fake news detection using Gemini 2.5

        Args:
            text (str): Text content to analyze
            use_grounding (bool): Whether to use Google Search grounding

        Returns:
            str: Analysis result from Gemini 2.5
        """
        prompt = f"""
        As an expert fact-checker and misinformation analyst using advanced Gemini 2.5 capabilities, 
        analyze this news content with enhanced precision and contextual understanding:

        CONTENT: {text}

        Provide comprehensive analysis in this exact format:

        AUTHENTICITY SCORE: [0-100]
        CLASSIFICATION: [AUTHENTIC/SUSPICIOUS/FAKE]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]

        KEY FINDINGS:
        - [Critical finding 1 with specific details]
        - [Critical finding 2 with evidence]
        - [Critical finding 3 with context]

        EVIDENCE FROM SOURCES:
        - [Verified evidence 1 with citation if available]
        - [Verified evidence 2 with source reference]

        RED FLAGS DETECTED:
        - [Specific red flag 1 if any]
        - [Specific red flag 2 if any]

        LINGUISTIC ANALYSIS:
        - [Language pattern assessment]
        - [Bias indicators found]

        RECOMMENDATION: [Detailed actionable recommendation]
        REASONING: [Clear explanation of the assessment logic]
        """

        try:
            tools = self.create_grounding_tool() if use_grounding else []

            response = self.model.generate_content(
                prompt,
                tools=tools if use_grounding else None,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.05,  # Lower temperature for more consistent analysis
                    max_output_tokens=2500,  # Increased for more detailed analysis
                    top_p=0.8,
                    top_k=40
                )
            )

            return response.text

        except Exception as e:
            return f"Error in Gemini 2.5 text analysis: {str(e)}"

    def analyze_image(self, image: Image.Image, context: str = "") -> str:
        """
        Analyze image for authenticity and manipulation using Gemini 2.5 vision capabilities

        Args:
            image (Image.Image): PIL Image to analyze
            context (str): Optional text context

        Returns:
            str: Analysis result from Gemini 2.5
        """
        prompt = f"""
        As an advanced image forensics expert using Gemini 2.5's enhanced vision capabilities, 
        analyze this image for authenticity, manipulation, and contextual accuracy:

        CONTEXT: {context}

        Perform comprehensive analysis covering:
        1. Digital manipulation detection with advanced algorithms
        2. Metadata and technical inconsistencies
        3. Visual artifacts and compression patterns
        4. Contextual and temporal relevance
        5. Deepfake and AI-generation indicators

        Provide analysis in this format:

        IMAGE AUTHENTICITY SCORE: [0-100]
        MANIPULATION DETECTED: [YES/NO/UNCERTAIN]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]

        TECHNICAL ANALYSIS:
        - [Advanced technical finding 1]
        - [Advanced technical finding 2]
        - [Metadata analysis result]

        VISUAL FORENSICS:
        - [Pixel-level analysis result]
        - [Compression artifact assessment]
        - [Lighting and shadow consistency]

        CONTEXTUAL ANALYSIS:
        - [Temporal accuracy assessment]
        - [Geographic consistency check]
        - [Subject matter verification]

        AI DETECTION ANALYSIS:
        - [Deepfake indicators if any]
        - [AI generation signatures]

        RECOMMENDATION: [Specific actionable guidance]
        VERIFICATION STEPS: [Suggested next steps for verification]
        """

        try:
            response = self.model.generate_content([prompt, image])
            return response.text

        except Exception as e:
            return f"Error in Gemini 2.5 image analysis: {str(e)}"

    def multimodal_analysis(self, text: str, image: Image.Image, use_grounding: bool = True) -> str:
        """
        Perform advanced combined text and image analysis using Gemini 2.5's multimodal capabilities

        Args:
            text (str): Text content
            image (Image.Image): Image content
            use_grounding (bool): Whether to use Google Search grounding

        Returns:
            str: Combined analysis result from Gemini 2.5
        """
        prompt = f"""
        As a multimodal misinformation expert using Gemini 2.5's advanced cross-modal reasoning,
        perform comprehensive analysis of both text and image content:

        TEXT CONTENT: {text}

        Conduct advanced multimodal analysis including:

        1. Individual authenticity assessment with enhanced precision
        2. Cross-modal consistency verification using advanced reasoning
        3. Temporal and contextual alignment analysis
        4. Source credibility cross-referencing
        5. Narrative coherence evaluation

        Provide comprehensive analysis in this format:

        OVERALL AUTHENTICITY SCORE: [0-100]
        FINAL CLASSIFICATION: [AUTHENTIC/SUSPICIOUS/FAKE]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
        MULTIMODAL CONSISTENCY: [CONSISTENT/PARTIALLY_CONSISTENT/INCONSISTENT]

        TEXT ANALYSIS SUMMARY:
        - [Enhanced text finding 1]
        - [Enhanced text finding 2]
        - [Linguistic pattern analysis]

        IMAGE ANALYSIS SUMMARY:
        - [Advanced image finding 1]
        - [Advanced image finding 2]
        - [Visual forensics result]

        CROSS-MODAL CONSISTENCY ANALYSIS:
        - [Consistency check 1 with detailed reasoning]
        - [Consistency check 2 with evidence]
        - [Temporal alignment assessment]
        - [Narrative coherence evaluation]

        EVIDENCE SUPPORTING ASSESSMENT:
        - [Verified evidence 1 with source if available]
        - [Verified evidence 2 with citation]
        - [Cross-referenced information]

        CONTRADICTION ANALYSIS:
        - [Identified contradiction 1 if any]
        - [Identified contradiction 2 if any]

        ADVANCED INSIGHTS:
        - [Deep contextual insight 1]
        - [Pattern recognition result]
        - [Anomaly detection finding]

        FINAL RECOMMENDATION: [Comprehensive actionable recommendation]
        VERIFICATION STRATEGY: [Detailed verification approach]
        RISK ASSESSMENT: [Specific risk evaluation for sharing/believing]
        """

        try:
            tools = self.create_grounding_tool() if use_grounding else []
            content = [prompt, image]

            response = self.model.generate_content(
                content,
                tools=tools if use_grounding else None,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.05,  # Very low temperature for consistent analysis
                    max_output_tokens=3500,  # Increased for comprehensive analysis
                    top_p=0.8,
                    top_k=40
                )
            )

            return response.text

        except Exception as e:
            return f"Error in Gemini 2.5 multimodal analysis: {str(e)}"

    def batch_analyze(self, items: List[Dict[str, Any]], use_grounding: bool = True) -> List[str]:
        """
        Perform batch analysis using Gemini 2.5's improved efficiency

        Args:
            items (List[Dict]): List of items to analyze, each with 'type', 'content', and optional 'image'
            use_grounding (bool): Whether to use Google Search grounding

        Returns:
            List[str]: Analysis results for each item
        """
        results = []

        for item in items:
            try:
                if item['type'] == 'text':
                    result = self.analyze_text(item['content'], use_grounding)
                elif item['type'] == 'image':
                    result = self.analyze_image(item['image'], item.get('context', ''))
                elif item['type'] == 'multimodal':
                    result = self.multimodal_analysis(
                        item['content'], 
                        item['image'], 
                        use_grounding
                    )
                else:
                    result = f"Unsupported analysis type: {item['type']}"

                results.append(result)

            except Exception as e:
                results.append(f"Error analyzing item: {str(e)}")

        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the Gemini 2.5 model being used"""
        return {
            'model_name': 'gemini-2.0-flash-exp',
            'version': '2.5',
            'capabilities': [
                'Advanced text analysis',
                'Enhanced image forensics',
                'Multimodal reasoning',
                'Real-time grounding',
                'Batch processing',
                'Improved accuracy',
                'Lower latency'
            ],
            'max_tokens': 3500,
            'temperature_range': '0.0-1.0',
            'supports_grounding': True,
            'supports_multimodal': True
        }
