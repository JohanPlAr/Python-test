import random, pprint, os, time


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu(player):
    print("Choose your next opponent")


def swordBattle(player, enemy):
    clear_screen()
    while True:
        print(f"\t\t⚔⚔⚔Battle⚔⚔⚔")
        attack = (player.skillPoints + dice(6)) - (enemy.skillPoints + dice(6))

        if attack == 0:
            print(f"The swords clash and no damage is dealt to either opponent")
        if attack > 0:
            damage = attack + player.strengthPoints - player.armor
            print(f"{player.name} strikes {enemy.name} who looses {damage} HEALTH")
            enemy.healthPoints -= damage
            if enemy.healthPoints < 1:
                print(
                    f"{enemy.name.upper()} recieves a deadly blow. \n{player.name.upper()} lifts sword in triumph"
                )
                menu(player)
        if attack < 0:
            damage = abs(attack) + enemy.strengthPoints - player.armor
            print(
                f"{player.name.upper()} strikes {enemy.name.upper()} who looses {damage} HEALTH"
            )
            enemy.healthPoints -= damage
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
    type = input("Choose your characters type\nHuman/Elf/Dwarf/Orc\n").lower()
    time.sleep(1)
    clear_screen()
    if type == "human":
        strengthPoints = 15 + dice(6)
        healthPoints = 15 + dice(6)
        skillPoints = 15 + dice(6)
        armor = 5
        statsPoints = dice(10)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if type == "elf":
        strengthPoints = 15 + dice(6)
        healthPoints = 15 + dice(6)
        skillPoints = 15 + dice(6)
        armor = 5
        statsPoints = dice(9)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if type == "dwarf":
        strengthPoints = 15 + dice(6)
        healthPoints = 15 + dice(6)
        skillPoints = 15 + dice(6)
        armor = 5
        statsPoints = dice(10)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    if type == "orc":
        strengthPoints = 15 + dice(6)
        healthPoints = 15 + dice(6)
        skillPoints = 15 + dice(6)
        armor = 5
        statsPoints = dice(10)
        player = CharacterStats(
            type, name, strengthPoints, healthPoints, skillPoints, armor
        )
    else:
        print(f"Choices available are Human/Elf/Dwarf/Orc\nYou wrote {name}")

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
            type = "orc"
            name = "orgul"
            strengthPoints = 40
            healthPoints = 26
            skillPoints = 25
            armor = 2
            enemy = CharacterStats(
                type, name, strengthPoints, healthPoints, skillPoints, armor
            )
            swordBattle(player, enemy)
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


def main():
    clear_screen()
    characterInput()


main()
