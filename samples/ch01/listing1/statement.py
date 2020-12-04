from samples.ch01.listing1.helper import get_invoices, get_plays
from samples.ch01.listing1.statement_arg import StatementArg, create_statement_arg
from samples.ch01.listing1.typings import Invoice, Plays


def statement(invoice: Invoice, plays: Plays) -> str:
    return render_plain_text(create_statement_arg(invoice, plays))


def render_plain_text(statement_args: StatementArg) -> str:
    result = f'Statement for {statement_args["customer"]}\n'
    for perf in statement_args['performances']:
        result += (
            f' {perf.play.name}: {usd_format(perf.amount)} '
            f'({perf.audience} seats)\n'
        )

    result += f'Amount owed is {statement_args["total_amount"]} \n'
    result += f'You earned {statement_args["total_volume_credits"]} credits\n'

    return result


def html_statement(invoice: Invoice, plays: Plays) -> str:
    return render_html(create_statement_arg(invoice, plays))


def render_html(statement_args: StatementArg) -> str:
    result = f"<h1>Invoice (Customer: {statement_args['customer']})</h1>\n"
    result += "<table>\n"
    result += "<tr><th>Play</th><th>Seats</th><th>Price</th></tr>\n"

    for perf in statement_args["performances"]:
        result += (
            f"\t<tr><td>{perf.play.name}</td>"
            f"<td>({perf.audience} Seats)</td>"
            f"<td>{usd_format(perf.amount)}</td></tr>\n"
        )

    result += "</table>\n"
    result += (
        f"<p>Total Amount: <em>{usd_format(statement_args['total_amount'])}</em></p>\n"
    )
    result += (
        f"<p>Volume Credits: <em>{statement_args['total_volume_credits']}</em></p>\n"
    )
    return result


def usd_format(amount: float) -> str:
    return f'{amount : ,.2f}'


if __name__ == '__main__':
    param1 = get_invoices()[0]
    param2 = get_plays()
    print(statement(param1, param2))
    print(html_statement(param1, param2))
