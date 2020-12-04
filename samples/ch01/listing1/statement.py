import math

from samples.ch01.listing1.helper import get_invoices, get_plays
from samples.ch01.listing1.typings import Invoice, Plays, Performance, Play


def statement(invoice: Invoice, plays: Plays) -> str:
    return render_plain_text(invoice, plays)


def render_plain_text(invoice: Invoice, plays: Plays) -> str:
    def play_for(perf: Performance) -> Play:
        play = plays[perf.play_id]
        return play

    def amount_for(perf: Performance) -> int:
        if play_for(perf).type == 'tragedy':
            amount = 40000
            if perf.audience > 30:
                amount += 1000 * (perf.audience - 30)
        elif play_for(perf).type == 'comedy':
            amount = 30000
            if perf.audience > 20:
                amount += 10000 + 500 * (perf.audience - 20)
            amount += 300 * perf.audience
        else:
            raise ValueError(f'Unknown type: ${play_for(perf).type}')
        return amount

    def volume_credits_for(perf: Performance) -> int:
        volume_credits = 0
        volume_credits += max(perf.audience - 30, 0)
        if play_for(perf).type == 'comedy':
            volume_credits += math.floor(perf.audience / 5)
        return volume_credits

    def total_amount() -> int:
        total_amount = 0
        for perf in invoice.performances:
            total_amount += amount_for(perf)
        return total_amount

    def total_volume_credits() -> int:
        volume_credits = 0
        for perf in invoice.performances:
            volume_credits += volume_credits_for(perf)
        return volume_credits

    result = f'Statement for {invoice.customer}\n'
    for perf in invoice.performances:
        result += f' {play_for(perf).name}: {usd_format(amount_for(perf) / 100)} ({perf.audience} seats)\n'

    result += f'Amount owed is {usd_format(total_amount() / 100)} \n'
    result += f'You earned {total_volume_credits()} credits\n'

    return result


def usd_format(amount: float) -> str:
    return f'{amount : ,.2f}'


if __name__ == '__main__':
    param1 = get_invoices()[0]
    param2 = get_plays()
    print(statement(param1, param2))
