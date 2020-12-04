import math
from dataclasses import asdict, dataclass
from functools import reduce
from typing import List, TypedDict

from samples.ch01.listing1.typings import Invoice, Performance, Play, Plays


@dataclass(frozen=True)
class EnrichedPerformance(Performance):
    play: Play
    amount: int
    volume_credits: int


class StatementArg(TypedDict, total=False):
    customer: str
    performances: List[EnrichedPerformance]
    total_amount: int
    total_volume_credits: int


def create_statement_arg(invoice: Invoice, plays: Plays) -> StatementArg:
    statement_arg: StatementArg = dict()
    statement_arg['customer'] = invoice.customer
    statement_arg['performances'] = [
        _enrich_performance(plays, perf) for perf in invoice.performances
    ]
    statement_arg['total_amount'] = _get_total_amount(statement_arg)
    statement_arg['total_volume_credits'] = _get_total_volume_credits(statement_arg)
    return statement_arg


def _enrich_performance(plays: Plays, perf: Performance) -> EnrichedPerformance:
    return EnrichedPerformance(
        play=_get_play_for(plays, perf),
        amount=_get_amount_for(plays, perf),
        volume_credits=_get_volume_credits_for(plays, perf),
        **asdict(perf),
    )


def _get_play_for(plays: Plays, perf: Performance) -> Play:
    play = plays[perf.play_id]
    return play


def _get_amount_for(plays: Plays, perf: Performance) -> int:
    if _get_play_for(plays, perf).type == 'tragedy':
        amount = 40000
        if perf.audience > 30:
            amount += 1000 * (perf.audience - 30)
    elif _get_play_for(plays, perf).type == 'comedy':
        amount = 30000
        if perf.audience > 20:
            amount += 10000 + 500 * (perf.audience - 20)
        amount += 300 * perf.audience
    else:
        raise ValueError(f'Unknown type: ${_get_play_for(plays, perf).type}')
    return amount


def _get_volume_credits_for(plays: Plays, perf: Performance) -> int:
    volume_credits = 0
    volume_credits += max(perf.audience - 30, 0)
    if _get_play_for(plays, perf).type == 'comedy':
        volume_credits += math.floor(perf.audience / 5)
    return volume_credits


def _get_total_amount(statement_args: StatementArg) -> int:
    return reduce(lambda total, p: total + p.amount, statement_args['performances'], 0)


def _get_total_volume_credits(statement_args: StatementArg) -> int:
    return reduce(
        lambda total, p: total + p.volume_credits, statement_args['performances'], 0
    )
