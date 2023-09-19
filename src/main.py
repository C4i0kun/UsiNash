import requests
import spade
import asyncio

from power_plant import PowerPlant
from environment import Environment

admin_user = "admin"
admin_pass = "admin"
base_address = "http://127.0.0.1:9090"
n = 5

def create_user(user, password):
    print("Creating user " + user + " ...")
    requests.post(
        base_address + "/plugins/restapi/v1/users", \
        auth=(admin_user, admin_pass), \
        json={ "username": user, "password": password }
    )


game_attributes = {
    "new_workers_per_step": 10,
    "workers_mean_money": 100,
    "workers_std_dev_money": 250,
    "workers": []
}

player_attributes = {
    "cash": 1000,
    "products": 0,
    "step": 0,
    "size": None # variable value: must be set in connection
}

async def main():
    global n

    # instanciando as usinas (jogadores do jogo)
    players = []
    for i in range(0, n):
        create_user("player_" + str(i), "pass")
        player = PowerPlant("player_" + str(i) + "@localhost", "pass", "server@localhost")
        players.append(player)

    # instanciando o ambiente (servidor do jogo)
    create_user("server", "pass")
    server = Environment(
        jid="server@localhost", password="pass", \
        power_plants=players, frequency=1,
        game_attributes=game_attributes,
        player_attributes=player_attributes
    )

    # inicializando agentes
    await server.start()
    for player in players:
        await player.start()

    # loop principal
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    spade.run(main())