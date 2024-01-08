import os
import random
from datetime import datetime
import sys

def game(player1):

  global fleur
  evenement_intro_dialogue, evenement_pnj_astronomie, antenne = True, True, True
  player_name = player1.player_name


  liste_refus_chemin = [
      "\033[91mChemin inacessible...\033[0m",
      "\033[91mLa forêt est trop dense...\033[0m",
      "\033[91mImpossible par ici.\033[0m",
      "\033[91mVous ne pouvez pas passer par là.\033[0m",
      "\033[91mUn obstacle bloque le chemin.\033[0m",
      "\033[91mC'est un cul-de-sac, essayez une autre direction.\033[0m",
      "\033[91mVous heurtez une barrière invisible.\033[0m",
      "\033[91mUn mystérieux pouvoir vous empêche d'avancer.\033[0m",
      "\033[91mLa voie est fermée pour le moment.\033[0m",
      "\033[91mLe joueur dit : 'C'est un mauvais chemin, essayons autre chose.'\033[0m",
      "\033[91mVous entendez le joueur murmurer : 'Un détour est nécessaire.'\033[0m",
      "\033[91mLe joueur marmonne : 'Peut-être qu'il y a un autre moyen.'\033[0m",
      "\033[91mVous dites à voix haute : 'Ce chemin semble bloqué.'\033[0m",
      "\033[91mLe joueur soupire : 'Il faut trouver une autre route.'\033[0m",
  ]

  def dialogue_intro():
    global icone
    nonlocal evenement_intro_dialogue
    icone = int(input("\nChoisissez une icone de joueur : \n1. 🔹\n2. 🔸\n"))
    print(' ')

    if evenement_intro_dialogue:
      player1.add_inventory('Couteau')
      print(f"""
      \033[34mLe vent murmure doucement à travers les feuilles denses de la forêt...<{player_name}> ouvre les yeux pour découvrir qu'il est allongé au cœur d'une nature mystique.
      À ses côtés, un sac en toile dégage un léger parfum de terre fraîche.
      Intrigué, il décide d'ouvrir le sac et y découvre un couteau rustique 🔪, qui scintille faiblement à la lueur des premiers rayons du soleil.
      Un mystérieux prospectus attire ensuite son attention, révélant des coordonnées énigmatiques : 'Antenne réseau - X: 2, Y: 1'.
      \033[3mLa densité de la forêt réduit considérablement la visibilité aux alentours, pense <{player_name}>. Naviguer ici ne sera pas facile.\033[0m\033[0m

      \033[92mℹ️ : info utile ➜\033[0m La map indique votre position en temps réel, avec les possibilités de déplacement et affiche les zones déjà explorées.
      Déplacez-vous avec les touches 'z' (haut), 's' (bas), 'q' (gauche), 'd' (droite).
      La visibilité est limitée autour de vous. Les terrains explorés seront affichés.
      """)
      evenement_intro_dialogue = False

  def dialogue_pnj_astronomie():
    nonlocal evenement_pnj_astronomie
    if evenement_pnj_astronomie:
      print("👤 \033[34mVous repérez une silhouette à l'horizon. Que souhaitez-vous faire ?\033[0m\033[0m\n")

      while True:
          ask = input("1. Engager la conversation\n"
                      "2. Continuer votre chemin et revenir plus tard .")

          if ask in ('1', '2'):
              break
          else:
              print("Veuillez entrer uniquement 1 ou 2. Réessayez.")

      if ask == '1':
        print(f"""🙋‍♂️ : \033[34m« Hey, tu n’es pas encore allé à l'Ouest de la montagne, n’est-ce pas ? » demande un homme à l'allure ordinaire.
        On y raconte que les étoiles nous aident lorsqu'on a besoin d'elles...
        <{player_name}> : «Je devrais sûrement l'écouter, ça me fait toujours une potentielle piste.»\033[0m\033[0m""")

  dialogue_roche_bloque = "\033[34mVous avez rencontré une 🪨 roche. Impossible de passer sur votre gauche pour le moment. \033[0m\033[0m"
  dialogue_montagne = "⭐ Plus loin au Nord se trouve un élément dont vous avez besoin, le chemin semble bloqué par une 🪨 roche imposante..."
  dialogue_intro()



  map = [
      ["🌲", "┏", "┲", "┓", "🌱"],
      ["🌲", "┗", "╇", "┨", "┃"],
      ["🌳", "🌳", "┡", "┨", "┃"],
      ["🏔️", "─", "╋", "┷", "┛"],
      ["🌳", "🌲", "↓", "🌲", "🌳"],
      ["🌳", "🌳", "🌲", "🌲", "🌳"]
  ]


  map_mask = [
      ["☁️", "☁️", "☁️", "☁️", "☁️"],
      ["☁️", "☁️", "☁️", "☁️", "☁️"],
      ["☁️", "☁️", "☁️", "☁️", "☁️"],
      ["☁️", "☁️", "☁️", "☁️", "☁️"],
      ["☁️", "☁️", "☁️", "☁️", "☁️"],
      ["☁️", "☁️", "☁️", "☁️", "☁️"]
  ]


  def afficher_carte(carte, joueur_x, joueur_y, visibilite):
    max_largeur = max(len(element) for ligne in carte for element in ligne)

    for i, ligne in enumerate(carte):
        for j, case in enumerate(ligne):
            distance = max(abs(i - joueur_x), abs(j - joueur_y))
            if distance <= visibilite and not (
                (distance == 1 and abs(i - joueur_x) == 1 and abs(j - joueur_y) == 1)
            ):
                if i == joueur_x and j == joueur_y:
                    if icone == 1:
                        print("🔹", end=" ")
                    elif icone == 2:
                        print("🔸", end=" ")
                else:
                    print(case, end=" ")
            else:
                print("☁️", end=" ")
        print()

# Le reste du code reste inchangé...




  def deplacer(x, y, direction):
      nonlocal position_x, position_y
      if direction == 'z' and x > 0:
          x -= 1
      elif direction == 's' and x < len(map) - 1:
          x += 1
      elif direction == 'q' and y > 0:
          y -= 1
      elif direction == 'd' and y < len(map[0]) - 1:
          y += 1
      elif direction == 'exit':
        return

      print(f'Position actuelle : {map[x][y]}')
      return x, y


  def valid_move(position_x, position_y, direction):

      current_cell = map[position_x][position_y]
      evenement(direction, current_cell, player1)

      if current_cell == "┏":
          if direction == 's' or direction == 'd':
              return True
          return False

      elif current_cell == "┗":
        if direction == 'd' or direction == 'z':
            return True
        return False

      elif current_cell == map[3][2] and direction == 's':
          if antenne == False:
            return True
          return 'acces_bloque', False

      elif current_cell == '╇':
        if direction == 'd' or direction == 'z' or direction == 'q':
          return True
        else:
          return False

      elif current_cell == "╋":
        if direction == 'd' or direction == 'z' or direction == 'q' or direction == 's':
            return True
        return False

      elif current_cell == "┗":
        if direction == 'd' or direction == 'z':
            return True

      elif current_cell == "┨" or current_cell == "┃":
          if direction == 's' or direction == 'z':
              return True
          return False

      elif current_cell == "┛":
        if direction == 'q' or direction == 'z':
            return True
        return False

      elif current_cell == "─" or current_cell == "┷":
        if direction == 'q' or direction == 'd':
            return True
        return False

      elif current_cell == "┲":
        if direction == 's' or direction == 'd':
            return True
        return False

      elif current_cell == "┡":
        if direction == 'z' or direction == 'd':
            return True
        return False

      elif current_cell == "🏔️":
        if direction == 'd':
            return True
        return False

      elif current_cell == "🌱":
        if direction == 's':
            return True
        return False

      elif current_cell == "┓":
        if direction == 's' or direction == 'q':
            return True
        return False

      else:return False

  def evenement(direction, current_cell, player):

    if current_cell == map[3][4] and direction == 'q':
        print('🌲 \033[33mVous entrez dans la forêt.\033[0m\n')

    if current_cell == map[3][1] and direction == 'd':
        print('🌲 \033[33mVous entrez dans la forêt.\033[0m\n')

    if current_cell == map[3][3] and direction == 'd':
        print('🕳️ \033[33mVous entrez dans la grotte.\033[0m\n')

    if current_cell == map[3][2] and direction == 'q':
        print('⛰️ \033[33mVous entrez dans la montagne du Sud.\033[0m\n')
        dialogue_pnj_astronomie()

    if current_cell == map[0][2] and direction == 'd':
        player.event_sceau_deau()

    if current_cell == map[1][3] and direction == 'z':
        player.event_sceau_deau()

    if current_cell == map[0][2] and direction == 's':
      player.dialogue_antenne()

    if current_cell == map[2][2] and direction == 'z':
      player.dialogue_antenne()

    if current_cell == map[1][1] and direction == 'd':
      player.dialogue_antenne()

    if current_cell == map[1][4] and direction == 'z':
      player.dialogue_fleur()

    if current_cell == map[1][2] and direction == 'q':
      player.dialogue_pnj_plante()

    if "Fleur" in player.item:
        print("""\033[34mLe PNJ vous remarque et s'exclame : 'Ah, vous avez une plante !'
              Vous décidez de donner la plante au PNJ en échange d'une ⛏️​ pioche.\033[0m\033[0m""")

        player.item.remove("Fleur")
        player.item.append("Pioche")

        print("Le PNJ vous donne une pioche en échange de la plante. Vous obtenez la ⛏️​ pioche.")

    if current_cell == map[3][2] and direction == 's' and PlayerRPG.evenement_antenne == False:

        print("""\033[34mVous vous trouvez à l'entrée d'une zone dangereuse.\nCette zone est réputée pour être infestée de monstres redoutables.\033[0m\033[0m""")


        while True:
          ask = input("\nSouhaitez-vous y accéder ?\n1. Oui\n2. Non \n:")

          if ask == "1":
              print("Vous avancez courageusement dans la zone dangereuse.")
              player.chest()
              monstre = Monster()
              resultat_combat = Monster.boss(player1, monstre)
              print(resultat_combat)

              return True
          elif ask == "2":
              print("Vous décidez de ne pas risquer votre vie pour le moment.")
              return False
          else:
              print("Choix invalide. Veuillez entrer 1 pour 'Oui' ou 2 pour 'Non'.")

    if current_cell == map[1][1] and direction == 'z':

      if 'Pioche' in player.item:
        utiliser_pioche = input("Voulez-vous utiliser la pioche pour casser la roche 🪨⛏️​ ?\n1. Oui\n: ")

        if utiliser_pioche == '1':
            print("\033[34mLe chemin vers la gauche est maintenant débloqué.\033[0m\033[0m")
            player.item.append("Batterie")
            print("\033[34mVous trouvez une batterie pour le générateur dans la zone débloquée.\033[0m\033[0m")

            return True

        else:
            print("Choix invalide. Veuillez entrer 1 pour 'Oui'.")
      else:
        print(dialogue_roche_bloque)

    if current_cell == map[3][1] and direction == 'q':
      print(dialogue_montagne)
      
    return False







  def open_map():
    nonlocal position_x, position_y
    nonlocal visibilite
    map_mask[position_x][position_y] = map[position_x][position_y]
    afficher_carte(map_mask, position_x, position_y, visibilite)
    print(' ')

    while True:
        print("\033[32mDans quelle direction souhaitez-vous vous déplacer (haut : z, bas : s, gauche : q, droite : d) ou <exit_map> ? \033[0m")
        direction = input()
        direction = direction.lower()

        if direction == 'exit_map':
            break

        result = valid_move(position_x, position_y, direction)

        if result is True:
            position_x, position_y = deplacer(position_x, position_y, direction)
            map_mask[position_x][position_y] = map[position_x][position_y]
            afficher_carte(map_mask, position_x, position_y, visibilite)
            print(' ')
        else:
            if result == 'acces_bloque':
                print('\033[91mCette zone est trop dangereuse pour le moment...\033[91m')
            else:
                random_message = random.randint(0, len(liste_refus_chemin) - 1)
                print(liste_refus_chemin[random_message])
                print(' ')


  #inialisation des variables par défaut
  position_x = 0
  position_y = 2
  visibilite = 1

  while True:
      user_choice = input(
          "\nQue voulez-vous faire ?\n"
          "1. Ouvrir la carte\n"
          "2. Ouvrir l'inventaire\n"
          "3. Retourner au menu principal\n"
          "Choisissez une option (1-3): ")

      if user_choice == '1':
          print("\nVous avez choisi d'ouvrir la carte.")
          open_map()

      elif user_choice == '2':
          print("Vous avez choisi d'ouvrir l'inventaire.")
          player1.open_inventory()

      elif user_choice == '3':
          print("Retour au menu principal.")
          break

      elif user_choice.lower() == 'exit':
          print("Au revoir !")
          exit()

      else:
          print("Veuillez entrer une option valide (1-3).")

















# CLASS Menu ---------------------------------------------------------------

class Menu:
    def __init__(self):
        self.player_name = None
        self.game_loaded = False
        self.sauvegardes_dir = 'sauvegardes'
        os.makedirs(self.sauvegardes_dir, exist_ok=True)

    def show_main_menu(self):
        print("\033[92m\n››› RPG Menu Principal ‹‹‹\033[0m\n\033[1m1.\033[0m Créer une nouvelle partie\n\033[1m2.\033[0m Charger une partie sauvegardée\n\033[1m3.\033[0m À propos\n\033[1m4.\033[0m Quitter\n")

    def create_new_game(self):
        global player1
        print("\nCréation d'un nouveau jeu...")
        player_name = input("Saisissez le nom de votre personnage : ✎")
        self.player_name = player_name
        player1 = PlayerRPG(self.player_name)

        print(f"Bienvenue, {self.player_name}! Votre aventure commence.")

        nom_fichier = input("Enter the save file name (without extension): ")
        date_actuelle = datetime.now()
        format_date = date_actuelle.strftime("%Y%m%d_%H%M%S")
        nom_complet_fichier = os.path.join(self.sauvegardes_dir, f"{nom_fichier}_{format_date}.txt")

        with open(nom_complet_fichier, 'w') as fichier:
            fichier.write(f"Enregistrer le fichier pour {self.player_name} crée le {format_date}.")

        print(f"Jeu chargé avec succès.: {nom_complet_fichier}")
        game(player1)


    def load_saved_game(self):
        global player1
        if self.game_loaded:
            print("\nJeu déjà chargé.")
        else:
            print("\nChargement en cours...")
            self.game_loaded = True
            print("Jeu chargé avec succès.")
            self.player1 = PlayerRPG(self.player_name)
            game(self.player1)

    def about(self):
        print("\n=== A propos ===\nC'est simplement un jeu RPG...\nCrée par Kylian & Kémil.")

    def run(self):
        while True:
            self.show_main_menu()
            choice = input("Entrée un choix (1-4): ")

            if choice == '1':
                self.create_new_game()
            elif choice == '2':
                self.load_saved_game()
            elif choice == '3':
                self.about()
            elif choice == '4':
                print("Au revoir !")
                break
            else:
                print("Choix invalide (1-4!)")













# CLASS PlayerRPG ---------------------------------------------------------------

class PlayerRPG:

    evenement_sceau_deau, fleur, evenement_antenne = True, True, True

    def __init__(self, player_name):
        self.player_name = player_name
        self.strength = 10
        self.defense = 0
        self.hp = 100
        self.item = []
        self.attack = {'hit': 25, 'special': 70}

    def __str__(self):
        return f"PlayerRPG object: {self.player_name}"

    def add_inventory(self, item):
        self.item.append(item)

    def open_inventory(self):
      if not self.item:
          print('Aucun item disponible')
      else:
          print("Inventaire:")
          for i, item in enumerate(self.item, start=1):
              print(f"{i}. {item}")
      return self.item

    def use_item(self, item_index):
        if 0 <= item_index < len(self.item):
            item_use = self.item[item_index]

            if item_use == 'Potion heal':
                self.hp += 50
                self.item.remove(item_use)
                print(f"{item_use} utilisée, vos points de vie actuels : {self.life()}.")

            elif item_use == 'Potion strength':
                self.strength += 30
                self.item.remove(item_use)
                print(f"{item_use} utilisée, ajout de {self.strength} points de force.")

            elif item_use == 'Potion defense':
                self.defense += 25
                self.item.remove(item_use)
                print(self.defense)
                print(f"{item_use} utilisée, ajout de {self.defense} points de bouclier.")
        else:
            print("Index d'item invalide.")

    def life(self):
        dico_life = {
            1 : "🧡",
            2 : "❤️❤️",
            3 : "❤️❤️🧡",
            4 : "❤️❤️❤️❤️",
            5 : "❤️❤️❤️❤️🧡",
            6 : "❤️❤️❤️❤️❤️❤️",
            7 : "❤️❤️❤️❤️❤️❤️🧡",
            8 : "❤️❤️❤️❤️❤️❤️❤️❤️",
            9 : "❤️❤️❤️❤️❤️❤️❤️❤️🧡",
            10: "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"}

        if self.hp > 100:
            return("Points de vie invalides")

        num_hearts_entiers = self.hp // 10

        if num_hearts_entiers > 0:
              return(dico_life[num_hearts_entiers])
        else:
            return str("Joueur mort...")

    def event_sceau_deau(self):
      if PlayerRPG.evenement_sceau_deau:
        self.item.append("Sceau d'eau")
        print("\033[34m Tu as trouvé un sceau d'eau! \033[0m\033[0m")
        PlayerRPG.evenement_sceau_deau = False

    def dialogue_fleur(self):
        if PlayerRPG.fleur:
            print("\033[34mOh, il y a une pousse de fleur ici. Si seulement elle avait de l'eau 💧 pour pousser...\033[0m\033[0m")

            choix_arroser = 0
            while choix_arroser not in [1, 2]:
                if "Sceau d'eau" in self.item:
                    choix_arroser = int(input("Que souhaitez-vous faire ?\n1. Arroser la fleur\n2. Ne rien faire\n"))

                    if choix_arroser == 1:
                        print("Vous arrosez la fleur 💧🌱.")
                        self.item.remove("Sceau d'eau")
                        print("\033[34mLa fleur pousse et s'épanouit\033[0m\033[0m 🌹.")
                        print("1. Récupérer la fleur et l'ajouter à l'inventaire.")

                        choix_recuperer = 0
                        while choix_recuperer not in [1]:
                            choix_recuperer = int(input())
                            if choix_recuperer == 1:
                                print("\033[34mVous récupérez la fleur 🥀​ et l'ajoutez à votre inventaire.\033[0m\033[0m")
                                self.item.append('Fleur')
                                PlayerRPG.fleur = False
                            else:
                                print("Choix invalide. Veuillez choisir une option valide.")
                    elif choix_arroser == 2:
                        print("Vous choisissez de ne rien faire.")
                    else:
                        print("Choix invalide. Veuillez choisir une option valide.")
        else:
            print("Malheureusement, vous ne possédez pas de sceau d'eau pour arroser cette fleur.")




    def dialogue_pnj_plante(self):
      global player1

      if PlayerRPG.fleur == False:
        if PlayerRPG.fleur == 'Off':
          print("""👨‍🌾 : \033[34mJ'espère que tu feras bon usage de cette pioche et encore merci pour cette magnifique fleur !\033[0m\033[0m""")
        else:
          print("\033[34mUn PNJ est là, observant la plante que vous portez.\033[0m\033[0m")
          print("\033[34mLe PNJ s'approche de vous et dit : 'Oh, cette plante est magnifique !\033[0m\033[0m")
          print("\033[34mAccepteriez-vous de me la donner en échange de cette ⛏️​ pioche ?\033[0m\033[0m")

          choix_echange = input("1. Accepter l'échange :\n")

          if choix_echange == '1':
              print("⛏️​ Pioche récupérée !")
              self.item.append("Pioche")
              print("Le PNJ vous donne une pioche en échange de la plante. Vous obtenez la ⛏️​ pioche.")
              PlayerRPG.fleur = 'Off'

      elif PlayerRPG.fleur and 'Fleur' not in self.item:

          print("\n👨‍🌾 \033[34mAh, merci de prendre le temps de m'écouter. C'est notre 20e anniversaire de mariage avec ma femme bien-aimée, et je veux lui offrir quelque chose de spécial.\033[0m\033[0m")
          print(" \033[34mIl y a une fleur rare qui pousse dans une grotte une fois tous les 10 ans. C'est magnifique, et je suis sûr que ma femme l'adorerait.\033[0m\033[0m")
          print(" \033[34mLe seul problème, c'est que je ne peux plus me faufiler dans cette grotte comme avant. Les années ont ralenti mes pas, vous comprenez ?\033[0m\033[0m")
          print(" \033[34mSi vous pouviez récupérer cette fleur pour moi, je serais éternellement reconnaissant. La grotte se trouve juste au Sud Ouest d'ici.\033[0m\033[0m")

    def dialogue_antenne(self):
        if "Batterie" in self.item:
            ask = input("Voulez-vous insérer la batterie 🔋​ dans le générateur ?\n1. Oui\n: ")

            if ask == '1':
                self.item.remove("Batterie")
                print("\033[34mSoudain, un signal 📟 est capté en provenance du Sud.\n🧭​ Coordonnées du signal : x:3, y:2.\033[0m\033[0m")
                PlayerRPG.evenement_antenne = False

            else:
                print("Choix invalide. Veuillez entrer 1 pour 'Oui'.")

        if PlayerRPG.evenement_antenne:
            print("""\033[34mVous découvrez l'antenne 📡 de communication, seulement elle semble éteinte 🪫.  «Il faut trouver le générateur...»\033[0m\033[0m""")


    def chest(self):
      print("Vous avez trouvé un coffre enfoui!")
      ask = input("Voulez-vous l'ouvrir? (1. Oui / 2. Non): \n ")

      if ask == "1":
          self.item.append('Potion heal')
          self.item.append('Potion heal')
          self.item.append('Potion strength')
          self.item.append('Potion defense')
          print("""Vous avez ouvert le coffre et trouvé des potions dans votre inventaire!\n x2 : ​❤️ Potion de vie\ x1 : 💪 Potion de force\n x1 : 🛡️ Potion de défense\n""")
      else:
          print("Vous décidez de ne pas ouvrir le coffre.\n")







# CLASS Monster ---------------------------------------------------------------

class Monster:

    def __init__(self, strength=10, defense=15, hp=100, attack=None):
        self.strength = strength
        self.defense = defense
        self.hp = hp
        self.attack = {'uppercut': 20, 'impulse': 15, 'kick': 30}


    def life(self):
      dico_life = {
          1: "🧡",
          2: "❤️❤️",
          3: "❤️❤️🧡",
          4: "❤️❤️❤️❤️",
          5: "❤️❤️❤️❤️🧡",
          6: "❤️❤️❤️❤️❤️❤️",
          7: "❤️❤️❤️❤️❤️❤️🧡",
          8: "❤️❤️❤️❤️❤️❤️❤️❤️",
          9: "❤️❤️❤️❤️❤️❤️❤️❤️🧡",
          10: "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"}

      if self.hp > 100:
          return "Points de vie invalides"

      num_hearts_entiers = self.hp // 10

      if num_hearts_entiers > 0:
          return dico_life[num_hearts_entiers]
      else:
          return str("Monstre vaincu!")

    def boss(player, monster):
        print("\033[91mUn monstre devant ! Faites attention\033[0m")

        choice = int(input("1. Attaquer\n2. Fuir\nChoisissez une option : "))

        if choice == 2:
            tentative_fuite = random.randint(0, 100)
            if 0 < tentative_fuite < 80:
                return "Fuite réussie"
            else:
                print("\033[91mFuite ratée, combat obligatoire\033[0m")

        print(f"Votre liste d'attaques est la suivante : {player.attack}")
        print(' ')

        while player.hp > 0 and monster.hp > 0:
            player.hp += player.defense
            print(f"Le monstre a {monster.life()} points de vie.")

            attack_player = int(input("1. Attaque normale\n2. Attaque spéciale\nChoisissez une attaque : "))

            while attack_player not in [1, 2]:
                attack_player = int(input("1. Attaque normale\n2. Attaque spéciale\nChoisissez une attaque : "))

            attack_player = 'hit' if attack_player == 1 else 'special'

            if random.random() <= 0.80 if attack_player == 'hit' else 0.20:
                monster.hp -= (player.attack[attack_player] + player.strength)
                print(f"⚔️ Vous avez touché avec votre attaque {attack_player}! Il reste {monster.life()} points de vie au monstre.")
            else:
                print("L'attaque a raté.")

            if monster.hp <= 0:
                print(f"\033[91mLe monstre est vaincu !\033[0m \nFélicitations vous avez libéré la forêt de cette aura mystérieuse, un signal d'urgence a été envoyé à l'équipe de secours la plus proche !")
                sys.exit()

            elif player.hp <= 0:
                sys.exit()
                print('\033[91mVous êtes mort.\033[0m')

            attaques_possibles = list(monster.attack.keys())
            attaque_choisie = random.choice(attaques_possibles)
            puissance_attaque = monster.attack[attaque_choisie]

            if random.random() <= 0.40:
                player.hp -= puissance_attaque
                print(f"👾 L'attaque du monstre a touché, il vous reste {player.life()} points de vie.")
            else:
                print("Vous avez esquivé l'attaque adverse.")

            print(' ')

            ask_invy = int(input("1. Ouvrir l'inventaire\n2. Continuer le combat\nChoisissez une option : "))

            if ask_invy == 1:
                inventory = player.open_inventory()
                print(inventory)
                if not inventory:
                    print("Aucun item disponible dans votre inventaire.")
                else:
                    ask_use = int(input(f"Choisissez l'item à utiliser (1-{len(inventory)}): "))





#Menu ---------------------------------------------------------------
player1 = None
monster1 = Monster()
if __name__ == "__main__":
    rpg_game = Menu()
    rpg_game.run()