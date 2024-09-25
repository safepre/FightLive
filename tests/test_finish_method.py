import pytest
from src.x import finish_by_round_one, extract_finish_method

@pytest.fixture
def sample_tweets():
    return [
        "#UFCVegas96 Official Result: Michael Morales defeats Neil Magny by TKO at 4:39 of Round 1 \n\nResults & More ➡️  https://ufc.ac/3Z0uF5p",
        "#UFC305 Official Result: Jesus Aguilar defeats Stewart Nicoll by Submission at 2:39 in Round 1. \n\nResults, Interviews & More ➡️: https://ufc.ac/3M7WQrl \n\n@WestAustralia | #WAtheDreamState",
        "#UFC303 Official Result: Payton Talbott (@PaytonTalbott) defeats Yanis Ghemmouri by KO, Round 1, :19 \n\nComplete Results ➡️: https://ufc.ac/3W23CEQ",
        "🇬🇧#UFC304 Official Result: Paddy Pimblett defeats King Green by Technical Submission, Triangle Choke, Round 1, 3:22 \n\nLive Results, Interviews & More: https://ufc.ac/3Yf3F1M Live Results, Interviews & More: https://ufc.ac/3Yf3F1M",
        "#UFC298 Official Result: Ilia Topuria (@TopuriaIlia) defeats Alexander Volkanovski by KO at 3:32 in Round 2. \n\nAll Fight Results ➡️: https://ufc.ac/3T278h1",
        "#UFC298 Official Result: Anthony Hernandez (@ilovebamf) defeats Roman Kopylov by Submission due to Rear Naked Choke at 3:23 in Round 2. \n\nAll Fight Results ➡️: https://ufc.ac/3T278h1",
        "#UFC298 Official Result: Marcos Rogerio de Lima (@Pezao011) defeats Junior Tafa by TKO at 1:14 in Round 2. \n\nAll Fight Results ➡️: https://ufc.ac/4bzUZr3"
    ]

def test_finish_by_round_one(sample_tweets):
    assert finish_by_round_one(sample_tweets[0]) == "by TKO at 4:39 of Round 1"
    assert finish_by_round_one(sample_tweets[1]) == "by Submission at 2:39 in Round 1"
    assert finish_by_round_one(sample_tweets[2]) == "by KO, Round 1"
    assert finish_by_round_one(sample_tweets[3]) == "by Technical Submission, Triangle Choke, Round 1"

def test_extract_not_round_one(sample_tweets):
    assert finish_by_round_one(sample_tweets[4]) == None
    assert finish_by_round_one(sample_tweets[5]) == None
    assert finish_by_round_one(sample_tweets[6]) == None

def test_extract_finish_method(sample_tweets):
    assert extract_finish_method(sample_tweets[0]) == "TKO"
    assert extract_finish_method(sample_tweets[1]) == "Submission"
    assert extract_finish_method(sample_tweets[2]) == "KO"
    assert extract_finish_method(sample_tweets[3]) == "Technical Submission"
