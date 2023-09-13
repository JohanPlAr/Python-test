import random, os, time, gspread, openai
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
MOREENEMIES = GSPREAD_CLIENT.open("reset").sheet1


def configure():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")


def gameTitle():
    print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")


def leave():
    leave = input(f"\nMENU press Enter: ")
    clearScreen()


def readEnemyCSV():
    enemyLst = SHEET.get_all_values()[1:]
    return enemyLst


def dice(num):
    result = 0
    total = 0
    for i in range(num):
        result = random.randint(1, 6)
        total += result
    return total


def battleDice(num, total):
    result = 0
    sixes = []
    for i in range(num):
        result = random.randint(1, 6)
        total += result
        if result != 6:
            result += total
        else:
            sixes.append(result)
    if len(sixes) > 0:
        battleDice(num, total)
    return total


def download(enemyLst):
    addEnemyLst = MOREENEMIES.get_all_values()[1:]

    x = 0
    for row in addEnemyLst:
        x += 1
        if row[1] in [sublist[1] for sublist in enemyLst]:
            addEnemyLst.pop(x - 1)
    x = 0
    for row in enemyLst:
        x += 1
        if row[1] not in [sublist[1] for sublist in addEnemyLst]:
            addEnemyLst.append(row)

    enemyLst = addEnemyLst
    print(enemyLst)
    return enemyLst


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
        clearScreen()
        gameTitle()
        print(f"GAME MENU:")
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please select an option: ")
        if selection == "1":
            characterInput(enemyLst)
        elif selection == "2":
            clearScreen()
            gameTitle()
            print(player)
            leave()
        elif selection == "3":
            clearScreen()
            gameTitle()
            player, enemyLst, num = opponentsLst(player, enemyLst)
            enemy, healthPoints, num = getEnemy(enemyLst, num)
            story(player, enemy)
            swordBattle(player, enemyLst, enemy, healthPoints, num)
        elif selection == "4":
            clearScreen()
            gameTitle()
            print("")
            winsLst(enemyLst)
        elif selection == "5":
            enemyLst = download(enemyLst)
            print("New Opponents Successfully Downloaded")

        elif selection == "6":
            enemyLst = readEnemyCSV()
        elif selection == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option selected. Please try again.")


def opponentsLst(player, enemyLst):
    while True:
        twoColLst = []
        x = 1
        columns = 2
        for row in enemyLst:
            if row[3] != 0:
                twoColLst.append(f"{x}. {row[1].upper()}")
                x += 1

        for first, second in zip(twoColLst[::columns], twoColLst[1::columns]):
            print(f"{first: <13}\t\t{second: <13}")

        if player != "Hero has not been created":
            opponent = input("Please select an opponent or 'M' for back to menu: ")
            x = 0
            undefOpponentLst = []
            for row in enemyLst:
                if row[3] != 0:
                    undefOpponentLst.append(row)
            if opponent.lower() == "m":
                menu(player, enemyLst)
            try:
                if int(opponent) - 1 in range(len(undefOpponentLst)):
                    for row in undefOpponentLst:
                        x += 1
                        if int(opponent) == x:
                            num = int(opponent) - 1
                            return player, enemyLst, num
                            break
            except:
                clearScreen()
                gameTitle()
                print(
                    f"Pick a number from the list or 'M' menu.\nYou entered '{opponent}'"
                )
            else:
                clearScreen()
                gameTitle()
                print(
                    f"Pick a number from the list or 'M' menu.\nYou entered '{opponent}'"
                )

        else:
            clearScreen()
            gameTitle()
            print(f"GAME MENU:")
            print(f"\nNo Hero Created. Please Go To Menu")
            leave()
            menu(player, enemyLst)
            break


def winsLst(enemyLst):
    x = 1
    for row in enemyLst:
        if row[3] == 0:
            print(f"{x}. {row[1]}")
            x += 1
        else:
            x = 1
    leave()


def swordBattle(player, enemyLst, enemy, healthPoints, num):
    total = 0
    clearScreen()
    print(f"\t\t⚔⚔⚔---Battle---⚔⚔⚔")
    while True:
        attack = (player.skillPoints + battleDice(6, total)) - (
            enemy.skillPoints + battleDice(6, total)
        )
        time.sleep(1)
        if attack == 0:
            print(f"The swords clash and no damage is dealt to either opponent")
            time.sleep(2)
        if attack > 0:
            damage = (player.strengthPoints + dice(1)) - round(
                enemy.armor + dice(1) + (enemy.skillPoints / 2)
            )
            if damage < 1:
                damage = 1
            print(f"{player.name} strikes {enemy.name} who looses {damage} HP")
            enemy.healthPoints -= damage
            print(f"{enemy.name.upper()} now has {enemy.healthPoints.upper()} HP left")
            time.sleep(2)
            if enemy.healthPoints < 1:
                print(
                    f"{enemy.name.upper()} recieves a final blow. \n{player.name.upper()} lifts the sword in triumph"
                )
                battlteOver = input(
                    f"The fight is over {enemy.name.upper()} is defeated. Press enter to continue the quest: "
                )
                time.sleep(1)
                dead = enemyLst[num]
                dead[3] = 0
                enemyLst.pop(num)
                enemyLst.append(dead)
                statsPoints = 3
                addStatsPoints(player, statsPoints, enemyLst)
        if attack < 0:
            damage = (enemy.strengthPoints + dice(1)) - round(
                (player.armor + dice(1) + (player.skillPoints / 2))
            )
            if damage < 1:
                damage = 1
            print(
                f"{enemy.name.upper()} strikes {player.name.upper()} who looses {damage} HP"
            )
            player.healthPoints -= damage
            print(
                f"{player.name.upper()} now has {player.healthPoints.upper()} HP left"
            )
            if player.healthPoints < 1:
                print(
                    f"{player.name.upper()} recieves a final blow. \n{enemy.name.upper()} lifts sword in triumph"
                )
                battlteOver = input("The fight is over. Press enter: ")
                clearScreen()
                print(
                    f"\n\n\t\t⚔⚔⚔---GAME OVER---⚔⚔⚔\n\n \n\n\t\t☩‌☩‌☩‌--{player.name.upper()}‌--☩‌☩‌☩"
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


def characterInput(enemyLst):
    clearScreen()
    gameTitle()
    print(f"HERO")
    name = input("NAME: ")
    time.sleep(1)
    typeChoice = input("1. Human\n2. Elf\n3. Dwarf\n4. Orc\n\nTYPE: ").lower()
    time.sleep(1)
    clearScreen()
    if typeChoice == "1" or typeChoice == "human":
        type = "human"
        strengthPoints = 2 + dice(1)
        healthPoints = 3 + dice(2)
        skillPoints = 4 + dice(1)
        armor = 0
        statsPoints = dice(2)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "2" or typeChoice == "elf":
        type = "elf"
        strengthPoints = 2 + dice(1)
        healthPoints = 2 + dice(1)
        skillPoints = 4 + dice(1)
        armor = 0
        statsPoints = dice(3)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "3" or typeChoice == "dwarf":
        type = "dwarf"
        strengthPoints = 3 + dice(2)
        healthPoints = 3 + dice(1)
        skillPoints = 2 + dice(1)
        armor = dice(1)
        statsPoints = dice(1)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    elif typeChoice == "4" or typeChoice == "orc":
        type = "orc"
        strengthPoints = 2 + dice(2)
        healthPoints = 2 + dice(1)
        skillPoints = dice(1)
        armor = 3
        statsPoints = dice(2)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    else:
        print(f"Choices available are Human/Elf/Dwarf/Orc\nYou entered '{name}'")

    addStatsPoints(player, statsPoints, enemyLst)
    return player


def addStatsPoints(player, statsPoints, enemyLst):
    while True:
        clearScreen()
        gameTitle()
        if statsPoints < 1:
            clearScreen()
            gameTitle()
            print(f"You have {statsPoints} points to add to your stats")
            print(player)
            leave()
            menu(player, enemyLst)
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
                addStatsPoints(player, statsPoints, enemyLst)
        elif selectAttribute == "2":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.healthPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints, enemyLst)
        elif selectAttribute == "3":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.skillPoints += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints, enemyLst)
        elif selectAttribute == "4":
            activateStatPoints = int(input(f"How many points do you wish to add: "))
            if activateStatPoints <= statsPoints:
                player.armor += activateStatPoints
                statsPoints -= activateStatPoints
            else:
                print(f"Not enough points left\nYou have {statsPoints} left")
                addStatsPoints(player, statsPoints, enemyLst)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered '{selectAttribute}'")


def getEnemy(enemyLst, num):
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
    clearScreen()
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f"Set up with dialouge that leads to {player.name} the {player.type} and {enemy.name} the {enemy.type} drawing their weapons and comencing a swordbattle against eachother. Maximum length 70 words"
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
    configure()
    enemyLst = SHEET.get_all_values()[1:]
    clearScreen()
    gameTitle()
    print(
        "A RPG-adventure game powered by the story-telling of chat-gpt\n\t\t      Now enter the realm"
    )
    leave()
    clearScreen()
    player = "Hero has not been created"
    time.sleep(1)

    menu(player, enemyLst)


main()
