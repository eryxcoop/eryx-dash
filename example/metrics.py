from eryx_dash.metrics import MoneyMetric, IntegerMetric, PercentageMetric, LargeIntegerMetric


class Invoices(IntegerMetric):
    def name(self):
        return 'Invoices'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df['Invoice ID'].nunique()


class Sales(MoneyMetric):
    def name(self):
        return 'Sales'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df['Total'].sum()


class IncomePerPurchase(MoneyMetric):
    def name(self):
        return 'Income per purchase'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df.groupby('Invoice ID')['Total'].sum().mean()


class Units(MoneyMetric):
    def name(self):
        return 'Units'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df['Quantity'].sum()


class UnitsPerPurchase(MoneyMetric):
    def name(self):
        return 'Units per Purchase'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df.groupby('Invoice ID')['Quantity'].sum().mean()


class Rating(MoneyMetric):
    def name(self):
        return 'Rating'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df['Rating'].mean()


class PercentMembers(PercentageMetric):
    def name(self):
        return '% Members'

    def compute(self, data_sources):
        df = data_sources.get('sales')
        return df[df['Customer type'] == 'Member']['Total'].sum() / df['Total'].sum()
