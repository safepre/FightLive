def is_first_round_finish(message):
    return ('Round 1' in message and 'No scorecard available' in message)

def is_new_fight_update(message):
    return message != "No new fight updates at this time."
