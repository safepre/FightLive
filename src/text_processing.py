import re

def finish_by_round_one(text):
    pattern = r"by\s+((?:Technical\s+)?(?:TKO|KO|Submission))(?:,\s+[^,]+?)?(?:,?\s+(?:at|in)?\s*(?:\d+:\d+\s*(?:of|in))?\s*)?(?:Round|R)\s*1"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def extract_finish_method(text):
    pattern = r"by\s+((?:Technical\s+)?(?:TKO|KO|Submission))(?:,\s+[^,]+?)?(?:,?\s+(?:at|in)?\s*(?:\d+:\d+\s*(?:of|in))?\s*)?(?:Round|R)\s*1"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_fighter_names(text):
    patterns = [
        r'(?:Scorecard|Result):\s*([\w\s\'\-\.]+?)\s+(?:vs\.?|and)\s+([\w\s\'\-\.\u0100-\uFFFF]+?)(?=\s*(?:\(|$|\n|[^\w\s\-\.]))',
        r'([\w\s\'\-\.]+?)\s+(?:\(@\w+\))?\s+(?:vs\.?|and)\s+([\w\s\'\-\.\u0100-\uFFFF]+?)(?=\s*(?:\n\n|$|\n|👇))',
        r'([\w\s\'\-\.]+?)(?:\s+\(@\w+\))?\s+(?:vs\.?|and)\s+([\w\s\'\-\.\u0100-\uFFFF]+?)(?=\s*(?:👇|$|\n))'
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        if matches:
            name1, name2 = matches[0]
            return (clean_name(name1), clean_name(name2))

    return None

def clean_name(name):
    name = re.split(r'\s+ruled\s+a\s+', name)[0]
    name = re.sub(r'\(@\w+\)', '', name)
    name = re.sub(r'\n.*', '', name) 
    name = re.sub(r'[^\w\s\'\-\.\u0100-\uFFFF]', '', name)
    return name.strip()

def extract_official_results(text):
    pattern = r"(#UFC(?:\d+|\w+)\s+(?:Official\s+)?(?:Result|Scorecard).*?)(?=\n|$)"
    match = re.search(pattern, text)
    if match:
        return [match.group(1).strip()]
    return []

def extract_scorecard(tweet_text):
    pattern = r"(#UFC(?:\d+|\w+)\s+Official\s+(?:(?:Result\s+&\s+)?Scorecard).*?)(?=\n|$)"
    match = re.search(pattern, tweet_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None