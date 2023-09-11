import random, pprint, os, time, gspread, csv, openai
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("enemy").sheet1
RESETSHEET = GSPREAD_CLIENT.open("reset").sheet1


def configure():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def leave():
    leave = input(f"\nMenu press Enter: ")
    clear_screen()


def readEnemyCSV():
    enemyLst = SHEET.get_all_values()[1:]
    return enemyLst


def download(enemyLst):
    addEnemyLst = RESETSHEET.get_all_values()[1:]
    for row in enemyLst:
        addEnemyLst.append(row)
    enemyLst = addEnemyLst
    return enemyLst


# def readEnemyCSV():
#     enemyLst = []
#     with open("Python-test\enemy.csv", newline="") as enemyFile:
#         reader = csv.reader(enemyFile, delimiter=",", quotechar='"')
#         for row in reader:
#             enemyLst.append(row)
#     return enemyLst


# def resetEnemyCSV(enemy):
#     enemyLst = []
#     with open("Python-test\enemy.csv", "w", newline="") as enemyFile:
#         writer = csv.writer(enemyFile)
#         writer.writerows([])
#     with open("Python-test\enemy_reset.csv", newline="") as resetFile:
#         reader = csv.reader(resetFile, delimiter=",", quotechar='"')
#         for row in reader:
#             enemyLst.append(row)
#     print(enemy)
#     with open("Python-test\enemy.csv", "w", newline="") as enemyFile:
#         writer = csv.writer(enemyFile)
#         writer.writerows(enemyLst)


# def updateEnemyCsv(enemyLst):
#     with open("Python-test\enemy.csv", "w", newline="") as enemyFile:
#         writer = csv.writer(enemyFile)
#         writer.writerows([])
#     with open("enemy.csv", "w", newline="") as enemyFile:
#         writer = csv.writer(enemyFile)
#         writer.writerows(enemyLst)


# def download():
#     csvLst = SHEET.get_all_values()
#     enemyLst = readEnemyCSV()[1:]
#     for row in enemyLst:
#         csvLst.append(row)
#     if len(csvLst) < 21:
#         with open("Python-test\enemy.csv", "w", newline="") as enemyFile:
#             writer = csv.writer(enemyFile)
#             writer.writerows(csvLst)
#     else:
#         print("list of opponents already updated")
#         leave()


def menu(player, enemyLst):
    menu = {}
    menu["1."] = "Create New Hero"
    menu["2."] = "View Stats"
    menu["3."] = "Choose Opponent"
    menu["4."] = "View Wins"
    menu["5."] = "Download New Opponents"
    menu["6."] = "Reset Opponents To Start Settings"
    menu["7."] = "Quit Game"

    while True:
        print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\nGAME MENU:")
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please select an option: ")
        if selection == "1":
            characterInput(enemyLst)
        elif selection == "2":
            clear_screen()
            print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")
            print(player)
            leave()
        elif selection == "3":
            clear_screen()
            print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")
            player, enemyLst, num = opponentsLst(player, enemyLst)
            enemy, healthPoints, num = getEnemy(enemyLst, num)
            story(player, enemy)
            swordBattle(player, enemyLst, enemy, healthPoints, num)
        elif selection == "4":
            clear_screen()
            print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")
            print("")
            winsLst(enemyLst)
        elif selection == "5":
            download(enemyLst)
            print("New Opponents Successfully Downloaded")

        elif selection == "6":
            # resetEnemyCSV()
            readEnemyCSV()
            print
        elif selection == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option selected. Please try again.")


def opponentsLst(player, enemyLst):
    # enemyLst = readEnemyCSV()
    twoColLst = []
    x = 1
    columns = 2
    for row in enemyLst:
        if row[3] != 0:
            twoColLst.append(f"{x}. {row[1].upper()}")
            x += 1

    for first, second in zip(twoColLst[::columns], twoColLst[1::columns]):
        print(f"{first: <10}\t\t{second: <10}")

    if player != "Hero has not been created":
        opponent = input("Please select an opponent or 'M' for back to menu: ").lower()
        x = 0
        for row in enemyLst:
            if row[3] != 0:
                x += 1
                if int(opponent) == x:
                    num = int(opponent) - 1
                    return player, enemyLst, num

                    break
            if opponent == "m":
                menu(player, enemyLst)
        else:
            print("Pick a number from the list or 'M' menu.\nYou entered {opponent}")

    else:
        print("No Hero Created. Please Go To Menu")
        menu(player, enemyLst)


def winsLst(enemyLst):
    # csvLst = SHEET.get_all_values()
    # enemyLst = readEnemyCSV()
    x = 1
    for row in enemyLst:
        if row[3] == 0:
            print(f"{x}. {row[1]}")
            x += 1
        else:
            x = 1
    leave()


def swordBattle(player, enemyLst, enemy, healthPoints, num):
    clear_screen()
    print(f"\t\t⚔⚔⚔---Battle---⚔⚔⚔")
    while True:
        attack = (player.skillPoints + dice(6)) - (enemy.skillPoints + dice(6))
        time.sleep(1)
        if attack == 0:
            print(f"The swords clash and no damage is dealt to either opponent")
            time.sleep(1)
        if attack > 0:
            damage = dice(1) + player.strengthPoints - player.armor
            print(f"{player.name} strikes {enemy.name} who looses {damage} HP")
            enemy.healthPoints -= damage
            print(f"{enemy.name} now has {enemy.healthPoints} HP left")
            time.sleep(1)
            if enemy.healthPoints < 1:
                print(
                    f"{enemy.name.upper()} recieves a final blow. \n{player.name.upper()} lifts the sword in triumph"
                )
                battlteOver = input(
                    f"The fight is over {enemy.name.upper()} is defeated. Press enter to continue the quest: "
                )
                time.sleep(1)
                # enemyLst = readEnemyCSV()
                dead = enemyLst[num]
                dead[3] = 0
                enemyLst.pop(num)
                enemyLst.append(dead)
                menu(player, enemyLst)
                # updateEnemyCsv(enemyLst)
        if attack < 0:
            damage = dice(1) + enemy.strengthPoints - player.armor
            print(
                f"{enemy.name.upper()} strikes {player.name.upper()} who looses {damage} HP"
            )
            player.healthPoints -= damage
            print(f"{player.name} now has {player.healthPoints} HP left")
            if player.healthPoints < 1:
                print(
                    f"{player.name.upper()} recieves a final blow. \n{enemy.name.upper()} lifts sword in triumph"
                )
                battlteOver = input("The fight is over. Press enter: ")
                clear_screen()
                print(
                    f"\n\n\t\t⚔⚔⚔---GAME OVER---⚔⚔⚔\n\n \n\n\t\t\t☩‌☩‌☩---{player.name.upper()}‌---☩‌☩‌☩"
                )
                leave()
                main()
                break


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


def characterInput(enemyLst):
    clear_screen()
    print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\n")
    print(f"HERO")
    name = input("NAME: ")
    time.sleep(1)
    typeChoice = input("1. Human\n2. Elf\n3. Dwarf\n4. Orc\n\nTYPE: ").lower()
    time.sleep(1)
    clear_screen()
    if typeChoice == "1" or typeChoice == "human":
        type = "human"
        strengthPoints = 5 + dice(3)
        healthPoints = 5 + dice(3)
        skillPoints = 5 + dice(3)
        armor = 5
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "2" or typeChoice == "elf":
        type = "elf"
        strengthPoints = 0 + dice(3)
        healthPoints = 0 + dice(3)
        skillPoints = 10 + dice(3)
        armor = 5
        statsPoints = dice(10)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "3" or typeChoice == "dwarf":
        type = "dwarf"
        strengthPoints = 10 + dice(3)
        healthPoints = 0 + dice(3)
        skillPoints = 0 + dice(3)
        armor = 15
        statsPoints = dice(7)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "4" or typeChoice == "orc":
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

    addStatsPoints(player, statsPoints, enemyLst)
    return player


def addStatsPoints(player, statsPoints, enemyLst):
    while True:
        if statsPoints < 1:
            menu(player, enemyLst)
        time.sleep(2)
        clear_screen()
        print(f"You have {statsPoints} points to add to your stats")
        print(
            f"What stats would you like to improve?\n1. STRENGTH:\t{getattr(player, 'strengthPoints')}\n2. HEALTH:\t{getattr(player, 'healthPoints')}\n3. SWORD SKILL:\t{getattr(player, 'skillPoints')}\n4. ARMOR:\t{getattr(player, 'armor')}\n"
        )
        if statsPoints > 0:
            selectAttribute = input(f"Choose attribute: ")

        if selectAttribute == "1":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
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
        leave()


def getEnemy(enemyLst, num):
    # enemyVals = SHEET.row_values(num)
    # enemyVals = readEnemyCSV()[num]
    enemyVals = enemyLst[num]
    type = enemyVals[0]
    name = enemyVals[1]
    strengthPoints = int(enemyVals[2])
    healthPoints = int(enemyVals[3])
    skillPoints = int(enemyVals[4])
    armor = int(enemyVals[5])
    enemy = CharacterStats(type, name, strengthPoints, healthPoints, skillPoints, armor)
    return enemy, enemyVals[3], num


def story(player, enemy):
    clear_screen()
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f"Set up with dialouge that leads to {player.name} the {player.type} and {enemy.name} the {enemy.type} drawing their weapons and comincing a swordbattle. Maximum length 70 words"
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\n\n{reply}")
    messages.append({"role": "assistant", "content": reply})
    startBattle = input(f"\nPress Enter to start the battle")


def main():
    # resetEnemyCSV(readEnemyCSV())
    # reset()
    configure()
    enemyLst = SHEET.get_all_values()[1:]
    clear_screen()
    print(
        "\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\nA RPG-adventure game powered by the story-telling of chat-gpt\n\t\t      Now enter the realm"
    )
    enter = input(f"\n\n\nPress ENTER to go to Menu: ")
    clear_screen()
    player = "Hero has not been created"
    time.sleep(1)

    menu(player, enemyLst)


main()
