import pytest
from theatrical_players import statement


def test_statement():
    play = {}
    performance = {}
    invoice = {'customer': 'acruz', 'performances': performance}

    assert statement(invoice, [play]) == 'Statement for acruz\nAmount owed is $0.00\nYou earned 0 credits\n'

def test_statement_tragedy():
    play = {'type': 'tragedy', 'name': 'Fortunata y Jacinta'}
    performance = {'playID': 0, 'audience': 0}
    invoice = {'customer': 'acruz', 'performances': [performance]}

    assert statement(invoice, [play]) == 'Statement for acruz\n Fortunata y Jacinta: $400.00 (0 seats)\nAmount owed is $400.00\nYou earned 0 credits\n'

def test_statement_tragedy_with_high_audience():
    play = {'type': 'tragedy', 'name': 'Fortunata y Jacinta'}
    performance = {'playID': 0, 'audience': 40}
    invoice = {'customer': 'acruz', 'performances': [performance]}

    assert statement(invoice, [play]) == 'Statement for acruz\n Fortunata y Jacinta: $500.00 (40 seats)\nAmount owed is $500.00\nYou earned 10 credits\n'

def test_statement_comedy():
    play = {'type': 'comedy', 'name': 'La traviata'}
    performance = {'playID': 0, 'audience': 0}
    invoice = {'customer': 'acruz', 'performances': [performance]}

    assert statement(invoice, [play]) == 'Statement for acruz\n La traviata: $300.00 (0 seats)\nAmount owed is $300.00\nYou earned 0 credits\n'

def test_statement_comedy_with_high_audience():
    play = {'type': 'comedy', 'name': 'La traviata'}
    performance = {'playID': 0, 'audience': 30}
    invoice = {'customer': 'acruz', 'performances': [performance]}

    assert statement(invoice, [play]) == 'Statement for acruz\n La traviata: $540.00 (30 seats)\nAmount owed is $540.00\nYou earned 6 credits\n'

def test_statement_with_unknown_type():
    play = {'type': 'western', 'name': 'El bueno, el feo y el malo'}
    performance = {'playID': 0, 'audience': 0}
    invoice = {'customer': 'acruz', 'performances': [performance]}

    with pytest.raises(Exception) as exc_info:
        statement(invoice, [play])

    assert str(exc_info.value) == 'unknown type: western'

def test_statement_comedy_with_several_plays():
    comedy_play = {'type': 'comedy', 'name': 'Traviata'}
    tragedy_play = {'type': 'tragedy', 'name': 'Fortunata'}
    performance_comedy = {'playID': 0, 'audience': 30}
    performance_tragedy = {'playID': 1, 'audience': 100}
    invoice = {'customer': 'acruz', 'performances': [performance_comedy, performance_tragedy]}

    assert statement(invoice, [comedy_play, tragedy_play]) == 'Statement for acruz\n Traviata: $540.00 (30 seats)\n Fortunata: $1,100.00 (100 seats)\nAmount owed is $1,640.00\nYou earned 76 credits\n'

