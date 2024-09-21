import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.x import extract_official_results

@pytest.fixture
def sample_tweets():
    return [
        "#UFC306 Official Result ➡️: Merab Dvalishvili (49-46, 48-47, 48-47 | @MerabDvalishvil) defeats Sean O'Malley by Unanimous Decision. \n\n@RiyadhSeason\n | #NocheUFC",
        "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest. \n\nBout ends at :15 of Round 2 due to accidental foul (groin strike). \n\nComplete Results: https://ufc.ac/45zUhWl \n\nComplete Scorecards: https://ufc.com/news/official-scorecards-ufc-294-makhachev-vs-volkanovski-2 \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
        "#UFC282 Official Result: Jan Blachowicz and Magomed Ankalaev fight to a Split Draw (48-47, 46-48, 47-47). \n\nAll Fight Results ⬇️: https://ufc.ac/45zUhWl"
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