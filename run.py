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
# SHEET = GSPREAD_CLIENT.open("enemy").sheet1
# RESETSHEET = GSPREAD_CLIENT.open("reset").sheet1
openai.api_key_path = "cred.txt"

fOne = r"Python-test\enemy.csv"
fTwo = r"Python-test\reset.csv"
SHEET = pd.read_csv(fOne)
RESETSHEET = pd.read_csv(fTwo)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

    # def reset():
    for i in range(1, SHEET.row_count):
        SHEET.delete_rows(SHEET.row_count)
    for i in range(2, RESETSHEET.row_count + 1):
        SHEET.append_row(RESETSHEET.row_values(i))


def reset():
    for i in range(1, len(SHEET)):
        SHEET.delete_rows(len(SHEET))
    for i in range(2, len(RESETSHEET + 1)):
        SHEET.append_row(RESETSHEET.row_values(i))


def menu(player):
    menu = {}
    menu["1."] = "Create your Hero"
    menu["2."] = "View Stats"
    menu["3."] = "Choose Opponent"
    menu["4."] = "View Wins"
    menu["5."] = "Quit"

    while True:
        print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\nGAME MENU:")
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
            enemy, healthPoints, num = getEnemy(opponentsLst())
            story(player, enemy)
            swordBattle(player, enemy, healthPoints, num)
        elif selection == "4":
            winsLst()
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


def winsLst():
    csvLst = SHEET.get_all_values()
    x = 1
    for row in csvLst:
        if row[3] == "0":
            print(f"{x}. {row[1]}")
            x += 1
        else:
            x = 1
    leave = input("Press Enter to return to menu:\n")


def swordBattle(player, enemy, healthPoints, num):
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

                dead = SHEET.row_values(num)
                dead[3] = 0
                SHEET.delete_rows(num)
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
                    f"{player.name.upper()} recieves a deadly blow. \n{enemy.name.upper()} lifts sword in triumph\n\n\t\tGAME OVER for {player.name.upper()}"
                )
                time.sleep(4)
                clear_screen()
                gameOver = input(
                    f"\n\n\t\t⚔⚔⚔---GAME OVER---⚔⚔⚔\n\nPress ENTER to reach menu:"
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
    name = input("Choose your characters name: \n")
    time.sleep(1)
    clear_screen()
    typeChoice = input(
        "Choose your characters type: \n1. Human\n2. Elf\n3. Dwarf\n4. Orc\n"
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
        strengthPoints = 10 + dice(3)
        healthPoints = 0 + dice(3)
        skillPoints = 0 + dice(3)
        armor = 10
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    else:
        print(f"Choices available are Human/Elf/Dwarf/Orc\nYou entered {name}")

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
        if statsPoints > 0:
            selectAttribute = input(f"Choose attribute: ")

        if statsPoints < 1:
            menu(player)

        if selectAttribute == "1":
            activateStatPoints = int(input(f"How many points do you wish to add"))
            if activateStatPoints <= statsPoints:
                player.strengthPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        elif selectAttribute == "2":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.healthPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        elif selectAttribute == "3":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.skillPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        elif selectAttribute == "4":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.armor += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered {selectAttribute}")
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
    return enemy, enemyVals[3], num


def story(player, enemy):
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f" {player.name} the {player.type} and {enemy.name} the {enemy.type} draws swords against eachother. A fight of life and death is about to start. Maximum length 60 words"
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
    reset()
    clear_screen()
    print(
        "\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\nA RPG-adventure game powered by the story-telling of chat-gpt\n\t\t      Now enter the realm"
    )
    player = "Hero has not been created"

    time.sleep(1)
    main()


main()
