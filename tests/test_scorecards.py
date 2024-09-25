import pytest
from src.text_processing import extract_scorecard

@pytest.fixture
def sample_tweets():
    return [
        "#UFC305 Official Scorecard: Israel Adesanya vs Dricus du Plessis (@DricusduPlessis) \n\nComplete Perth Scorecards ➡️: https://ufc.com/news/official-judges-scorecards-ufc-305-du-plessis-vs-adesanya \n\n@WestAustralia| #WAtheDreamState",
        "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest. \n\nBout ends at :15 of Round 2 due to accidental foul (groin strike). \n\nComplete Results: https://ufc.ac/45zUhWl \n\nComplete Scorecards: https://ufc.com/news/official-scorecards-ufc-294-makhachev-vs-volkanovski-2 \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
        "#UFC306 Official Scorecard: Sean O’Malley vs Merab Dvalishvili (@MerabDvalishvil) \n\nComplete Scorecards From @RiyadhSeason#NocheUFC ➡️: https://ufc.com/news/official-",
        "#UFCStLouis Official Scorecard: Diego Ferreira (@DiegoUFCTX) vs Mateusz Rębecki👇 \n\nAll Scorecards ➡️: https://ufc.com/news/official-",
        "#UFCAustin Official Result: Damir Ismagulov (28-28, 29-28, 30-27) defeats Guram Kutateladze by Majority Decision"
    ]

def test_extract_official_scorecard_from_perth(sample_tweets):
    result = extract_scorecard(sample_tweets[0])
    expected = "#UFC305 Official Scorecard: Israel Adesanya vs Dricus du Plessis (@DricusduPlessis)"
    assert result == expected

def test_extract_no_contest(sample_tweets):
    result = extract_scorecard(sample_tweets[1])
    expected = "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest."
    assert result == expected

def test_extract_official_scorecard_from_sphere(sample_tweets):
    result = extract_scorecard(sample_tweets[2])
    expected = "#UFC306 Official Scorecard: Sean O’Malley vs Merab Dvalishvili (@MerabDvalishvil)"
    assert result == expected

def test_extract_official_scorecards_from_st_louis(sample_tweets):
    result = extract_scorecard(sample_tweets[3])   
    expected = "#UFCStLouis Official Scorecard: Diego Ferreira (@DiegoUFCTX) vs Mateusz Rębecki👇"
    assert result == expected
  
def test_extract_majority_decision(sample_tweets):
    result = extract_scorecard(sample_tweets[4])
    assert result == None, f"This one should fail"