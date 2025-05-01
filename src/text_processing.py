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

def extract_scorecard_names(text):

    patterns = [
        r'(?:Scorecard|Result):\s*([\w\s\'\’\-\.]+?)\s+(?:vs\.?|and)\s+([\w\s\'\’\-\.\u0100-\uFFFF]+?)(?=\s*(?:\(|$|\n|[^\w\s\-\.]))',
        r'([\w\s\'\’\-\.]+?)\s+(?:\(@\w+\))?\s+(?:vs\.?|and)\s+([\w\s\’\'\-\.\u0100-\uFFFF]+?)(?=\s*(?:\n\n|$|\n|👇))',
        r'([\w\s\'\’\-\.]+?)(?:\s+\(@\w+\))?\s+(?:vs\.?|and)\s+([\w\s\’\'\-\.\u0100-\uFFFF]+?)(?=\s*(?:$|\n))'
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
    if re.search(r'#UFC\w+\s+[Oo]ff?i?c?i?a?l?\s+[Ss]corecard(?:s)?(?:\s|:)', text, re.IGNORECASE):
        print("Skipping scorecard tweet")
        return ""

    patterns = [
        r"#UFC\d+\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult:\s*[\w\s\'\-\.]+?\s*\(@[\w\s\-,]+\s+[\d\-,\s]+\)\s+defeats\s+[\w\s\-\'\.]+?\s+by\s+(?:Split|Unanimous)\s*Decision",
        
        r"^[^#\n]*?(#UFC(?:\d+|\w+)\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult:.*?)(?=\n|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result = match.group(0) if match.groups() == () else match.group(1)
            result = result.strip()
            if not any(word in result.upper() for word in ['SCORECARD', 'SCORECARDS']):
                print(f"Found valid result: {result}")
                return result
            
    print(f"No valid result found in: {text[:100]}...")
    return ""

def extract_scorecard(tweet_text):
    # Made pattern more flexible to handle typos and case variations
    pattern = r"^[^#\n]*?(#UFC(?:\d+|\w+)\s+[Oo]ff?i?c?i?a?l?\s+(?:(?:[Rr]esult\s+&\s+)?[Ss]corecard).*?)(?=\n|$)"
    match = re.search(pattern, tweet_text)
    if match:
        return match.group(1).strip()
    return None

def load_submission_types(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().lower() for line in f]

def find_all_submissions(tweets, submission_types_file):
    submission_types = load_submission_types(submission_types_file)
    found_submissions = set()
    for tweet in tweets:
        tweet_lower = tweet.lower()
        for submission_type in submission_types:
            if submission_type in tweet_lower:
                found_submissions.add(submission_type)
    return list(found_submissions)

def find_submission(tweets, submission_types_file):
    submission_types = load_submission_types(submission_types_file)
    found_submissions = set()
    for tweet in tweets:
        tweet_lower = tweet.lower()
        for submission_type in submission_types:
            if submission_type in tweet_lower:
                found_submissions.add(submission_type)
    submissions_list = list(found_submissions)
    return submissions_list[0] if submissions_list else None

def extract_result_names(text):
    pattern = r"#UFC\w+\s+Official\s+Result:\s*([\w\s\'\’\-\.]+?)\s+\(@\w+\s+[\d\-,\s]+\)\s+defeats\s*([\w\s\'\’\-\.]+?)\s+by"
    match = re.search(pattern, text)
    if match:
        winner, loser = match.groups()
        return (clean_name(winner), clean_name(loser))
    return None

def is_first_round_finish(text):
    # Should return True only if there's a finish (KO, TKO, Submission) in Round 1
    pattern = r"(?:KO|TKO|Submission).*?Round 1"
    return bool(re.search(pattern, text, re.IGNORECASE))

def extract_result_fighters(text):
    """
    Extracts fighter names from an official result tweet.
    Handles multiple formats of result tweets including no contests.
    """
    patterns = [
        # Pattern for tweets with Twitter handle after first fighter
        r"#UFC\w+\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult:\s*([\w\s\'\-\.]+?)\s*\(@[\w\s\-,]+\)\s+defeats\s+([\w\s\'\-\.]+?)(?:\s+by|\s*👇|\s*$)",
        # Pattern for tweets without Twitter handle
        r"#UFC\w+\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult:\s*([\w\s\'\-\.]+?)\s+defeats\s+([\w\s\'\-\.]+?)(?:\s+by|\s*👇|\s*$)",
        # Pattern for tweets with Twitter handle after second fighter
        r"#UFC\w+\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult:\s*([\w\s\'\-\.]+?)\s+defeats\s+([\w\s\'\-\.]+?)\s*\(@[\w\s\-,]+\)",
        # Pattern for no contest results
        r"#UFC\w+\s+[Oo]ff?i?c?i?a?l?\s+[Rr]esult(?:\s*&\s*[Ss]corecard)?:\s*([\w\s\'\-\.]+?)\s+vs\s+([\w\s\'\-\.]+?)\s+ruled\s+a\s+no\s+contest"
    ]
    
    first_line = text.split('\n')[0]
    for pattern in patterns:
        match = re.search(pattern, first_line, re.IGNORECASE)
        if match:
            fighter1, fighter2 = match.groups()
            fighter1 = clean_name(fighter1)
            fighter2 = clean_name(fighter2)
            return (fighter1, fighter2)
    
    print(f"No fighters found in result tweet: {first_line}")
    return None

def extract_first_names(tuple_of_names):
    """
    Extracts first names of the fighters from a tuple of full names.
    Returns a tuple of lowercase first names or None if input is invalid.
    """
    if tuple_of_names is None:
        return None
        
    first_name1 = tuple_of_names[0].split()[0].lower()
    first_name2 = tuple_of_names[1].split()[0].lower()
    
    return (first_name1, first_name2)


