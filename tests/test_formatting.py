import pytest
import datetime
from decimal import *
import formatting


class TestDataFormatting():

    def test_format_data_single_row(self):
        data = ["Vodka", "ALB 1L", 400, 6, 13.62, 5448]
        columns = ["type", "product", "amount", "case_size", "price", "total"]
        result = ["Vodka", "ALB 1L", 400, 6, '$13.62', "$5,448.00"]
        assert formatting.format_data(data, columns) == result

    def test_format_data_multiple_rows(self):
        data = [
            ["Vodka", "ALB 1L", 400, 6, 13.62, 5448],
            ["Whiskey", "Bourbon 750", 3213, 6, 162.00, 505926.00]
        ]
        columns = ["type", "product", "amount", "case_size", "price", "total"]
        result = [
            ["Vodka", "ALB 1L", 400, 6, '$13.62', '$5,448.00'],
            ["Whiskey", "Bourbon 750", 3213, 6, '$162.00', '$505,926.00']
        ]
        assert formatting.format_data(data, columns) == result

    def test_format_data_barrels(self):
        data = [
            ['13-001', 'Bourbon', 53, 32.67, datetime.datetime(2013,1,1), 2309,
             'Mark'],
            ['14-001', 'Malt', 30, 16.76, datetime.datetime(2014,5,2), 1823,
             'Louis'],
        ]
        columns = [
            'barrel_no', 'type', 'gallons', 'proof_gallons', 'date_filled',
            'age', 'investor'
        ]
        result = [
            ['13-001', 'Bourbon', 53, 32.67, '2013-01-01',
             '6 years, 3 months, 28 days', 'Mark'],
            ['14-001', 'Malt', 30, 16.76, '2014-05-02',
             '4 years, 11 months, 27 days', 'Louis'],
        ]
        assert formatting.format_data(data, columns) == result

    def test_reverse_format_data(self):
        data = ["Vodka", "ALB 1L", 400, 6, '$13.62', "$5,448.00"]
        columns = ["type", "product", "amount", "case_size", "price", "total"]
        result = ["Vodka", "ALB 1L", 400, 6, Decimal('13.62'), 5448]
        assert formatting.reverse_format_data(data, columns) == result

    def test_reverse_format_multiple_rows(self):
        data = [
            ["Vodka", "ALB 1L", 400, 6, '$13.62', '$5,448.00'],
            ["Whiskey", "Bourbon 750", 3213, 6, '$162.00', '$505,926.00']
        ]
        columns = ["type", "product", "amount", "case_size", "price", "total"]
        result = [
            ["Vodka", "ALB 1L", 400, 6, Decimal('13.62'), 5448],
            ["Whiskey", "Bourbon 750", 3213, 6, Decimal('162.00'), 505926.00]
        ]
        assert formatting.reverse_format_data(data, columns) == result

    def test_reverse_format_data_barrels(self):
        data = [
            ['13-001', 'Bourbon', 53, 32.67, '2013-01-01',
             '6 years, 3 months, 28 days', 'Mark'],
            ['14-001', 'Malt', 30, 16.76, '2014-05-02',
             '4 years, 11 months, 27 days', 'Louis']
        ]
        columns = ['barrel_no', 'type', 'gallons', 'proof_gallons',
                   'date_filled', 'age', 'investor'
        ]
        now = datetime.datetime.now()
        result = [
            ['13-001', 'Bourbon', 53, 32.67, datetime.datetime(2013,1,1),
             (now - datetime.datetime(2013,1,1)).days, 'Mark'],
            ['14-001', 'Malt', 30, 16.76, datetime.datetime(2014,5,2),
             (now - datetime.datetime(2014,5,2)).days, 'Louis']
        ]
        assert formatting.reverse_format_data(data, columns) == result

    def test_reverse_format_data_emptied_barrels(self):
        data = ['14-067', 'Rye', '53', 34.56, 29.67, '2014-05-24',
                '2019-03-12', '4 years, 9 months, 16 days', 'Miles'
        ]
        columns = ['barrel_no', 'type', 'gallons', 'proof_gallons',
                   'pg_remaining', 'date_filled', 'date_emptied', 'age',
                   'investor'
        ]
        result = [
            '14-067', 'Rye', '53', 34.56, 29.67, datetime.datetime(2014,5,24),
            datetime.datetime(2019,3,12), 1753, 'Miles'
        ]
        assert formatting.reverse_format_data(data, columns) == result
