def validate_string_format(text):
    """
    Validates if the string is in the format 'xxxx-xxxxx-xxxxxx'.
    """
    parts = text.split('-')
    if len(parts) != 3:
        return False
    
    if len(parts[0]) != 4 or len(parts[1]) != 5 or len(parts[2]) != 6:
        return False
        
    return True


