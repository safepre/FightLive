import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.x import extract_scorecard

@pytest.fixture
def sample_tweets():
    return [
        "#UFC305 Official Scorecard: Israel Adesanya vs Dricus du Plessis (@DricusduPlessis) \n\nComplete Perth Scorecards ➡️: https://ufc.com/news/official-judges-scorecards-ufc-305-du-plessis-vs-adesanya \n\n@WestAustralia| #WAtheDreamState",
        "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest. \n\nBout ends at :15 of Round 2 due to accidental foul (groin strike). \n\nComplete Results: https://ufc.ac/45zUhWl \n\nComplete Scorecards: https://ufc.com/news/official-scorecards-ufc-294-makhachev-vs-volkanovski-2 \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
        "#UFC306 Official Scorecard: Sean O’Malley vs Merab Dvalishvili (@MerabDvalishvil) \n\nComplete Scorecards From @RiyadhSeason#NocheUFC ➡️: https://ufc.com/news/official-"
    ]

def test_extract_official_results(sample_tweets):
    result = extract_scorecard(sample_tweets[0])
    expected = "#UFC305 Official Scorecard: Israel Adesanya vs Dricus du Plessis (@DricusduPlessis)"
    assert result == expected

def test_extract_no_contest(sample_tweets):
    result = extract_scorecard(sample_tweets[1])
    expected = "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest."
    assert result == expected

def test_extract_split_draw(sample_tweets):
    result = extract_scorecard(sample_tweets[2])
    expected = "#UFC306 Official Scorecard: Sean O’Malley vs Merab Dvalishvili (@MerabDvalishvil)"
    assert result == expected