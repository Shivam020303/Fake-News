
"""
Enhanced Result Parser with Clear Categorization
Provides precise REAL/FAKE/PARTIALLY MANIPULATED classification
"""

import re
from typing import Dict, Any, List, Optional

class ResultParser:
    """Enhanced parser with clear, specific categorization"""

    @staticmethod
    def extract_score(text: str) -> int:
        """Extract authenticity score with enhanced precision"""
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

        return 50  # Default middle score if no score found

    @staticmethod
    def extract_classification(text: str) -> str:
        """
        Extract precise classification with clear categorization
        Returns: AUTHENTIC, FAKE, SUSPICIOUS (mapped to REAL/FAKE/PARTIALLY MANIPULATED)
        """
        text_lower = text.lower()

        # Check for explicit classifications first
        classification_patterns = [
            r'(?:CLASSIFICATION|FINAL CLASSIFICATION):\s*(AUTHENTIC|SUSPICIOUS|FAKE)',
            r'(?:ASSESSMENT|FINAL ASSESSMENT):\s*(AUTHENTIC|SUSPICIOUS|FAKE)'
        ]

        for pattern in classification_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                return match.group(1).upper()

        # Enhanced keyword analysis for more precise detection
        authentic_indicators = [
            'authentic', 'genuine', 'real', 'credible', 'trustworthy', 'verified',
            'accurate', 'legitimate', 'reliable', 'factual', 'true'
        ]

        fake_indicators = [
            'fake', 'false', 'fabricated', 'misleading', 'deceptive', 'manipulated',
            'synthetic', 'generated', 'doctored', 'altered', 'forged', 'hoax'
        ]

        suspicious_indicators = [
            'suspicious', 'questionable', 'uncertain', 'dubious', 'partial',
            'mixed', 'inconclusive', 'requires verification', 'unclear'
        ]

        # Count weighted occurrences
        authentic_score = sum(2 if indicator in text_lower else 0 for indicator in authentic_indicators)
        fake_score = sum(2 if indicator in text_lower else 0 for indicator in fake_indicators)
        suspicious_score = sum(1 if indicator in text_lower else 0 for indicator in suspicious_indicators)

        # Determine classification with threshold
        if fake_score >= 4 or (fake_score > authentic_score and fake_score > suspicious_score):
            return "FAKE"
        elif authentic_score >= 4 or (authentic_score > fake_score and authentic_score > suspicious_score):
            return "AUTHENTIC"
        elif suspicious_score > 0 or abs(authentic_score - fake_score) <= 2:
            return "SUSPICIOUS"

        return "SUSPICIOUS"  # Default to suspicious if unclear

    @staticmethod
    def get_clear_category(classification: str, score: int) -> str:
        """
        Map AI classification to clear user categories

        Args:
            classification (str): AI classification
            score (int): Confidence score

        Returns:
            str: Clear category (REAL, FAKE, PARTIALLY MANIPULATED)
        """
        if classification == "AUTHENTIC" and score >= 75:
            return "REAL"
        elif classification == "FAKE" or score < 25:
            return "FAKE"
        else:
            return "PARTIALLY MANIPULATED"

    @staticmethod
    def extract_key_findings(text: str) -> List[str]:
        """Extract key findings with enhanced patterns"""
        findings = []

        patterns = [
            r'KEY_TOPICS_EXTRACTED:(.*?)(?=\n[A-Z_]+:|$)',
            r'KEY FINDINGS:(.*?)(?=\n[A-Z]+:|$)',
            r'VISUAL EVIDENCE:(.*?)(?=\n[A-Z]+:|$)',
            r'TECHNICAL_ANALYSIS:(.*?)(?=\n[A-Z_]+:|$)',
            r'TEXT_ANALYSIS_SUMMARY:(.*?)(?=\n[A-Z_]+:|$)',
            r'IMAGE_ANALYSIS_SUMMARY:(.*?)(?=\n[A-Z_]+:|$)',
            r'DETECTION_FACTORS:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                findings_text = match.group(1)
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', findings_text)
                findings.extend([point.strip() for point in bullet_points])

        # Remove duplicates while preserving order
        seen = set()
        unique_findings = []
        for finding in findings:
            if finding.lower() not in seen:
                seen.add(finding.lower())
                unique_findings.append(finding)

        return unique_findings[:6]  # Return top 6 unique findings

    @staticmethod
    def extract_evidence(text: str) -> List[str]:
        """Extract supporting evidence with enhanced detection"""
        evidence = []

        patterns = [
            r'SUPPORTING_EVIDENCE:(.*?)(?=\n[A-Z_]+:|$)',
            r'FACT_CHECK_RESULTS:(.*?)(?=\n[A-Z_]+:|$)',
            r'EVIDENCE_COMPILATION:(.*?)(?=\n[A-Z_]+:|$)',
            r'VERIFICATION_RESULTS:(.*?)(?=\n[A-Z_]+:|$)',
            r'SOURCE_VERIFICATION:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                evidence_text = match.group(1)
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', evidence_text)
                evidence.extend([point.strip() for point in bullet_points])

        return evidence[:4]  # Return top 4 evidence points

    @staticmethod
    def extract_red_flags(text: str) -> List[str]:
        """Extract red flags with enhanced detection"""
        red_flags = []

        patterns = [
            r'RED_FLAGS_DETECTED:(.*?)(?=\n[A-Z_]+:|$)',
            r'RED FLAGS:(.*?)(?=\n[A-Z]+:|$)',
            r'WARNING_SIGNS:(.*?)(?=\n[A-Z_]+:|$)',
            r'MANIPULATION_INDICATORS:(.*?)(?=\n[A-Z_]+:|$)',
            r'SUSPICIOUS_ELEMENTS:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                flags_text = match.group(1)
                bullet_points = re.findall(r'[-•*]\s*([^\n]+)', flags_text)
                red_flags.extend([point.strip() for point in bullet_points])

        return red_flags[:4]  # Return top 4 red flags

    @staticmethod
    def extract_recommendation(text: str) -> str:
        """Extract actionable recommendation"""
        patterns = [
            r'FINAL_RECOMMENDATION:(.*?)(?=\n[A-Z_]+:|$)',
            r'RECOMMENDATION:(.*?)(?=\n[A-Z]+:|$)',
            r'SUGGESTED_ACTION:(.*?)(?=\n[A-Z_]+:|$)',
            r'NEXT_STEPS:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                recommendation = match.group(1).strip()
                recommendation = re.sub(r'\n+', ' ', recommendation)
                recommendation = re.sub(r'\s+', ' ', recommendation)
                return recommendation[:250]

        return "Verify through multiple authoritative sources before sharing or believing this content."

    @staticmethod
    def extract_confidence_level(text: str) -> str:
        """Extract AI confidence level"""
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
        """Extract detailed reasoning with enhanced detection"""
        patterns = [
            r'REASONING_CHAIN:(.*?)(?=\n[A-Z_]+:|$)',
            r'COMPREHENSIVE_REASONING:(.*?)(?=\n[A-Z_]+:|$)',
            r'ANALYSIS_LOGIC:(.*?)(?=\n[A-Z_]+:|$)',
            r'WHY_CLASSIFICATION:(.*?)(?=\n[A-Z_]+:|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                reasoning = match.group(1).strip()
                reasoning = re.sub(r'\n+', ' ', reasoning)
                reasoning = re.sub(r'\s+', ' ', reasoning)
                return reasoning[:500]

        return "Analysis completed using advanced AI reasoning with cross-source verification."

    @staticmethod
    def extract_cross_modal_consistency(text: str) -> str:
        """Extract cross-modal consistency assessment"""
        pattern = r'CROSS_MODAL_CONSISTENCY:\s*(CONSISTENT|PARTIALLY_CONSISTENT|INCONSISTENT)'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).replace('_', ' ')

        return "Not Assessed"

    @classmethod
    def parse_analysis(cls, analysis_text: str) -> Dict[str, Any]:
        """
        Parse analysis with enhanced categorization

        Args:
            analysis_text (str): Raw analysis from Gemini 2.5

        Returns:
            Dict[str, Any]: Structured analysis with clear categorization
        """
        score = cls.extract_score(analysis_text)
        classification = cls.extract_classification(analysis_text)
        clear_category = cls.get_clear_category(classification, score)

        return {
            'score': score,
            'classification': classification,
            'clear_category': clear_category,
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
        """Get user-friendly confidence level"""
        if score >= 90:
            return "Extremely High Confidence"
        elif score >= 80:
            return "High Confidence"
        elif score >= 65:
            return "Good Confidence"
        elif score >= 50:
            return "Medium Confidence"
        elif score >= 35:
            return "Low Confidence"
        else:
            return "Very Low Confidence"

    @staticmethod
    def get_risk_level(classification: str, score: int) -> str:
        """Get clear risk assessment for sharing"""
        clear_category = ResultParser.get_clear_category(classification, score)

        if clear_category == "FAKE":
            return "High Risk - Do Not Share"
        elif clear_category == "PARTIALLY MANIPULATED":
            return "Medium Risk - Verify Before Sharing"
        elif clear_category == "REAL" and score >= 85:
            return "Low Risk - Appears Reliable"
        else:
            return "Medium Risk - Additional Verification Recommended"
