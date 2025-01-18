# -*- coding: utf-8 -*-
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, LikeEvent, GiftEvent
import subprocess
import requests
import uuid
import concurrent.futures
gift_to_commande_mapping = {
    "Rose": "D",
    "Pink": "D",
    "Finger Heart": "S",
    "Cœur avec les doigts": "S",
    "TikTok": "U",
    "Haltère": "L",
    "Dumbbell": "L",
    "Bonjour juillet": "W",
    "Hello July": "W",
    "GG": "Y",
    "Micro": "C",
    "Cornet de crème glacée": "X",
    "ice cream cone": "X",
    "Coquillage de Coton": "R",
    "Cotton Shell": "R",
    "Photo des stars": "O",
    "Picture of the stars": "O"
}


def generate_unique_id():
    # Générer un UUID version 4 (aléatoire)
    unique_id = uuid.uuid4()
    # Convertir l'UUID en chaîne de caractères et supprimer les tirets
    return str(unique_id).replace('-', '')

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="@vladik_oladik_2222")
def send_post_request(url, data):
    def post_request():
        try:
            response = requests.post(url, json=data)

            if response.status_code == 200:
                # La requête a réussi
                # print("Requête POST réussie")
                response_data = response.json()  # Récupération des données de réponse au format JSON
                print(response_data)
                return response_data
            else:
                # La requête a échoué
                print(f"Erreur lors de la requête POST. Code de réponse : {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Une exception s'est produite lors de la requête
            print(f"Erreur lors de la requête POST : {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(post_request)

@client.on("connect")
async def on_connect(event: ConnectEvent):
    print("Connected")

# Notice no decorator?
async def on_comment(event: CommentEvent):
    data = {"commande": "B", "id_commande": generate_unique_id()}

    send_post_request('http://127.0.0.1:5000/commande', data)

@client.on("like")
async def on_like(event: LikeEvent):
    data = {"commande": "A", "id_commande": generate_unique_id()}
    send_post_request('http://127.0.0.1:5000/commande', data)
    print(f"@{event.user.unique_id} liked the stream!")

@client.on("gift")
async def on_gift(event: GiftEvent):
    global gift_to_commande_mapping
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")
        gift_name = event.gift.info.name
        if gift_name in gift_to_commande_mapping:
            if event.gift.count >= 2:
                if event.gift.count > 50:
                    for _ in 50:
                        commande = {"commande": gift_to_commande_mapping[gift_name],"id_commande": generate_unique_id()}
                        send_post_request('http://127.0.0.1:5000/commande', commande)
                else:
                    for _ in range(event.gift.count):
                        commande = {"commande": gift_to_commande_mapping[gift_name],"id_commande": generate_unique_id()}
                        send_post_request('http://127.0.0.1:5000/commande', commande)
            else:
                commande = {"commande": gift_to_commande_mapping[gift_name], "id_commande": generate_unique_id()}
                send_post_request('http://127.0.0.1:5000/commande', commande)
            # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\" - event gift streakable")
        gift_name = event.gift.info.name
        if gift_name in gift_to_commande_mapping:
            commande = gift_to_commande_mapping[gift_name]
            send_post_request('http://127.0.0.1:5000/commande', commande)

    # Non-streakable gift

# Define handling an event via a "callback"
client.add_listener("gift", GiftEvent)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()