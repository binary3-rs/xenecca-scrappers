# patterns
# -
# _
# capital letter
# prefix capital letter
from config.constants import DASH_PATTERN, UNDERSCORE_PATTERN, CAPITAL_LETTERS_PATTERN

PREFIX_PATTERNS = []
SUFFIX_PATTERNS = []


def determine_resource_name_by_filename(filename, filename_pattern):
    if filename_pattern in (DASH_PATTERN, UNDERSCORE_PATTERN):
        return " ".join(filename.split(filename_pattern))
    elif filename_pattern == CAPITAL_LETTERS_PATTERN:
        return _determine_resource_name_with_capital_pattern(filename)
    return filename


def determine_category_name_by_filename(filename, categories):
    filename = filename.lower()
    for cat_name, cat_obj in categories.items():
        if cat_obj.name.lower() in filename:
            return cat_obj
        if cat_obj.tags is None:
            continue
        for tag in cat_obj.tags.split(','):
            tag = tag.lower().strip()
            if tag in filename:
                return cat_obj
    return None


def _determine_resource_name_with_capital_pattern(filename):
    words = []
    i = 0
    while i < len(filename):
        start = i

        if filename[i:i + 3].upper() in ("PHP", "CSS", "SQL"):
            i += 3
        elif filename[i:i + 5].upper() in ("HTML5",):
            i += 5
        elif filename[i:i + 4].upper() in ("HTML",):
            i += 4
        elif filename[i:i + 6].upper() in ("MATLAB",):
            i += 6
        if start != i:
            words.append(filename[start:i])
            continue
        i += 1
        while i < len(filename) and (filename[i].isdigit() or filename[i].islower()):
            i += 1
        words.append(filename[start:i])
    return " ".join(words)
