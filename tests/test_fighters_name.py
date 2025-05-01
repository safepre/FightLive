import pytest
import re
from src.text_processing import extract_scorecard_names ,extract_result_fighters, extract_first_names

@pytest.fixture
def sample_tweets():
    return [
        "#UFC305 Official Scorecard: Israel Adesanya vs Dricus du Plessis (@DricusduPlessis) \n\nComplete Perth Scorecards ➡️: https://ufc.com/news/official-judges-scorecards-ufc-305-du-plessis-vs-adesanya \n\n@WestAustralia| #WAtheDreamState",
        "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest. \n\nBout ends at :15 of Round 2 due to accidental foul (groin strike). \n\nComplete Results: https://ufc.ac/45zUhWl \n\nComplete Scorecards: https://ufc.com/news/official-scorecards-ufc-294-makhachev-vs-volkanovski-2 \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
        "#UFC306 Official Scorecard: Sean O'Malley vs Merab Dvalishvili (@MerabDvalishvil) \n\nComplete Scorecards From @RiyadhSeason#NocheUFC ➡️: https://ufc.com/news/official-",
        "#UFCStLouis Official Scorecard: Diego Ferreira (@DiegoUFCTX) vs Mateusz Rębecki👇 \n\nAll Scorecards ➡️: https://ufc.com/news/official-",
        "#UFCVegas87 Official Scorecard: Loik Radzhabov (@LoikRadzhabov) vs Abdul-Kareem Al-Selwady👇",
        "#UFC299 Official Scorecards: Gilbert Burns vs Jack Della Maddalena \n\nSee every scorecard here ➡️: https://ufc.com/news/official-",
        "#UFC267 Official Scorecard: Elizeu Zaleski dos Santos (@ElizeuCapoeira) vs Benoit Saint-Denis \n\nAll Scorecards: https://ufc.com/news/official-scorecards-ufc-267-dos-santos-vs-saint-denis",
        "#UFC297 Official Scorecard: Chris Curtis vs Marc-Andre Barriault 👇 \n\nAll Scorecards ➡️: https://ufc.com/news/official-",
        "#UFC306 Official Scorecard: Raul Rosas Jr. vs Aoriqileng \n\nComplete Scorecards From @RiyadhSeaso #NocheUFC ➡️: https://ufc.com/news/official-",
        "#UFCLongIsland Official Scorecards: Matt Schnell (@DANGER_Caged) vs Sumudaerji \n\nAll Long Island Scorecards ➡️: https://ufc.com/news/official-",
        "#UFC306 Official Scorecard: Sean O’Malley vs Merab Dvalishvili (@MerabDvalishvil)",
    ]

@pytest.fixture
def sample_tweets_with_result():
    return [
        "#UFC305 Official Result: Israel Adesanya defeats Dricus du Plessis (@DricusduPlessis) \n\nComplete Perth Scorecards ➡️: https://ufc.com/news/official-judges-scorecards-ufc-305-du-plessis-vs-adesanya \n\n@WestAustralia| #WAtheDreamState",
        "#UFC294 Official Result & Scorecard: Javid Basharat vs Victor Henry ruled a no contest. \n\nBout ends at :15 of Round 2 due to accidental foul (groin strike). \n\nComplete Results: https://ufc.ac/45zUhWl \n\nComplete Scorecards: https://ufc.com/news/official-scorecards-ufc-294-makhachev-vs-volkanovski-2 \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
        "#UFC306 Official Result: Sean O'Malley defeats Merab Dvalishvili (@MerabDvalishvil) \n\nComplete Scorecards From @RiyadhSeason#NocheUFC ➡️: https://ufc.com/news/official-",
        "#UFC297 Official Result: Chris Curtis defeats Marc-Andre Barriault 👇 \n\nAll Scorecards ➡️: https://ufc.com/news/official-",
        "#UFC306 Official Result: Raul Rosas Jr. defeats Aoriqileng \n\nComplete Scorecards From @RiyadhSeaso #NocheUFC ➡️: https://ufc.com/news/official-",

    ]
def test_extract_scorecard_names(sample_tweets):
    expected_results = [
        ("Israel Adesanya", "Dricus du Plessis"),
        ("Javid Basharat", "Victor Henry"),
        ("Sean O'Malley", "Merab Dvalishvili"),
        ("Diego Ferreira", "Mateusz Rębecki"),
        ("Loik Radzhabov", "Abdul-Kareem Al-Selwady"),
        ("Gilbert Burns", "Jack Della Maddalena"),
        ("Elizeu Zaleski dos Santos", "Benoit Saint-Denis"),
        ("Chris Curtis", "Marc-Andre Barriault"),
        ("Raul Rosas Jr.", "Aoriqileng"),
        ("Matt Schnell", "Sumudaerji"),
        ("Sean O’Malley", "Merab Dvalishvili"),
    ]

    for tweet, expected in zip(sample_tweets, expected_results):
        result = extract_scorecard_names(tweet)
        assert result == expected, f"Expected: {expected}\nGot: {result}"


def test_extract_first_names(sample_tweets_with_result):
    expected_results = [
        ("israel", "dricus"),
        ("javid", "victor"),
        ("sean", "merab"),
        ("chris", "marc-andre"),
        ("raul", "aoriqileng"),
    ]

    for tweet, expected in zip(sample_tweets_with_result, expected_results):
        result = extract_result_fighters(tweet)
        first_names = extract_first_names(result)
        assert first_names == expected, f"\nTweet: {tweet}\nExpected: {expected}\nGot: {first_names}\nExtracted result: {result}"