
"""
Gemini 2.5 API Client - Optimized for Detailed Fake News Detection Workflow
"""

import google.generativeai as genai
from PIL import Image
from typing import Optional, Dict, Any, List

class GeminiClient:
    """
    Optimized Client for Google Gemini 2.5 (Flash) for Fake News Detection
    Implements: reverse image search reasoning, OCR-to-keywords fallback,
    advanced topic/keyword search, explicit evidence summaries, and critical reasoning output.
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.api_key = api_key

    def create_grounding_tool(self) -> List[Any]:
        return [genai.protos.Tool(
            google_search_retrieval=genai.protos.GoogleSearchRetrieval()
        )]

    def reverse_image_search_rationale(self, image: Image.Image) -> str:
        """Simulates reasoning for image reverse search using Gemini multimodal input"""
        prompt = f"""
        You are an expert fake news analyst utilizing image reverse search.
        Carefully review the uploaded image, retrieve and analyze visually similar matches (imagine Google Lens results),
        summarize matched sources (titles, context), and critically reason:
        - Are there signs of manipulation, context shift, or incorrect provenance?
        - Are there reliable sources associating this image with the stated topic?
        - List any supporting/dissenting evidence, and provide a preliminary confidence and citation summary.
        Output a concise reasoned analysis with critical thinking.
        """
        try:
            response = self.model.generate_content([prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.08,
                    max_output_tokens=1500
                )
            )
            return response.text
        except Exception as e:
            return f"Reverse image analysis error: {str(e)}"

    def ocr_and_topic_extraction(self, image: Image.Image) -> Dict[str, Any]:
        """
        Extract text from image and use NLP to find key topics (fallback if reverse search is inconclusive)
        Currently stub: actual OCR is handled externally for privacy; simulate extraction/analysis path.
        """
        prompt = f"""
        The image contains embedded text. Your tasks:
        - Accurately extract all visible text from the image.
        - Identify and list the most relevant keywords, topics, and entities present.
        - Suggest how these topics should guide further fact-checking and evidence search for genuineness testing.
        Output structured JSON with: extracted_text, topics, evidence_search_suggestions.
        """
        try:
            response = self.model.generate_content([prompt, image],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.07,
                    max_output_tokens=1200
                )
            )
            return response.text
        except Exception as e:
            return {"error": str(e)}

    def analyze_text_or_article(self, text: str, use_grounding: bool = True) -> str:
        """
        NLP + multi-source fact-checking for article/ocr text:
        - Extract topics, run Google Search Grounding, compare against credible sources, cite specific evidence,
          and provide explicit reason-chain.
        - Flag bias/manipulation/copy-paste clues.
        """
        tools = self.create_grounding_tool() if use_grounding else []
        prompt = f"""
        As an advanced AI-powered fact-checker, analyze the following article or extracted text:
        1. Extract the most relevant keywords, topics, and entities.
        2. For each topic, retrieve the latest evidence and summaries using Google Search Grounding.
        3. Critically evaluate: compare with reputable sources, detect bias, emotional/linguistic manipulation, and trace the topic's source.
        4. Provide:
            - Supporting and dissenting evidence snippets with citations
            - Genuineness/confidence score (0-100) with justification
            - Detected red flags (if any) and critical reasoning for each
            - A concise but transparent reason-chain: "Because X, Y, and Z, the article is assessed as ..."
        Output structured JSON with sections: topics, evidence, confidence, red_flags, reasoning_chain, suggested_verification_steps.
        """
        try:
            response = self.model.generate_content(prompt,
                tools=tools if use_grounding else None,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.08,
                    max_output_tokens=1800
                )
            )
            return response.text
        except Exception as e:
            return f"Text/article analysis error: {str(e)}"

    def multimodal_detect(self, image: Optional[Image.Image]=None, text: Optional[str]=None, use_grounding: bool=True) -> Dict[str, Any]:
        """
        Complete pipeline: reverse search (image), OCR fallback, then article/topic analysis with explicit reason-chain and evidence summary.
        Returns visual text and structured output.
        """
        results = {}
        if image is not None:
            # Step 1: Reverse image search rationale
            step1 = self.reverse_image_search_rationale(image)
            results['reverse_image_assessment'] = step1
            if 'no relevant matches' in step1.lower() or 'could not determine' in step1.lower():
                # Step 2: OCR & topics
                step2 = self.ocr_and_topic_extraction(image)
                results['ocr_topics'] = step2
                ocr_text = step2 if isinstance(step2, str) else step2.get('extracted_text', '')
                # Step 3: Treat OCR as article
                step3 = self.analyze_text_or_article(ocr_text, use_grounding)
                results['ocr_article_analysis'] = step3
        elif text:
            # Step 3: Article analysis direct
            results['article_analysis'] = self.analyze_text_or_article(text, use_grounding)
        return results
