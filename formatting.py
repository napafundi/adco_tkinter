import datetime
from decimal import Decimal, getcontext, InvalidOperation
from dateutil.relativedelta import relativedelta

# Set precision of Decimal
# Allows large decimal numbers to exist
getcontext().prec = 28

def barrel_age(days):
    now = datetime.datetime.now()
    td = datetime.timedelta(days=days)
    orig_date = now - td
    diff = relativedelta(now, orig_date)
    years = diff.years
    months = diff.months
    days = diff.days
    return "{} years, {} months, {} days".format(years, months, days)

def rev_barrel_age(data, columns):
    if 'date_emptied' in columns:
        fill_date = datetime.datetime.strptime(
            data[columns.index('date_filled')],
            "%Y-%m-%d"
        )
        empty_date = datetime.datetime.strptime(
            data[columns.index('date_emptied')],
            "%Y-%m-%d"
        )
        delta = empty_date - fill_date
    else:
        fill_date = datetime.datetime.strptime(
            data[columns.index('date_filled')],
            "%Y-%m-%d"
        )
        now = datetime.datetime.now()
        delta = now - fill_date
    days = delta.days
    return days


def float_format_currency(x):
    return "${:,.2f}".format(float(x))


def rev_currency_format(x):
    if '$' in str(x):
        x = str(x).replace(",", "")[1:]
    # Round decimal to 2 places when returning
    return Decimal(x).quantize(Decimal('.01'), rounding='ROUND_HALF_UP')


def rev_general_format(x):
    # Format data not handled by the functions above
    # Treeview's get_value method sometimes returns decimals/floats/ints
    # as strings and they need to be reformatted. Else, just return data
    try:
        x =  Decimal(x).quantize(Decimal('.01'), rounding='ROUND_HALF_UP')
        return x
    except InvalidOperation:
        return x


def format_data(data, columns):
    formatted_rows = []
    # Check if data is a list of lists or tuples
    if any(isinstance(el, (list, tuple)) for el in data):
        for row in data:
             formatted_rows.append([float_format_currency(x)
                                   if y in ['price','total']
                                   else barrel_age(x)
                                   if y in ['age']
                                   else x.strftime('%Y-%m-%d')
                                   if 'date' in y
                                   else x
                                   for x,y in zip(row, columns)])
    else:
        formatted_rows = [float_format_currency(x)
                          if y in ['price','total']
                          else barrel_age(x)
                          if y in ['age']
                          else x.strftime('%Y-%m-%d')
                          if 'date' in y
                          else x
                          for x,y in zip(data, columns)]
    return formatted_rows

def reverse_format_data(data, columns):
    formatted_rows = []
    if any(isinstance(el, (list, tuple)) for el in data):
        for row in data:
            formatted_rows.append([rev_currency_format(x)
                                   if y in ['price', 'total']
                                   else rev_barrel_age(row, columns)
                                   if y in ['age']
                                   else datetime.datetime.strptime(x,"%Y-%m-%d")
                                   if 'date' in y
                                   else rev_general_format(x)
                                   for x,y in zip(row, columns)])
    else:
        formatted_rows = [rev_currency_format(x)
                          if y in ['price', 'total']
                          else rev_barrel_age(data, columns)
                          if y in ['age']
                          else datetime.datetime.strptime(x, "%Y-%m-%d")
                          if 'date' in y
                          else rev_general_format(x)
                          for x,y in zip(data, columns)]
    return formatted_rows
