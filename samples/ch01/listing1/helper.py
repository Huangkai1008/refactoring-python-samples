import json
from typing import List

from dacite import from_dict

from samples.ch01.listing1.typings import Invoice, Play, Plays


def get_invoices() -> List[Invoice]:
    with open('../invoices.json') as f:
        items: list = json.load(f)
    invoices = []
    for item in items:
        invoices.append(from_dict(Invoice, item))
    return invoices


def get_plays() -> Plays:
    with open('../plays.json') as f:
        m: dict = json.load(f)
    plays = dict()
    for key, value in m.items():
        plays[key] = from_dict(Play, value)
    return plays
