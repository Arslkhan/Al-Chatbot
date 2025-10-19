"""
Language detection and translation utilities
"""
import re
from typing import Tuple


def detect_language(text: str) -> str:
    """
    Detect if text is Arabic or English
    
    Returns:
        'ar' for Arabic, 'en' for English
    """
    # Count Arabic characters
    arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
    total_chars = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', text))
    
    if total_chars == 0:
        return 'en'  # Default to English
    
    # If more than 30% Arabic characters, consider it Arabic
    if arabic_chars / total_chars > 0.3:
        return 'ar'
    
    return 'en'


def translate_if_needed(text: str, target_language: str) -> Tuple[str, str]:
    """
    Translate text if needed (placeholder for future translation API)
    
    Returns:
        (translated_text, detected_language)
    """
    detected = detect_language(text)
    
    # For MVP, we'll rely on GPT-4o-mini's multilingual capabilities
    # In the future, can integrate Google Translate API here
    
    return text, detected


# Common legal terms in Arabic for reference
ARABIC_LEGAL_TERMS = {
    'contract': 'عقد',
    'tenant': 'مستأجر',
    'landlord': 'مالك',
    'rent': 'إيجار',
    'lease': 'عقد إيجار',
    'property': 'عقار',
    'eviction': 'إخلاء',
    'deposit': 'تأمين',
    'maintenance': 'صيانة',
    'RERA': 'ريرا',
    'Dubai Land Department': 'دائرة الأراضي والأملاك في دبي',
}

