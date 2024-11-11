def is_first_round_finish(message):
    return ('Round 1' in message)

def is_new_fight_update(message):
    no_update_messages = {
        "No new fight updates at this time.",
        "Three Minutes Until Next Update"
    }
    return message not in no_update_messages