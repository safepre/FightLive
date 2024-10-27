import pytest
from src.text_processing import extract_official_results

@pytest.fixture
def sample_tweets():
    return [
        "#UFC306 Official Result ➡️: Merab Dvalishvili (49-46, 48-47, 48-47 | @MerabDvalishvil) defeats Sean O'Malley by Unanimous Decision. \n\n@RiyadhSeason\n | #NocheUFC",
        "#UFC282 Official Result: Jan Blachowicz and Magomed Ankalaev fight to a Split Draw (48-47, 46-48, 47-47). \n\nAll Fight Results ⬇️: https://ufc.ac/45zUhWl",
        "#UFCAustin Official Result: Damir Ismagulov (28-28, 29-28, 30-27) defeats Guram Kutateladze by Majority Decision",
        "🇬🇧#UFC304 Official Result: Paddy Pimblett defeats King Green by Technical Submission, Triangle Choke, Round 1, 3:22 \n\nLive Results, Interviews & More: https://ufc.ac/3Yf3F1M Live Results, Interviews & More: https://ufc.ac/3Yf3F1M",

    ]

def test_extract_official_results(sample_tweets):
    result = extract_official_results(sample_tweets[0])
    expected = ["#UFC306 Official Result ➡️: Merab Dvalishvili (49-46, 48-47, 48-47 | @MerabDvalishvil) defeats Sean O'Malley by Unanimous Decision."]
    assert result == expected

def test_extract_no_contest(sample_tweets):
    result = extract_official_results(sample_tweets[1])
    expected = ["#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest."]
    assert result == expected

def test_extract_split_draw(sample_tweets):
    result = extract_official_results(sample_tweets[2])
    expected = ["#UFC282 Official Result: Jan Blachowicz and Magomed Ankalaev fight to a Split Draw (48-47, 46-48, 47-47)."]
    assert result == expected

def test_extract_majority_decision(sample_tweets):
    result = extract_official_results(sample_tweets[3])
    expected = ["#UFCAustin Official Result: Damir Ismagulov (28-28, 29-28, 30-27) defeats Guram Kutateladze by Majority Decision"]
    assert result == expected

def test_extract_round_one_finish(sample_tweets):
    result = extract_official_results(sample_tweets[4])
    expected = ["#UFC304 Official Result: Paddy Pimblett defeats King Green by Technical Submission, Triangle Choke, Round 1, 3:22"]
    assert result == expected