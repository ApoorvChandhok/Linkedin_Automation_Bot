import re

def handle_experience_question(label: str, options: list[str], skill_experience: dict, default_experience: str, min_experience_for_unknown_skills: str) -> str:
    """
    Extracts the skill from the question label and matches it against the skill_experience dict.
    Returns the years of experience as a string.
    """
    label_lower = label.lower()
    
    # Try to find a matching skill in the dictionary
    for skill, years in skill_experience.items():
        # Match standalone words using word boundaries to avoid partial matches like 'api' in 'capital'
        if re.search(r'\b' + re.escape(skill) + r'\b', label_lower):
            return str(years)
            
    # If no skill matches, check if the question generally asks for "experience"
    if 'experience' in label_lower or 'years' in label_lower:
        # If it specifically asks for a skill ('experience with X' or 'experience in X') but we don't have it listed
        if ' in ' in label_lower or ' with ' in label_lower:
            return str(min_experience_for_unknown_skills)
        return str(default_experience)
        
    return ""

def handle_categorical_question(label: str, options: list[str], categorical_answers: dict) -> str:
    """
    Maps standard personal/categorical questions (Visa, Clearance, EEO, etc.) to their answers.
    Returns the exact option text if a match is found based on the answer mapping.
    """
    label_lower = label.lower()
    
    # Check for direct mapping
    for keywords, mapped_answer in categorical_answers.items():
        if any(keyword in label_lower for keyword in keywords):
            # Mapped answer defines the intent (e.g., "Yes", "No", "Decline")
            # We now must find the closest matching option text
            for option in options:
                if mapped_answer.lower() in option.lower():
                    return option
            
            # Special case for "Decline"
            if mapped_answer == "Decline":
                phrases = ["Decline", "not wish", "don't wish", "Prefer not", "not want"]
                for phrase in phrases:
                    for option in options:
                        if phrase.lower() in option.lower():
                            return option
                            
            # Return the mapped answer directly if exact match not found but it might still work
            return mapped_answer
            
    return ""

def handle_personal_info_question(label: str, personal_info: dict) -> str:
    """
    Extracts text answers to personal info inputs (name, phone, address).
    """
    label_lower = label.lower()
    
    if 'phone' in label_lower or 'mobile' in label_lower: return personal_info.get("phone_number", "")
    if 'street' in label_lower: return personal_info.get("street", "")
    if 'city' in label_lower or 'location' in label_lower or 'address' in label_lower: return personal_info.get("current_city", "")
    if 'signature' in label_lower: return personal_info.get("full_name", "")
    if 'name' in label_lower:
        if 'full' in label_lower: return personal_info.get("full_name", "")
        if 'first' in label_lower and 'last' not in label_lower: return personal_info.get("first_name", "")
        if 'middle' in label_lower and 'last' not in label_lower: return personal_info.get("middle_name", "")
        if 'last' in label_lower and 'first' not in label_lower: return personal_info.get("last_name", "")
        if 'employer' in label_lower: return personal_info.get("recent_employer", "")
        return personal_info.get("full_name", "")
    if 'notice' in label_lower:
        if 'month' in label_lower: return str(personal_info.get("notice_period_months", ""))
        if 'week' in label_lower: return str(personal_info.get("notice_period_weeks", ""))
        return str(personal_info.get("notice_period", ""))
    if 'linkedin' in label_lower: return personal_info.get("linkedIn", "")
    if 'website' in label_lower or 'blog' in label_lower or 'portfolio' in label_lower or 'link' in label_lower: return personal_info.get("website", "")
    if 'scale of 1-10' in label_lower: return str(personal_info.get("confidence_level", ""))
    if 'headline' in label_lower: return personal_info.get("linkedin_headline", "")
    if 'state' in label_lower or 'province' in label_lower: return personal_info.get("state", "")
    if 'zip' in label_lower or 'postal' in label_lower or 'code' in label_lower: return str(personal_info.get("zipcode", ""))
    if 'country' in label_lower: return personal_info.get("country", "")
    
    return ""
