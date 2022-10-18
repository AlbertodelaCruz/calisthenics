import math


def statement(invoice, plays):
    total_amount = 0
    total_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    for perf in invoice['performances']:
        total_credits, result, total_amount = _calculate_perfomance_result(plays, perf, total_credits, result, total_amount)

    result += f'Amount owed is {_format_as_dollars(total_amount/100)}\nYou earned {total_credits} credits\n'
    return result

def _calculate_perfomance_result(plays, perf, total_credits, result, total_amount):
    play = plays[perf['playID']]
    this_amount = _calculate_performance_amount(play, perf)
    performance_credits = _calculate_performance_credits(perf, play)

    result += f' {play["name"]}: {_format_as_dollars(this_amount/100)} ({perf["audience"]} seats)\n'
    total_amount += this_amount
    total_credits += performance_credits
    return total_credits, result, total_amount

def _calculate_performance_credits(perf, play):
    volume_credits = max(perf['audience'] - 30, 0)
    if "comedy" == play["type"]:
        volume_credits += math.floor(perf['audience'] / 5)
    return volume_credits

def _calculate_performance_amount(play, perf):
    if not play['type'] in ['tragedy', 'comedy']:
        raise ValueError(f'unknown type: {play["type"]}')
    if play['type'] == "tragedy":
        this_amount = _calculate_amount_for_tragedy_play(perf)
    if play['type'] == "comedy":
        this_amount = _calculate_amount_for_comedy_play(perf)
    return this_amount

def _calculate_amount_for_comedy_play(perf):
    this_amount = 30000
    if perf['audience'] > 20:
        this_amount += 10000 + 500 * (perf['audience'] - 20)
    this_amount += 300 * perf['audience']
    return this_amount

def _calculate_amount_for_tragedy_play(perf):
    this_amount = 40000
    if perf['audience'] > 30:
        this_amount += 1000 * (perf['audience'] - 30)
    return this_amount

def _format_as_dollars(amount):
    return f"${amount:0,.2f}"

