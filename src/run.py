from environment import Environment

import matplotlib.pyplot as plt

env = Environment()
env.run_simulation()

power_plant = env.power_plants[0]

plt.plot(power_plant.cash_hist)
plt.title("Cash over time")
plt.xlabel("Time step")
plt.show()

plt.plot(power_plant.production_hist, label="Production")
plt.plot(power_plant.expenses_hist, label="Expenses")
plt.plot(power_plant.profit_hist, label="Profit")
plt.title("Production and Cost over time")
plt.xlabel("Time step")
plt.legend()
plt.show()

# plt.plot(power_plant.num_workers_hist)
# plt.show()