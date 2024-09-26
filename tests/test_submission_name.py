import pytest
from src.text_processing import find_all_submissions

@pytest.fixture
def sample_tweets():
    return [
      "#UFCMexico Official Result: Raoni Barcelos (@BarcelosRaoni) defeats Cristian Quiñonez by Submission due to a Rear Naked Choke at 2:04 in Round 3. \n\nAll Fight Results ➡️: https://ufc.ac/3OW2jTY",
      "🇬🇧#UFC304 Official Result: Paddy Pimblett defeats King Green by Technical Submission, Triangle Choke, Round 1, 3:22 \n\nLive Results, Interviews & More: https://ufc.ac/3Yf3F1M",
      "#UFCAbuDhabi Official Result: Michael Chiesa (@MikeMav22) defeats Tony Ferguson by Submission (Rear-Naked Choke) at 3:44 of Round 1. \n\nResults, Interviews & More ➡️: https://ufc.ac/3WyvoIk \n\n#InAbuDhabi | @InAbuDhabi| @VisitAbuDhabi",
      "#UFCVegas89 Official Result: Julian Erosa (@juicyj_erosa) defeats Ricardo Ramos by Submission (guillotine choke) at 2:15 of Round 1. \n\nAll Fight Results ⬇️: https://ufc.ac/4aqSwxK",
      "#UFCVegas89 Official Result: Fernando Padilla defeats Luis Pajuelo by Submission (D'Arce Choke) at 2:45 of Round 1. \n\nAll Fight Results ⬇️: https://ufc.ac/4akTmvG",
      "#UFCVegas91 Official Result: Ivana Petrovic defeats Liang Na by Submission (Arm Triangle Choke) at 1:29 of Round 3 \n\n All Fight Results ➡️: https://ufc.ac/4aTEhlu",
      "#UFCVegas92 Official Result: Angela Hill (@AngieOverkill) defeats Luana Pinheiro by Submission due to a Guillotine Choke 4:12 in Round 2. \n\n All Fight Results ➡️: https://ufc.ac/3QMP4Gj",
      "#UFC297 Official Result: Jasmine Jasudavicius (@JasJasudavicius) defeats Priscila Cachoeira by Submission (anaconda choke) at 4:21 of Round 3. \n\n All Fight Results ⬇️: https://ufc.ac/422CzuB",
      "#UFCVegas82 Official Result: Joanderson Brito defeats Jonathan Pearce by Submission due to a Ninja Choke at 3:54 in Round 2. \n\n All Results ➡️: https://ufc.ac/40ZvE53",
      "#UFC294 Official Result: Muhammad Mokaev (@muhammadmokaev) defeats Tim Elliott by Submission, Head & Arm Choke, Round 3, 3:03 \n\n Complete Results: https://ufc.ac/45zUhWl \n\n [#InAbuDhabi | @InAbuDhabi | @VisitAbuDhabi]",
      "#UFC293 Official Result: Alexander Volkov (@AlexDragoVolkov) defeats Tai Tuivasa by Submission, Ezekiel Choke, Round 2, 4:37 \n\n All Results From Sydney:  https://ufc.ac/3r5D8pk",
      "#UFC235 Official Result: @BenAskren def Robbie Lawler by submission due to a bulldog choke at 3:20 in Round 1. \n\n Live Results: https://ufc.com/news/ufc-235-r",
      "Dana White's Contender Series Official Result: Kevin Christian defeats Francesco Mazzeo by Submission (triangle armbar) at 4:17 of Round 2. \n\n All #DWCS Week 7 Results + Scorecards ➡️: https://ufc.ac/4ecnw6T",
      "#UFC295 Official Result: Mateusz Rebecki (@RebeckiMateusz) defeats Roosevelt Roberts by Submission (armbar) at 3:08 of Round 1. \n\n All Fight Results ⬇️: https://ufc.ac/463Aejz",
      "#UFCLasVegas Official Result: Davey Grant (@daveygrantmma) defeats Raphael Assuncao by Submission, Reverse Triangle, Round 3, 4:43 \n\n Full Results, Backstage Interviews, Highlights & More ➡️: https://ufc.ac/3Jv04Vv",
      "#UFCGlendale Official Result: Adam Wieczorek def. Arjan Bhullar by submission (Omoplata) at 1:59 of R2",
      "#UFCVegas Official Result: @MackenzieDern def Hannah Cifers by submission, kneebar, Round 1, 2:36. \n\n Live Results: https://ufc.com/news/ufc-vegas",
    ]

def test_process_submission_types(sample_tweets):

    submission_types = find_all_submissions(sample_tweets, 'submission_types.txt')
    expected_types = [
        'rear naked choke', 'triangle choke', 'guillotine choke', 'd\'arce choke',
        'arm triangle choke', 'anaconda choke', 'ninja choke', 'head & arm choke',
        'ezekiel choke', 'bulldog choke', 'triangle armbar', 'armbar',
        'reverse triangle', 'omoplata', 'kneebar'
    ]
    assert all(submission_type in submission_types for submission_type in expected_types)
    assert all(submission_type in expected_types for submission_type in submission_types)
    assert len(submission_types) == len(set(submission_types))