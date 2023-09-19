from spade_game.player import Player

class PowerPlant(Player):
    def __init__(self, jid, password, server_jid, size=1):
        super().__init__(jid, password, server_jid)
        self.size = size
        self.cash = 1000
        self.workers = []
        self.base_expenses = 50 * (self.size ** 2)
        self.base_production = 1000 * self.size

        # defined by action
        self.workers_needed = 0
        self.proposed_salary = 0

        self.step = 0
        self.cash_hist = [self.cash]
        self.production_hist = []
        self.expenses_hist = []
        self.profit_hist = []
        self.num_workers_hist = []

    """
    def update_state(self):
        salary_expenses = 0
        for worker in self.workers:
            salary_expenses += worker["salary"]
            worker["steps_to_work"] -= 1
        self.workers = [worker for worker in self.workers if worker["steps_to_work"] > 0]

        # update cash
        production = self.base_production * (1 + 10 * (1 - 1/(1 + len(self.workers) / 10)))
        expenses = salary_expenses + self.base_expenses
        self.cash += production
        self.cash -= expenses

        # log data
        self.cash_hist.append(self.cash)
        self.production_hist.append(production)
        self.expenses_hist.append(expenses)
        self.profit_hist.append(production - expenses)
        self.num_workers_hist.append(len(self.workers))

        # next step
        self.step += 1
    """

    def decide_action(self):
        # simple action: always looking for 1 worker
        self.workers_needed = 1
        self.proposed_salary = 150

