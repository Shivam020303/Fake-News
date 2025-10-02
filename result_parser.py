
"""
Enhanced Result Parser for Optimized Fake News Detection Analysis
Parses and structures analysis results from the enhanced Gemini 2.5 API workflow
"""

import re
from typing import Dict, Any, List, Optional

class ResultParser:
    """Enhanced parser for structuring optimized analysis results"""

    @staticmethod
    def extract_score(text: str) -> int:
        """
        Extract authenticity score from analysis text with enhanced patterns

        Args:
            text (str): Analysis text

        Returns:
            int: Extracted score (0-100)
        """
        # Enhanced patterns for score extraction
        score_patterns = [
            r'(?:AUTHENTICITY SCORE|OVERALL.*SCORE|IMAGE.*SCORE):\s*(\d{1,3})',
            r'(?:SCORE|Score):\s*(\d{1,3})',
            r'(\d{1,3})/100',
            r'(\d{1,3})%',
            r'(\d{1,3})\s*(?:out of 100|/ 100)'
        ]

        for pattern in score_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(max(score, 0), 100)

        return 0

    @staticmethod
    def extract_classification(text: str) -> str:
        """
        Extract classification from enhanced analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Classification (AUTHENTIC, SUSPICIOUS, FAKE, or UNCERTAIN)
        """
        text_lower = text.lower()

        # Check for explicit classifications
        classification_patterns = [
            r'(?:CLASSIFICATION|FINAL CLASSIFICATION):\s*(AUTHENTIC|SUSPICIOUS|FAKE)',
            r'(?:ASSESSMENT|FINAL ASSESSMENT):\s*(AUTHENTIC|SUSPICIOUS|FAKE)'
        ]

        for pattern in classification_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        # Fallback keyword analysis
        authentic_keywords = ['authentic', 'genuine', 'real', 'credible', 'trustworthy', 'verified']
        fake_keywords = ['fake', 'false', 'fabricated', 'misleading', 'deceptive', 'manipulated']
        suspicious_keywords = ['suspicious', 'questionable', 'uncertain', 'dubious', 'requires verification']

        # Count keyword occurrences
        authentic_count = sum(1 for keyword in authentic_keywords if keyword in text_lower)
        fake_count = sum(1 for keyword in fake_keywords if keyword in text_lower)
        suspicious_count = sum(1 for keyword in suspicious_keywords if keyword in text_lower)

        # Determine classification based on highest count
        if fake_count > authentic_count and fake_count > suspicious_count:
            return "FAKE"
        elif authentic_count > fake_count and authentic_count > suspicious_count:
            return "AUTHENTIC"
        elif suspicious_count > 0:
            return "SUSPICIOUS"

        return "UNCERTAIN"

    @staticmethod
    def extract_key_findings(text: str) -> List[str]:
        """
        Extract key findings from enhanced analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of key findings
        """
        findings = []

        # Enhanced patterns for findings extraction
        patterns = [
            r'KEY_TOPICS_EXTRACTED:(.*?)(?=\n[A-Z_]+:|$)',
            r'KEY FINDINGS:(.*?)(?=\n[A-Z]+:|$)',
            r'VISUAL EVIDENCE:(.*?)(?=\n[A-Z]+:|$)',
            r'TECHNICAL_ANALYSIS:(.*?)(?=\n[A-Z_]+:|$)',
            r'TEXT_ANALYSIS_SUMMARY:(.*?)(?=\n[A-Z_]+:|$)',
            r'IMAGE_ANALYSIS_SUMMARY:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                findings_text = match.group(1)
                # Extract bullet points
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', findings_text)
                findings.extend([point.strip() for point in bullet_points])

        return findings[:8]  # Return top 8 findings

    @staticmethod
    def extract_evidence(text: str) -> List[str]:
        """
        Extract evidence from enhanced analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of evidence points
        """
        evidence = []

        # Enhanced patterns for evidence extraction
        patterns = [
            r'SUPPORTING_EVIDENCE:(.*?)(?=\n[A-Z_]+:|$)',
            r'FACT_CHECK_RESULTS:(.*?)(?=\n[A-Z_]+:|$)',
            r'EVIDENCE_COMPILATION:(.*?)(?=\n[A-Z_]+:|$)',
            r'VERIFICATION:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                evidence_text = match.group(1)
                # Extract bullet points
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', evidence_text)
                evidence.extend([point.strip() for point in bullet_points])

        return evidence[:5]  # Return top 5 evidence points

    @staticmethod
    def extract_red_flags(text: str) -> List[str]:
        """
        Extract red flags from enhanced analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of red flags
        """
        red_flags = []

        # Enhanced patterns for red flags
        patterns = [
            r'RED_FLAGS_DETECTED:(.*?)(?=\n[A-Z_]+:|$)',
            r'RED FLAGS:(.*?)(?=\n[A-Z]+:|$)',
            r'WARNING SIGNS:(.*?)(?=\n[A-Z]+:|$)',
            r'CONCERNS:(.*?)(?=\n[A-Z]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                flags_text = match.group(1)
                # Extract bullet points
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', flags_text)
                red_flags.extend([point.strip() for point in bullet_points])

        return red_flags[:4]  # Return top 4 red flags

    @staticmethod
    def extract_recommendation(text: str) -> str:
        """
        Extract recommendation from enhanced analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Recommendation text
        """
        patterns = [
            r'FINAL_RECOMMENDATION:(.*?)(?=\n[A-Z_]+:|$)',
            r'RECOMMENDATION:(.*?)(?=\n[A-Z]+:|$)',
            r'CONCLUSION:(.*?)(?=\n[A-Z]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                recommendation = match.group(1).strip()
                # Clean up the recommendation
                recommendation = re.sub(r'\n+', ' ', recommendation)
                recommendation = re.sub(r'\s+', ' ', recommendation)
                return recommendation[:300]  # Limit length

        return "Further verification recommended through multiple sources"

    @staticmethod
    def extract_confidence_level(text: str) -> str:
        """
        Extract confidence level from analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Confidence level (HIGH, MEDIUM, LOW)
        """
        patterns = [
            r'CONFIDENCE LEVEL:\s*(HIGH|MEDIUM|LOW)',
            r'CONFIDENCE:\s*(HIGH|MEDIUM|LOW)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        return "MEDIUM"

    @staticmethod
    def extract_reasoning_chain(text: str) -> str:
        """
        Extract reasoning chain from analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Reasoning chain
        """
        patterns = [
            r'REASONING_CHAIN:(.*?)(?=\n[A-Z_]+:|$)',
            r'COMPREHENSIVE_REASONING:(.*?)(?=\n[A-Z_]+:|$)',
            r'FINAL_ASSESSMENT:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                reasoning = match.group(1).strip()
                reasoning = re.sub(r'\n+', ' ', reasoning)
                reasoning = re.sub(r'\s+', ' ', reasoning)
                return reasoning[:400]  # Limit length

        return "Analysis completed using advanced AI reasoning"

    @staticmethod
    def extract_cross_modal_consistency(text: str) -> str:
        """
        Extract cross-modal consistency assessment

        Args:
            text (str): Analysis text

        Returns:
            str: Consistency assessment
        """
        pattern = r'CROSS_MODAL_CONSISTENCY:\s*(CONSISTENT|PARTIALLY_CONSISTENT|INCONSISTENT)'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).replace('_', ' ')

        return "Not Assessed"

    @classmethod
    def parse_analysis(cls, analysis_text: str) -> Dict[str, Any]:
        """
        Parse complete enhanced analysis text into structured data

        Args:
            analysis_text (str): Raw analysis text from Gemini 2.5

        Returns:
            Dict[str, Any]: Structured analysis data
        """
        return {
            'score': cls.extract_score(analysis_text),
            'classification': cls.extract_classification(analysis_text),
            'confidence_level': cls.extract_confidence_level(analysis_text),
            'key_findings': cls.extract_key_findings(analysis_text),
            'evidence': cls.extract_evidence(analysis_text),
            'red_flags': cls.extract_red_flags(analysis_text),
            'recommendation': cls.extract_recommendation(analysis_text),
            'reasoning_chain': cls.extract_reasoning_chain(analysis_text),
            'cross_modal_consistency': cls.extract_cross_modal_consistency(analysis_text),
            'raw_analysis': analysis_text
        }

    @staticmethod
    def get_confidence_level(score: int) -> str:
        """
        Get confidence level based on score

        Args:
            score (int): Authenticity score (0-100)

        Returns:
            str: Confidence level description
        """
        if score >= 85:
            return "Very High Confidence"
        elif score >= 70:
            return "High Confidence"
        elif score >= 55:
            return "Medium Confidence"
        elif score >= 40:
            return "Low Confidence"
        else:
            return "Very Low Confidence"

    @staticmethod
    def get_risk_level(classification: str, score: int) -> str:
        """
        Get enhanced risk level for sharing/believing content

        Args:
            classification (str): Content classification
            score (int): Authenticity score

        Returns:
            str: Risk level description
        """
        if classification == "FAKE" or score < 25:
            return "Critical Risk - Do Not Share or Believe"
        elif classification == "SUSPICIOUS" or score < 50:
            return "High Risk - Verify Through Multiple Sources"
        elif score < 70:
            return "Medium Risk - Additional Verification Recommended"
        elif classification == "AUTHENTIC" and score >= 85:
            return "Low Risk - Content Appears Reliable"
        else:
            return "Medium Risk - Consider Additional Verification"
