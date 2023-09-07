import random, pprint, os, time, gspread, csv, openai
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("cred.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("enemy").sheet1
openai.api_key_path = "cred.txt"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu(player):
    menu = {}
    menu["1"] = "Create your Hero"
    menu["2"] = "View Stats"
    menu["3"] = "Choose Opponent"
    menu["4"] = "View Wins"
    menu["5"] = "Quit"

    while True:
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please select an option: ")
        if selection == "1":
            characterInput()
        elif selection == "2":
            print(player)
        elif selection == "3":
            enemy, healthPoints = getEnemy(opponentsLst())
            story(player, enemy)
            swordBattle(player, enemy, healthPoints)
        elif selection == "4":
            print("You selected 'View Wins'.")
        elif selection == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option selected. Please try again.")


def opponentsLst():
    csvLst = SHEET.get_all_values()
    x = 0
    for row in csvLst:
        if x != 0 and row[3] != "0":
            print(f"{x}. {row[1]}")
            x += 1
        else:
            x += 1
    opponent = input("Please select an option: ")
    return int(opponent) + 1


def swordBattle(player, enemy, healthPoints):
    clear_screen()
    print(f"\t\t⚔⚔⚔---Battle---⚔⚔⚔")
    while True:
        attack = (player.skillPoints + dice(3)) - (enemy.skillPoints + dice(3))
        time.sleep(1)
        if attack == 0:
            print(f"The swords clash and no damage is dealt to either opponent")
        if attack > 0:
            damage = attack + player.strengthPoints - player.armor
            print(f"{player.name} strikes {enemy.name} who looses {damage} HP")
            enemy.healthPoints -= damage
            print(f"{enemy.name} now has {enemy.healthPoints} HP left")
            if enemy.healthPoints < 1:
                print(
                    f"{enemy.name.upper()} recieves a deadly blow. \n{player.name.upper()} lifts the sword in triumph"
                )
                dead = SHEET.row_values(2)
                dead[3] = 0

                SHEET.append_row(dead)

                break
        if attack < 0:
            damage = abs(attack) + enemy.strengthPoints - player.armor
            print(
                f"{enemy.name.upper()} strikes {player.name.upper()} who looses {damage} HP"
            )
            player.healthPoints -= damage
            print(f"{player.name} now has {player.healthPoints} HP left")
            if player.healthPoints < 1:
                print(
                    f"{enemy.name.upper()} recieves a deadly blow. \n{player.name.upper()} lifts sword in triumph"
                )
                menu(player)


class CharacterStats:
    """
    The object collects the character stats
    """

    def __init__(self, type, name, strengthPoints, healthPoints, skillPoints, armor):
        self.type = type
        self.name = name
        self.strengthPoints = strengthPoints
        self.healthPoints = healthPoints
        self.skillPoints = skillPoints
        self.armor = armor

    def __str__(self):
        return f"{self.name.upper()} THE MIGHTY {self.type.upper()}\nSTRENGTH:\t{self.strengthPoints}\nHEALTH:\t\t{self.healthPoints}\nSWORD SKILL:\t{self.skillPoints}\nARMOR:\t\t{self.armor}"


def dice(num):
    result = 0
    total = 0
    for i in range(num):
        result = random.randint(1, 6)
        total += result
    return total


def characterInput():
    name = input("Choose your characters name\n")
    time.sleep(1)
    clear_screen()
    typeChoice = input(
        "Choose your characters type\n1. Human\n2. Elf\n3. Dwarf\n4. Orc\n"
    ).lower()
    time.sleep(1)
    clear_screen()
    if typeChoice == "1" or "human":
        type = "human"
        strengthPoints = 5 + dice(3)
        healthPoints = 5 + dice(3)
        skillPoints = 5 + dice(3)
        armor = 5
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if typeChoice == "2" or "elf":
        type = "elf"
        strengthPoints = 0 + dice(3)
        healthPoints = 0 + dice(3)
        skillPoints = 10 + dice(3)
        armor = 5
        statsPoints = dice(10)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if typeChoice == "3" or "dwarf":
        type = "dwarf"
        strengthPoints = 10 + dice(3)
        healthPoints = 0 + dice(3)
        skillPoints = 0 + dice(3)
        armor = 15
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if typeChoice == "4" or "Orc":
        type = "orc"
        strengthPoints = 10 + dice(6)
        healthPoints = 0 + dice(6)
        skillPoints = 0 + dice(6)
        armor = 10
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    else:
        print(f"Choices available are for Human/Elf/Dwarf/Orc\nYou wrote {name}")

    print(player)
    addStatsPoints(player, statsPoints)
    return player


def addStatsPoints(player, statsPoints):
    while True:
        time.sleep(2)
        clear_screen()
        print(f"You have {statsPoints} points to add to your stats")
        print(
            f"What stats would you like to improve?\n1. STRENGTH:\t{getattr(player, 'strengthPoints')}\n2. HEALTH:\t{getattr(player, 'healthPoints')}\n3. SWORD SKILL:\t{getattr(player, 'skillPoints')}\n4. ARMOR:\t{getattr(player, 'armor')}\n"
        )
        if statsPoints < 1:
            menu(player)
        selectAttribute = input(f"Choose attribute 1/2/3/4: ")
        if selectAttribute == "1":
            activateStatPoints = int(input(f"How many points do you wish to add"))
            if activateStatPoints <= statsPoints:
                player.strengthPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        if selectAttribute == "2":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.healthPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        if selectAttribute == "3":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.skillPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        if selectAttribute == "4":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.armor += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)

        print(player)


def getEnemy(num):
    enemyVals = SHEET.row_values(num)
    type = enemyVals[0]
    name = enemyVals[1]
    strengthPoints = int(enemyVals[2])
    healthPoints = int(enemyVals[3])
    skillPoints = int(enemyVals[4])
    armor = int(enemyVals[5])
    enemy = CharacterStats(type, name, strengthPoints, healthPoints, skillPoints, armor)
    return enemy, enemyVals[3]


def story(player, enemy):
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f" {player.name} the {player.type} and {enemy.name} the {enemy.type} draws swords against eachother. A battle between them is to start when the story ends. Maximum length 60 words"
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    print(f"A Lord of the Strings tale: {reply}")
    messages.append({"role": "assistant", "content": reply})
    startBattle = input(f"\nPress Enter to start the battle")


def main():
    clear_screen()
    print(
        "\t\tWelcome to LORD OF THE STRINGS\nA RPG-adventure game powered by the story-telling of chat-gpt\n\t\t      Now enter the realm"
    )
    player = "Hero has not been created"

    time.sleep(1)
    menu(
        player,
    )


main()
