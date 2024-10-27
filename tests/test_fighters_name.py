import pytest
from src.text_processing import extract_fighter_names

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
        "#UFC307 Official Scorecard: Julianna Peña vs Raquel Pennington \n\nComplete Results ➡️ https://ufc.ac/3NeEXrK"
    ]

def test_extract_fighter_names(sample_tweets):
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
        ("Julianna Peña", "Raquel Pennington")
    ]
    
    for tweet, expected in zip(sample_tweets, expected_results):
        result = extract_fighter_names(tweet)
        assert result == expected, f"Expected: {expected}\nGot: {result}"
