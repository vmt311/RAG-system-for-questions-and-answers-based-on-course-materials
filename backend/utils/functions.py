import re

def preprocess_text(text):
    # Define the pattern for special characters to remove
    text = re.sub(r'[=]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
