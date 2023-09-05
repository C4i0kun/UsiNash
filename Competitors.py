class Competitor:
    def __init__(self, size=1):
        self.size = size
        self.cash = 1000
        self.products = 0
        self.expenses = self.size * 10
        self.production = self.size

        self.step = 0
        self.cash_per_step = [self.cash]
        self.profit = []

    def run(self):
        self.decide_action()

    def update_state(self):
        self.step += 1
        self.cash -= self.expenses
        self.cash_per_step.append(self.cash)
        self.profit.append(self.cash_per_step[-1] - self.cash_per_step[-2])

    def decide_action(self):
        pass

