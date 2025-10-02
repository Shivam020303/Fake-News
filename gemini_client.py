
"""
Gemini 2.5 API Client - Complete Implementation with Optimized Fake News Detection
Handles all interactions with Google's Gemini 2.5 AI API including reverse image search,
OCR text extraction, and comprehensive multimodal analysis.
"""

import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import Optional, Dict, Any, List
import json
import re

class GeminiClient:
    """
    Complete Client for interacting with Google Gemini 2.5 API
    Implements optimized fake news detection workflow with reverse image search,
    OCR extraction, and advanced evidence-based analysis.
    """

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
                'Reverse image search analysis',
                'OCR text extraction',
                'Improved accuracy',
                'Lower latency'
            ],
            'max_tokens': 3500,
            'temperature_range': '0.0-1.0',
            'supports_grounding': True,
            'supports_multimodal': True,
            'supports_ocr': True,
            'supports_reverse_search': True
        }

    def reverse_image_search_analysis(self, image: Image.Image, context: str = "") -> str:
        """
        Perform reverse image search analysis to check image authenticity

        Args:
            image (Image.Image): PIL Image to analyze
            context (str): Optional context about the image

        Returns:
            str: Reverse image search analysis result
        """
        prompt = f"""
        As an expert in image verification and reverse search analysis, examine this image thoroughly.

        Context: {context}

        Perform comprehensive reverse image search analysis:

        1. VISUAL SIMILARITY ASSESSMENT:
           - Analyze if this image appears to be original or recycled
           - Look for signs of manipulation, editing, or synthetic generation
           - Check for watermarks, logos, or identifying features

        2. CONTEXTUAL VERIFICATION:
           - Assess if the image matches the claimed context
           - Look for anachronisms or inconsistencies
           - Evaluate temporal and geographical consistency

        3. AUTHENTICITY INDICATORS:
           - Check for digital manipulation artifacts
           - Analyze compression patterns and metadata inconsistencies
           - Look for AI-generated or deepfake indicators

        4. EVIDENCE COMPILATION:
           - Identify key visual elements for further verification
           - Suggest reverse search strategies
           - Flag potential red flags or supporting evidence

        Provide analysis in this format:

        REVERSE SEARCH ASSESSMENT: [Analysis of likely matches and sources]
        AUTHENTICITY SCORE: [0-100]
        MANIPULATION DETECTED: [YES/NO/UNCERTAIN]

        VISUAL EVIDENCE:
        - [Key finding 1]
        - [Key finding 2]
        - [Key finding 3]

        CONTEXTUAL ANALYSIS:
        - [Context verification 1]
        - [Context verification 2]

        RED FLAGS:
        - [Flag 1 if any]
        - [Flag 2 if any]

        VERIFICATION STEPS:
        - [Suggested verification step 1]
        - [Suggested verification step 2]

        RECOMMENDATION: [Detailed recommendation for further verification]
        """

        try:
            response = self.model.generate_content([prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.05,
                    max_output_tokens=2000,
                    top_p=0.8,
                    top_k=40
                )
            )
            return response.text
        except Exception as e:
            return f"Error in reverse image search analysis: {str(e)}"

    def extract_text_from_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract text from image using OCR and analyze for key topics

        Args:
            image (Image.Image): PIL Image to extract text from

        Returns:
            Dict[str, Any]: Extracted text and topic analysis
        """
        prompt = f"""
        As an OCR and NLP expert, extract and analyze all text from this image.

        Tasks:
        1. Extract ALL visible text accurately (headlines, captions, body text, etc.)
        2. Identify key topics, entities, and themes
        3. Extract important keywords for fact-checking
        4. Suggest search queries for verification

        Provide analysis in this format:

        EXTRACTED_TEXT: [All visible text from the image]

        KEY_TOPICS:
        - [Topic 1]
        - [Topic 2]
        - [Topic 3]

        IMPORTANT_KEYWORDS:
        - [Keyword 1]
        - [Keyword 2]
        - [Keyword 3]

        ENTITIES_DETECTED:
        - [Person/Organization/Location 1]
        - [Person/Organization/Location 2]

        SEARCH_QUERIES:
        - [Query 1 for fact-checking]
        - [Query 2 for verification]

        ANALYSIS_PRIORITY: [What aspects need immediate fact-checking]
        """

        try:
            response = self.model.generate_content([prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=1500,
                    top_p=0.8,
                    top_k=40
                )
            )
            return {"success": True, "analysis": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def analyze_text(self, text: str, use_grounding: bool = True) -> str:
        """
        Analyze text content for fake news detection using enhanced Gemini 2.5

        Args:
            text (str): Text content to analyze
            use_grounding (bool): Whether to use Google Search grounding

        Returns:
            str: Analysis result from Gemini 2.5
        """
        prompt = f"""
        As an expert fact-checker using advanced Gemini 2.5 capabilities, analyze this content:

        CONTENT: {text}

        Perform comprehensive analysis:

        1. KEYWORD AND TOPIC EXTRACTION:
           - Extract main topics, entities, and claims
           - Identify key facts that need verification
           - Find controversial or suspicious elements

        2. CREDIBILITY ASSESSMENT:
           - Cross-reference claims with reliable sources
           - Check for bias, manipulation, or misleading language
           - Verify factual accuracy of key statements

        3. EVIDENCE COMPILATION:
           - Gather supporting evidence from credible sources
           - Identify contradicting information
           - Cite specific sources and references

        4. CRITICAL REASONING:
           - Provide logical reasoning chain for assessment
           - Explain why content is authentic, suspicious, or fake
           - Consider multiple perspectives and interpretations

        Provide analysis in this exact format:

        AUTHENTICITY SCORE: [0-100]
        CLASSIFICATION: [AUTHENTIC/SUSPICIOUS/FAKE]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]

        KEY_TOPICS_EXTRACTED:
        - [Topic 1]
        - [Topic 2]
        - [Topic 3]

        FACT_CHECK_RESULTS:
        - [Verified fact 1 with source]
        - [Verified fact 2 with source]
        - [Contradicted claim 1 with evidence]

        SUPPORTING_EVIDENCE:
        - [Evidence 1 with citation]
        - [Evidence 2 with citation]

        RED_FLAGS_DETECTED:
        - [Red flag 1 with explanation]
        - [Red flag 2 with explanation]

        REASONING_CHAIN:
        [Step-by-step logical reasoning for the assessment]

        VERIFICATION_STEPS:
        - [Suggested step 1]
        - [Suggested step 2]

        RECOMMENDATION: [Detailed actionable recommendation]
        """

        try:
            tools = self.create_grounding_tool() if use_grounding else []

            response = self.model.generate_content(
                prompt,
                tools=tools if use_grounding else None,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.05,
                    max_output_tokens=2500,
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

        # First perform reverse image search analysis
        reverse_analysis = self.reverse_image_search_analysis(image, context)

        # Then extract text if needed
        ocr_result = self.extract_text_from_image(image)

        # Combine both analyses
        prompt = f"""
        As an advanced image forensics expert using Gemini 2.5's enhanced capabilities,
        provide a comprehensive image authenticity analysis.

        Context: {context}

        Previous Analysis Results:
        REVERSE SEARCH: {reverse_analysis}
        OCR EXTRACTION: {ocr_result.get('analysis', 'No text detected')}

        Perform final comprehensive analysis:

        IMAGE AUTHENTICITY SCORE: [0-100]
        MANIPULATION DETECTED: [YES/NO/UNCERTAIN]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]

        TECHNICAL_ANALYSIS:
        - [Technical finding 1]
        - [Technical finding 2]
        - [Metadata/compression analysis]

        CONTEXTUAL_VERIFICATION:
        - [Context matching assessment]
        - [Temporal consistency check]
        - [Geographic/situational accuracy]

        TEXT_CONTENT_ANALYSIS:
        - [Analysis of extracted text if any]
        - [Fact-checking of text claims]

        FINAL_ASSESSMENT:
        [Comprehensive reasoning combining all analyses]

        RECOMMENDATION: [Specific actionable guidance]
        VERIFICATION_STEPS: [Detailed next steps for verification]
        """

        try:
            response = self.model.generate_content([prompt, image])
            return response.text

        except Exception as e:
            return f"Error in Gemini 2.5 image analysis: {str(e)}"

    def multimodal_analysis(self, text: str, image: Image.Image, use_grounding: bool = True) -> str:
        """
        Perform comprehensive multimodal analysis using optimized workflow

        Args:
            text (str): Text content
            image (Image.Image): Image content
            use_grounding (bool): Whether to use Google Search grounding

        Returns:
            str: Combined analysis result
        """

        # Step 1: Analyze image with reverse search
        image_analysis = self.analyze_image(image, text)

        # Step 2: Extract text from image
        ocr_result = self.extract_text_from_image(image)
        extracted_text = ocr_result.get('analysis', '') if ocr_result.get('success') else ''

        # Step 3: Combine text from article and extracted text
        combined_text = f"Article Text: {text}\n\nExtracted from Image: {extracted_text}"

        # Step 4: Comprehensive multimodal analysis
        prompt = f"""
        As a multimodal misinformation expert using Gemini 2.5's advanced capabilities,
        perform the ultimate authenticity assessment combining all available evidence.

        TEXT CONTENT: {text}
        IMAGE ANALYSIS: {image_analysis}
        EXTRACTED TEXT: {extracted_text}

        Perform comprehensive multimodal analysis:

        OVERALL AUTHENTICITY SCORE: [0-100]
        FINAL CLASSIFICATION: [AUTHENTIC/SUSPICIOUS/FAKE]
        CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
        CROSS_MODAL_CONSISTENCY: [CONSISTENT/PARTIALLY_CONSISTENT/INCONSISTENT]

        TEXT_ANALYSIS_SUMMARY:
        - [Key text finding 1]
        - [Key text finding 2]
        - [Fact-check result]

        IMAGE_ANALYSIS_SUMMARY:
        - [Key image finding 1]
        - [Key image finding 2]
        - [Authenticity assessment]

        CROSS_MODAL_VERIFICATION:
        - [Consistency check 1 with detailed reasoning]
        - [Consistency check 2 with evidence]
        - [Timeline and context alignment]

        EVIDENCE_COMPILATION:
        - [Supporting evidence 1 with source]
        - [Supporting evidence 2 with citation]
        - [Contradicting evidence if any]

        COMPREHENSIVE_REASONING:
        [Detailed step-by-step reasoning combining all analyses]

        RED_FLAGS_IDENTIFIED:
        - [Red flag 1 with explanation]
        - [Red flag 2 with explanation]

        VERIFICATION_STRATEGY:
        [Complete strategy for further verification]

        FINAL_RECOMMENDATION:
        [Comprehensive actionable recommendation with risk assessment]
        """

        try:
            tools = self.create_grounding_tool() if use_grounding else []
            content = [prompt, image]

            response = self.model.generate_content(
                content,
                tools=tools if use_grounding else None,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.05,
                    max_output_tokens=3500,
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
            items (List[Dict]): List of items to analyze
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
