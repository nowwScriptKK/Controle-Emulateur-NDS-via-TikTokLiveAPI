## Projet de 2023, je ne ferais pas de mise à jour dessus.
## Si vous avez besoin d'outils d'interaction avec Tiktok Live api(Commentaire ou cadeaux) je vous propose un service payant, contacté moi sur discord: Actheglitch

# Contrôle d'Émulateur NDS via TikTokLive API

Ce projet combine deux scripts Python pour offrir une expérience de streaming interactive unique avec TikTokLive tout en contrôlant un émulateur Nintendo DS (DeSmuME) en temps réel. Grâce à cette combinaison, les spectateurs peuvent influencer le gameplay de l'émulateur en envoyant des commentaires, des likes et des cadeaux pendant le stream TikTokLive.

<center><img src="https://raw.githubusercontent.com/nowwScriptKK/Controle-Emulateur-NDS-via-TikTokLiveAPI/refs/heads/main/1.png" style="text-align: center;" alt="Texte alternatif" width="500" height="880"></center>

## Dépendances

- TikTokLive (v0.1.0 ou supérieur)
- requests (v2.26.0 ou supérieur)
- concurrent.futures (généralement inclus dans Python standard)

- pyautogui (v0.9.53 ou supérieur)
- Flask (v2.1.0 ou supérieur)
- psutil (v5.8.0 ou supérieur)
- pynput (v1.7.3 ou supérieur)
- Keyboard (généralement inclus dans Python standard)

## Installation des dépendances

```py
pip install TikTokLive requests pyautogui Flask psutil pynput Keyboard 
```

## Description du Fonctionnement

1. `tikLive.py`: Ce script se connecte au service TikTokLive en utilisant le TikTokLiveClient et écoute les événements tels que les commentaires, les likes et les cadeaux pendant le stream TikTok en direct. Lorsqu'un événement est détecté, le script envoie une commande correspondante au serveur local.

2. `py_script.py`: Ce script contrôle l'émulateur Nintendo DS (DeSmuME) à l'aide de Keyboard. A la base je souhaiter utiisé pyautogui mais les touches n'étaient pas pris en compte par l'émulateur. Il lance l'émulateur avec le fichier ROM spécifié et crée un serveur local qui écoute les requêtes POST sur l'URL `/commande`. Lorsqu'il reçoit une commande via le serveur, il simule la pression de la touche correspondante sur l'émulateur.

## Utilisation


1. Configurez les chemins vers l'exécutable de l'émulateur Nintendo DS et le fichier ROM dans le script `py_script.py`.
   
```py
current_directory_rom = os.path.join(current_directory, "desmume", "pokemon.nds")
```
2. Télécharger Meulon emu, mettre le script dans le même dossier que l'émulateur : https://melonds.kuribo64.net/

3. Exécutez les deux scripts `py_script.py` et `tikLive.py` à l'aide de Python 3 dans des terminaux séparés.

4. Le script `tikLive.py` se connectera au stream TikTokLive spécifié (en utilisant le nom d'utilisateur `@testing` par défaut) et détectera les commentaires, les likes et les cadeaux.

5. Lorsqu'un événement est détecté, `tikLive.py` enverra une commande appropriée au serveur local via une requête POST, vous pouvez modifier les touches associé a l'émulateur dans `gift_to_commande_mapping{}`
   
```py
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

```
Il y a aussi une vérification des entré par le script `py_script.py`, vous pouvez modifier cette vérification a la ligne 84.
```py
   if commande in ['u', 'd', 'l', 'y', 'a', 'b', 'x', 's', 'c', 'o', 'r', 'w','U', 'D', 'L', 'Y', 'A', 'B', 'X', 'S', 'C', 'O', 'R', 'W']: 
      emulateur.press_key(commande)  # Appelle la méthode de l'objet EmulateurNDS pour simuler la pression de touche
      return jsonify({"id_commande": id_commande, "pass": True, "message": "Commande reçue et traitée"})
```
7. Le serveur local, géré par `py_script.py`, recevra la commande, simulant ensuite la pression de la touche correspondante sur l'émulateur Nintendo DS, si vous changer les touches associé dans `tikLive.py` il faudra faire les modifications approprié dans `py_script.py` pour accépter les bonnes touches 

8. Les spectateurs du stream TikTokLive peuvent ainsi influencer le gameplay de l'émulateur en envoyant différents événements et commandes.

## Remarques importantes

- Assurez-vous de respecter les règles d'utilisation de TikTokLive et de l'émulateur Nintendo DS, notamment en matière de droits d'auteur.

- Les scripts fonctionnent en collaboration pour offrir une expérience interactive pendant le stream TikTokLive. Assurez-vous de configurer correctement les chemins vers l'émulateur et le fichier ROM avant de lancer les scripts.

- Le mapping des touches pour les commandes NDS dans `py_script.py` mais dans `tikLive.py`, et peut être personnalisé en fonction de vos besoins.

- Gardez à l'esprit que l'utilisation de ce projet peut nécessiter l'autorisation des parties impliquées, y compris TikTok et les propriétaires de l'émulateur et du contenu ROM.


---

Note : Soyez conscient que l'utilisation de ces scripts pour interagir avec des services tiers comme TikTok peut être soumise à des restrictions et des règles spécifiques. Assurez-vous de les respecter et d'obtenir les autorisations nécessaires avant toute utilisation.
