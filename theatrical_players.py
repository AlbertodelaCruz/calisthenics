import math
from dataclasses import dataclass

@dataclass
class Amount:
    _amount: int

    def current(self):
        return self._amount

    def add(self, other):
        new_amount = self._amount + other.current()
        return Amount(new_amount)

@dataclass
class Credits:
    _credits: int

    def current(self):
        return self._credits

    def add(self, other):
        new_credits = self._credits + other.current()
        return Credits(new_credits)


def statement(invoice, plays):
    amount = Amount(0)
    credits = Credits(0)
    result = f'Statement for {invoice["customer"]}\n'

    for perf in invoice['performances']:
        credits, result, amount = _calculate_perfomance_result(plays, perf, credits, result, amount)

    result += f'Amount owed is {_format_as_dollars(amount.current()/100)}\nYou earned {credits.current()} credits\n'
    return result

def _calculate_perfomance_result(plays, perf, credits, result, amount):
    play = plays[perf['playID']]
    performance_amount = _calculate_performance_amount(play, perf)
    performance_credits = _calculate_performance_credits(perf, play)

    result += f' {play["name"]}: {_format_as_dollars(performance_amount.current()/100)} ({perf["audience"]} seats)\n'
    amount = amount.add(performance_amount)
    credits = credits.add(performance_credits)
    return credits, result, amount

def _calculate_performance_credits(perf, play):
    credits = Credits(max(perf['audience'] - 30, 0))
    return credits.add(_calculate_extra_credits_for_comedy(play, perf))

def _calculate_extra_credits_for_comedy(play, perf):
    if "comedy" == play["type"]:
        return Credits(math.floor(perf['audience'] / 5))
    return Credits(0)

def _calculate_performance_amount(play, perf):
    if not play['type'] in ['tragedy', 'comedy']:
        raise ValueError(f'unknown type: {play["type"]}')
    if play['type'] == "tragedy":
        return _calculate_amount_for_tragedy_play(perf)
    if play['type'] == "comedy":
        return _calculate_amount_for_comedy_play(perf)

def _calculate_amount_for_comedy_play(perf):
    return Amount(30000)\
        .add(_calculate_extra_amount_for_comedy_high_audience(perf))\
        .add(Amount(300 * perf['audience']))

def _calculate_amount_for_tragedy_play(perf):
    return Amount(40000)\
        .add(_calculate_extra_amount_for_tragedy_high_audience(perf))

def _calculate_extra_amount_for_comedy_high_audience(perf):
    if perf['audience'] > 20:
        return Amount(10000 + 500 * (perf['audience'] - 20))
    return Amount(0)

def _calculate_extra_amount_for_tragedy_high_audience(perf):
    if perf['audience'] > 30:
        return Amount(1000 * (perf['audience'] - 30))
    return Amount(0)

def _format_as_dollars(amount):
    return f"${amount:0,.2f}"
