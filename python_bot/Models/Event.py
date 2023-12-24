from python_bot.Models.Price import Price


class Event:
    def __init__(self, name: str, description: str, date: str, price: Price, location: str):
        self.name = name
        self.description = description
        self.date = date
        self.price = price
        self.location = location
