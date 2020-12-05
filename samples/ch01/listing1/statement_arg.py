import math
from dataclasses import asdict, dataclass
from functools import reduce
from typing import List, TypedDict

from samples.ch01.listing1.performance_calculator import create_performance_calculator
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
    calculator = create_performance_calculator(perf, _get_play_for(plays, perf))
    return EnrichedPerformance(
        play=_get_play_for(plays, perf),
        amount=calculator.get_amount(),
        volume_credits=calculator.get_volume_credits(),
        **asdict(perf),
    )


def _get_play_for(plays: Plays, perf: Performance) -> Play:
    play = plays[perf.play_id]
    return play


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
