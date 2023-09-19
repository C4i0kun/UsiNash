from power_plant import PowerPlant

import random
import numpy as np

class Worker:
    def __init__(self, mean, std):
        self.expected_salary = max(np.random.normal(mean, std), 0)
        self.min_salary = self.expected_salary / 2
        self.steps_to_max = 100

    def update_expected_salary(self):
        if self.steps_to_max > 0 and self.expected_salary < self.min_salary:
            y_0 = self.min_salary / self.expected_salary
            x_0 = 2 * np.arcsin(y_0) / np.pi
            dx = (1 - x_0) / self.steps_to_max
            x = x_0 + dx
            y = np.arcsin(np.pi * x / 2)
            self.expected_salary = self.expected_salary * y
            self.steps_to_max -= 1

    def will_accept_salary(self, salary):
        return True if self.expected_salary < salary else False

    def can_accept_salary(self, salary):
        return True if self.min_salary < salary else False


class Environment:
    def __init__(
        self,
        num_power_plants=2,
        new_workers_per_step=10,
        workers_mean_salary=100,
        workers_std_dev_salary=250,
    ):
        self.power_plants = []
        self.proposed_salaries = [None] * num_power_plants
        self.workers_needed = [None] * num_power_plants
        for i in range(num_power_plants):
            self.power_plants.append(PowerPlant())

        self.workers = []
        self.new_workers_per_step = new_workers_per_step
        self.workers_mean_salary = workers_mean_salary
        self.workers_std_dev_salary = workers_std_dev_salary

    def run_simulation(self, steps=100):
        for i in range(steps):
            self.set_actions()
            self.step()

    def set_actions(self):
        for index, power_plant in enumerate(self.power_plants):
            power_plant.run()
            self.proposed_salaries[index] = power_plant.proposed_salary
            self.workers_needed[index] = power_plant.workers_needed

    def step(self):
        # new possible workers arrive
        for i in range(self.new_workers_per_step):
            self.workers.append(
                Worker(self.workers_mean_salary, self.workers_std_dev_salary)
            )

        # sort competitors by salary (biggest salary first)
        valid_power_plants = []
        for power_plant in self.power_plants:
            if (
                power_plant.proposed_salary is not None
                and power_plant.workers_needed > 0
            ):
                valid_power_plants.append(power_plant)

        power_plants_ordered = sorted(valid_power_plants, key=lambda x: x.proposed_salary, reverse=True)

        # randomly sort
        workers_randomized = self.workers.copy()
        random.shuffle(self.workers)

        # workers prefer higher prices
        while len(workers_randomized) > 0 and len(power_plants_ordered) > 0:
            worker = workers_randomized.pop(0)
            power_plant = power_plants_ordered.pop(0)

            if worker.can_accept_salary(power_plant.proposed_salary) and worker.can_accept_salary(power_plant.proposed_salary):
                self.workers.remove(worker)
                power_plant.workers.append({"salary": power_plant.proposed_salary, "steps_to_work": 100 + 1})
                power_plant.workers_needed -= 1

            if power_plant.workers_needed > 0:
                power_plants_ordered.insert(0, power_plant)

        # update unemployed workers expected salary
        for worker in self.workers:
            worker.update_expected_salary()

        # update powerplant states
        for power_plant in self.power_plants:
            power_plant.update_state()

        

        
