import math

from samples.ch01.listing1.helper import get_invoices, get_plays
from samples.ch01.listing1.typings import Invoice, Plays


def statement(invoice: Invoice, plays: Plays) -> str:
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice.customer}\n'

    for perf in invoice.performances:
        play = plays[perf.play_id]

        if play.type == 'tragedy':
            this_amount = 40000
            if perf.audience > 30:
                this_amount += 1000 * (perf.audience - 30)
        elif play.type == 'comedy':
            this_amount = 30000
            if perf.audience > 20:
                this_amount += 10000 + 500 * (perf.audience - 20)
            this_amount += 300 * perf.audience
        else:
            raise ValueError(f'Unknown type: ${play.type}')

        # add volume credits
        volume_credits += max(perf.audience - 30, 0)
        # add extra credit for every ten comedy attendees
        if play.type == 'comedy':
            volume_credits += math.floor(perf.audience / 5)

        result += f' {play.name}: {this_amount / 100 : ,.2f} ({perf.audience} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {total_amount / 100 : ,.2f} \n'
    result += f'You earned {volume_credits} credits\n'

    return result


if __name__ == '__main__':
    param1 = get_invoices()[0]
    param2 = get_plays()
    print(statement(param1, param2))
