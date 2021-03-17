from eryx_dash.formats import format_money, format_percentage, format_integer, format_large_integer


class Metric(object):
    def compute(self, *args, **kwargs):
        raise Exception("Subclass responsibility")

    def formatted(self, *args, **kwargs):
        raise Exception("Subclass responsibility")


class MoneyMetric(object):
    def compute(self, *args, **kwargs):
        raise Exception("Subclass responsibility")

    def formatted(self, *args, **kwargs):
        return format_money(self.compute(*args, **kwargs))


class PercentageMetric(object):
    def compute(self, *args, **kwargs):
        raise Exception("Subclass responsibility")

    def formatted(self, *args, **kwargs):
        return format_percentage(self.compute(*args, **kwargs))


class IntegerMetric(object):
    def compute(self, *args, **kwargs):
        raise Exception("Subclass responsibility")

    def formatted(self, *args, **kwargs):
        return format_integer(self.compute(*args, **kwargs))


class LargeIntegerMetric(object):
    def compute(self, *args, **kwargs):
        raise Exception("Subclass responsibility")

    def formatted(self, *args, **kwargs):
        return format_large_integer(self.compute(*args, **kwargs))
