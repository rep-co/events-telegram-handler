class Price:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return "{0} {1}".format(self.amount, self.currency)