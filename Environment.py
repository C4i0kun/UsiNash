from .Competitors import Competitor

import random
import numpy as np


class Consumer:
    def __init__(self, mean, std):
        self.money = max(np.random.normal(mean, std), 0)
        self.max_buying_price = self.money / 2
        self.steps_to_max = 100

    def update_max_buying_price(self):
        if self.steps_to_max > 0:
            y_0 = self.max_buying_price / self.money
            x_0 = 2 * np.arcsin(y_0) / np.pi
            dx = (1 - x_0) / self.steps_to_max
            x = x_0 + dx
            y = np.sin(np.pi * x / 2)
            self.max_buying_price = self.money * y
            self.steps_to_max -= 1

    def can_buy(self, price):
        return True if self.money > price else False

    def will_buy(self, price):
        return True if self.max_buying_price > price else False


class Environment:
    def __init__(
        self,
        num_competitors=2,
        new_buyers_per_step=10,
        buyers_mean_money=100,
        buyers_std_dev_money=250,
    ):
        self.competitors = []
        self.actions = [None] * num_competitors
        for i in range(num_competitors):
            self.competitors.append(Competitor())

        self.buyers = []
        self.new_buyers_per_step = new_buyers_per_step
        self.buyers_mean_money = buyers_mean_money
        self.buyers_std_dev_money = buyers_std_dev_money

    def run_simulation(self, steps=100):
        for i in range(steps):
            self.set_actions()
            self.step()

    def set_actions(self):
        for index, competitor in enumerate(self.competitors):
            self.actions[index] = competitor.action

    def step(self):
        # new buyers arrive
        for i in range(self.new_buyers_per_step):
            self.buyers.append(
                Consumer(self.buyers_mean_money, self.buyers_std_dev_money)
            )

        # sort competitors by price
        valid_competitors = []
        for competitor in self.competitors:
            if (
                competitor.action is not None
                and competitor.product > 0
            ):
                valid_competitors.append(competitor)

        competitors_ordered = sorted(valid_competitors, key=lambda x: x.action)

        # randomly sort
        buyers_randomized = random.shuffle(self.buyers)

        # buyers prefer lower prices
        while len(buyers_randomized) > 0 and len(competitors_ordered) > 0:
            buyer = buyers_randomized.pop(0)
            competitor = competitors_ordered.pop(0)

            if buyer.can_buy(competitor.action) and buyer.will_buy(competitor.action):
                self.buyers.remove(buyer)
                competitor.cash += competitor.action
                competitor.products -= 1

            if competitor.products > 0:
                competitors_ordered.insert(0)
