# -*- coding: utf-8 -*-
import pyautogui
from flask import Flask, request, jsonify
import subprocess
import time
import psutil
from pynput.keyboard import Controller
import ctypes
import os
app = Flask(__name__)

class EmulateurNDS:
    def __init__(self, emulator_path, rom_path):
        self.keyboard = Controller()
        self.emulator_path = emulator_path
        self.rom_path = rom_path
        self.emulator_process = None
        self.emulator_process_pid = None
        self.emulator_window = None

    def launch_emulator(self):
        if self.emulator_process is not None:
            return True  # L'émulateur est déjà en cours d'exécution

        try:
            self.emulator_process = subprocess.Popen([self.emulator_path, self.rom_path])
            time.sleep(2)  # Attendre quelques secondes pour que l'émulateur démarre

            # Rechercher le processus "desmume.exe" parmi les processus en cours d'exécution
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'desmume.exe':
                    self.emulator_process_pid = proc.pid
                    break

            if self.emulator_process_pid is not None:
                print('Emulateur lancé PID : ' + str(self.emulator_process_pid))
                return True
            else:
                print("Le processus DeSmuME n'a pas été trouvé.")
                return False

        except Exception as e:
            print(f"Erreur lors du démarrage de l'émulateur : {e}")
            return False

    def get_pid(self):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'desmume.exe':
                self.emulator_process_pid = proc.pid
                print(f'PID du programme : {self.emulator_process_pid}')
                return proc.pid
#pyautogui.press(key, interval=0.03)  
    def press_key(self, key):
        self.get_pid()

        if self.emulator_process_pid is not None:
            try:
                # Utilise ctypes pour simuler la pression de la touche
                ctypes.windll.user32.keybd_event(ord(key), 0, 0, 0)
                time.sleep(0.1)  # Ajoute un court délai pour simuler le temps de pression de la touche
                ctypes.windll.user32.keybd_event(ord(key), 0, 2, 0)  # Relâche la touche
            except Exception as e:
                print(f"Erreur lors de l'envoi de la touche : {e}")
        else:
            print("L'émulateur n'est pas en cours d'exécution ou le PID est introuvable")
# Récupérer le chemin complet du fichier Python actuel
current_file_path = os.path.abspath(__file__)

# Récupérer le répertoire du fichier Python actuel
current_directory = os.path.dirname(current_file_path)

# Construire les chemins complets des autres fichiers ou dossiers nécessaires
current_directory_emulator = os.path.join(current_directory, "desmume", "desmume.exe")
current_directory_rom = os.path.join(current_directory, "desmume", "pokemon.nds")

# Maintenant, vous pouvez utiliser les chemins complets pour l'émulateur, etc.
emulateur = EmulateurNDS(current_directory_emulator, current_directory_rom)
@app.route('/commande', methods=['POST'])
def handle_command():
    data = request.get_json()
    commande = data.get('commande')
    id_commande = data.get('id_commande')
    print(f"Commande : {commande} - id_commande : {id_commande}")
    if commande in ['u', 'd', 'l', 'y', 'a', 'b', 'x', 's', 'c', 'o', 'r', 'w','U', 'D', 'L', 'Y', 'A', 'B', 'X', 'S', 'C', 'O', 'R', 'W']: 
        emulateur.press_key(commande)  # Appelle la méthode de l'objet EmulateurNDS pour simuler la pression de touche
        return jsonify({"id_commande": id_commande, "pass": True, "message": "Commande reçue et traitée"})
    else:
        return jsonify({"id_commande": id_commande, "erreur": "La commande n'est pas trouvée"})
if __name__ == '__main__':
    emulateur.launch_emulator()
    app.run()

"""
        [PARTERN TOUCHE] 
    GameTouche -> Keyboard
        L -> O
        R -> R 
        U -> UP
        L -> LEFT
        W -> RIGHT
        D -> DOWN
        C -> Select
        S -> Start
        X -> X
        A -> A
        Y -> Y
        B -> B
"""