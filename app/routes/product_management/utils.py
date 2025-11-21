import re
from .validation import PART_ONE_LENGTH, PART_TWO_LENGTH, PART_THREE_LENGTH

def _is_valid_checksum(part2):
    if not part2.isdigit():
        return False
    return sum(int(digit) for digit in part2) > 20

def validate_string_format(text):
    parts = text.split('-')
    if len(parts) != 3:
        return False
    
    part1, part2, part3 = parts[0], parts[1], parts[2]

    if not (len(part1) == PART_ONE_LENGTH and part1.isalpha() and part1.isupper()):
        return False

    if not (len(part2) == PART_TWO_LENGTH and _is_valid_checksum(part2)):
        return False

    if not (len(part3) == PART_THREE_LENGTH and part3.isalnum()):
        return False
    if not (re.search('[a-zA-Z]', part3) and re.search('[0-9]', part3)):
        return False
    if part3[0].upper() != part1[-1]:
        return False
        
    return True


