class PowerPlant:
    def __init__(self, size=1):
        self.size = size
        self.cash = 1000
        self.workers = []
        self.base_expenses = 10 * (self.size) ** 2
        self.production = 1000 * self.size

        # defined by action
        self.workers_needed = 0
        self.proposed_salary = 0

        self.step = 0
        self.cash_per_step = [self.cash]
        self.num_workers = []
        self.profit = []

    def run(self):
        self.decide_action()

    def update_state(self):
        salary_expenses = 0
        for worker in self.workers:
            salary_expenses += worker["salary"]
            worker["steps_to_work"] -= 1
        self.workers = [worker for worker in self.workers if worker["steps_to_work"] > 0]

        # update cashw
        self.cash += self.production * (1 + 1 - 1/(1 + len(self.workers) / 10))
        self.cash -= salary_expenses + self.base_expenses

        # log data
        self.cash_per_step.append(self.cash)
        self.profit.append(self.cash_per_step[-1] - self.cash_per_step[-2])
        self.num_workers.append(len(self.workers))

        # next step
        self.step += 1

    def decide_action(self):
        # simple action: always looking for 1 worker
        self.workers_needed = 1
        self.proposed_salary = 100

