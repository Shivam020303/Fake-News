
"""
Result Parser for Fake News Detection Analysis
Parses and structures analysis results from Gemini API
"""

import re
from typing import Dict, Any, List, Optional

class ResultParser:
    """Parser for structuring analysis results"""

    @staticmethod
    def extract_score(text: str) -> int:
        """
        Extract authenticity score from analysis text

        Args:
            text (str): Analysis text

        Returns:
            int: Extracted score (0-100)
        """
        # Look for patterns like "SCORE: 85" or "85/100" or "Score: 85"
        score_patterns = [
            r'(?:SCORE|Score):\s*(\d{1,3})',
            r'(\d{1,3})/100',
            r'(\d{1,3})%',
            r'(\d{1,3})\s*(?:out of 100|/ 100)'
        ]

        for pattern in score_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return min(max(score, 0), 100)  # Ensure score is between 0-100

        return 0

    @staticmethod
    def extract_classification(text: str) -> str:
        """
        Extract classification from analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Classification (AUTHENTIC, SUSPICIOUS, FAKE, or UNCERTAIN)
        """
        text_lower = text.lower()

        # Check for explicit classifications
        if re.search(r'classification:\s*authentic', text_lower):
            return "AUTHENTIC"
        elif re.search(r'classification:\s*fake', text_lower):
            return "FAKE"
        elif re.search(r'classification:\s*suspicious', text_lower):
            return "SUSPICIOUS"

        # Check for keywords indicating authenticity
        authentic_keywords = ['authentic', 'genuine', 'real', 'credible', 'trustworthy']
        fake_keywords = ['fake', 'false', 'fabricated', 'misleading', 'deceptive']
        suspicious_keywords = ['suspicious', 'questionable', 'uncertain', 'dubious']

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
        Extract key findings from analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of key findings
        """
        findings = []

        # Look for sections with findings
        patterns = [
            r'KEY FINDINGS:(.*?)(?=\n[A-Z]+:|$)',
            r'FINDINGS:(.*?)(?=\n[A-Z]+:|$)',
            r'ANALYSIS:(.*?)(?=\n[A-Z]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                findings_text = match.group(1)
                # Extract bullet points
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', findings_text)
                findings.extend([point.strip() for point in bullet_points])

        return findings[:5]  # Return top 5 findings

    @staticmethod
    def extract_evidence(text: str) -> List[str]:
        """
        Extract evidence from analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of evidence points
        """
        evidence = []

        # Look for evidence sections
        patterns = [
            r'EVIDENCE:(.*?)(?=\n[A-Z]+:|$)',
            r'SUPPORTING EVIDENCE:(.*?)(?=\n[A-Z]+:|$)',
            r'VERIFICATION:(.*?)(?=\n[A-Z]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                evidence_text = match.group(1)
                # Extract bullet points
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', evidence_text)
                evidence.extend([point.strip() for point in bullet_points])

        return evidence[:3]  # Return top 3 evidence points

    @staticmethod
    def extract_red_flags(text: str) -> List[str]:
        """
        Extract red flags from analysis text

        Args:
            text (str): Analysis text

        Returns:
            List[str]: List of red flags
        """
        red_flags = []

        # Look for red flags sections
        patterns = [
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

        return red_flags[:3]  # Return top 3 red flags

    @staticmethod
    def extract_recommendation(text: str) -> str:
        """
        Extract recommendation from analysis text

        Args:
            text (str): Analysis text

        Returns:
            str: Recommendation text
        """
        patterns = [
            r'RECOMMENDATION:(.*?)(?=\n[A-Z]+:|$)',
            r'FINAL RECOMMENDATION:(.*?)(?=\n[A-Z]+:|$)',
            r'CONCLUSION:(.*?)(?=\n[A-Z]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                recommendation = match.group(1).strip()
                # Clean up the recommendation
                recommendation = re.sub(r'\n+', ' ', recommendation)
                recommendation = re.sub(r'\s+', ' ', recommendation)
                return recommendation[:200]  # Limit length

        return "Further verification recommended"

    @classmethod
    def parse_analysis(cls, analysis_text: str) -> Dict[str, Any]:
        """
        Parse complete analysis text into structured data

        Args:
            analysis_text (str): Raw analysis text from Gemini

        Returns:
            Dict[str, Any]: Structured analysis data
        """
        return {
            'score': cls.extract_score(analysis_text),
            'classification': cls.extract_classification(analysis_text),
            'key_findings': cls.extract_key_findings(analysis_text),
            'evidence': cls.extract_evidence(analysis_text),
            'red_flags': cls.extract_red_flags(analysis_text),
            'recommendation': cls.extract_recommendation(analysis_text),
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
        if score >= 80:
            return "High Confidence"
        elif score >= 60:
            return "Medium Confidence"
        elif score >= 40:
            return "Low Confidence"
        else:
            return "Very Low Confidence"

    @staticmethod
    def get_risk_level(classification: str, score: int) -> str:
        """
        Get risk level for sharing/believing content

        Args:
            classification (str): Content classification
            score (int): Authenticity score

        Returns:
            str: Risk level description
        """
        if classification == "FAKE" or score < 30:
            return "High Risk - Do Not Share"
        elif classification == "SUSPICIOUS" or score < 60:
            return "Medium Risk - Verify Before Sharing"
        elif classification == "AUTHENTIC" and score >= 80:
            return "Low Risk - Likely Reliable"
        else:
            return "Medium Risk - Additional Verification Recommended"
