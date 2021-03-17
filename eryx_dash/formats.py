from millify import millify


def format_money(number):
    return '$' + millify(number, precision=2)


def format_percentage(number):
    return '%.0f%%' % (100 * number)


def format_integer(number):
    return round(number)


def format_large_integer(number):
    return millify(number)
