"""Providing random number functions."""
import random
import os
import time
import gspread
import openai
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
    """
    Fetches the API KEY from the .env file
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def clear_screen():
    """
    Clears the screen, cover the commands for Windows "nt" with "cls" and clear for else
    """
    os.system("cls" if os.name == "nt" else "clear")


def game_title():
    """
    Prints the game title
    """
    print("\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")


def leave():
    """
    Input used to pause program before user is leaving function.
    Asking the user to interact with enter before leaving.
    """
    leave_input = input("\nMENU press Enter: ")
    clear_screen()


def read_enemy_csv():
    """
    Reads the google sheet file and storing it in the variable enemy_lst.
    enemy_lst variable is passed along during the game and only reset to restart
    the settings
    """
    enemy_lst = SHEET.get_all_values()[1:]
    return enemy_lst


def dice(num):
    """
    Simulates a six sided dice roll. The num parameter describes number of rolls
    being called
    """
    result = 0
    total = 0
    for _ in range(num):
        result = random.randint(1, 6)
        total += result
    return total


def battle_dice(num, total):
    """
    Simulates a six sided dice with the addition that all sixes generates two new
    rolls of dice. This function is only used in the sword_battle function to
    increase serendipity and allow higher uncertanty in the battles.
    """
    result = 0
    sixes = []
    for _ in range(num):
        result = random.randint(1, 6)
        total += result
        if result != 6:
            result += total
        else:
            sixes.append(result)
    if len(sixes) > 0:
        battle_dice(num, total)
    return total


def download(enemy_lst):
    """
    Updates the enemy_lst with new enemies. The addenemy_lst list is crosschecked against enemy_lst
    and duplicates are removed. The enemy_lst is added to the bottom of addenemy_lst and then
    redefined to equal the updated addenemy_lst before returned.
    """
    addenemy_lst = MOREENEMIES.get_all_values()[1:]

    list_num = 0
    for row in addenemy_lst:
        list_num += 1
        if row[1] in [sublist[1] for sublist in enemy_lst]:
            addenemy_lst.pop(list_num - 1)
    list_num = 0
    for row in enemy_lst:
        list_num += 1
        if row[1] not in [sublist[1] for sublist in addenemy_lst]:
            addenemy_lst.append(row)

    enemy_lst = addenemy_lst
    print(enemy_lst)
    return enemy_lst


def game_menu(player, enemy_lst):
    """
    Holds the Game Menu which allows user to choose activities
    """
    menu = {}
    menu["1."] = "Create New Hero"
    menu["2."] = "View Stats"
    menu["3."] = "Choose Opponent"
    menu["4."] = "View Wins"
    menu["5."] = "Download New Opponents"
    menu["6."] = "Reset Opponents To Start Settings"
    menu["7."] = "Quit Game"

    while True:
        clear_screen()
        game_title()
        print("GAME MENU:")
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        selection = input("Please select an option: ")
        if selection == "1":
            character_input(enemy_lst)
        elif selection == "2":
            clear_screen()
            game_title()
            print(player)
            leave()
        elif selection == "3":
            clear_screen()
            game_title()
            player, enemy_lst, num = opponents_lst(player, enemy_lst)
            enemy, num = get_enemy(enemy_lst, num)
            story(player, enemy)
            sword_battle(player, enemy_lst, enemy, num)
        elif selection == "4":
            clear_screen()
            game_title()
            print("")
            wins_lst(enemy_lst)
        elif selection == "5":
            enemy_lst = download(enemy_lst)
            print("New Opponents Successfully Downloaded")

        elif selection == "6":
            enemy_lst = read_enemy_csv()
        elif selection == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option selected. Please try again.")


def opponents_lst(player, enemy_lst):
    """
    Displays the undefeated enemies available for battle. zip is used to display the list
    in two columns.
    """
    while True:
        two_col_lst = []
        x_num = 1
        columns = 2
        for row in enemy_lst:
            if row[3] != 0:
                two_col_lst.append(f"{x_num}. {row[1].upper()}")
                x_num += 1

        for first, second in zip(two_col_lst[::columns], two_col_lst[1::columns]):
            print(f"{first: <13}\t\t{second: <13}")

        if player != "Hero has not been created":
            opponent = input("Please select an opponent or 'M' for back to menu: ")
            x_num = 0
            undef_opponent_lst = []
            for row in enemy_lst:
                if row[3] != 0:
                    undef_opponent_lst.append(row)
            if opponent.lower() == "m":
                game_menu(player, enemy_lst)
            try:
                if int(opponent) - 1 in range(len(undef_opponent_lst)):
                    for row in undef_opponent_lst:
                        x_num += 1
                        if int(opponent) == x_num:
                            num = int(opponent) - 1
                            return player, enemy_lst, num
            except ValueError:
                clear_screen()
                game_title()
                print(
                    f"Pick a number from the list or 'M' menu.\nYou entered '{opponent}'"
                )
            else:
                clear_screen()
                game_title()
                print(
                    f"Pick a number from the list or 'M' menu.\nYou entered '{opponent}'"
                )

        else:
            clear_screen()
            game_title()
            print("GAME MENU:")
            print("\nNo Hero Created. Please Go To Menu")
            leave()
            game_menu(player, enemy_lst)
            break


def wins_lst(enemy_lst):
    """
    Displays a list of the defeated enemies. Checks for health_points 0
    """
    lst_num = 1
    for row in enemy_lst:
        if row[3] == 0:
            print(f"{lst_num}. {row[1]}")
            lst_num += 1
        else:
            lst_num = 1
    leave()


def sword_battle(player, enemy_lst, enemy, num):
    """
    handles the battle logic between player and selected opponent.
    """
    total = 0
    clear_screen()
    print("\t\t⚔⚔⚔---Battle---⚔⚔⚔")
    while True:
        attack = (player.skill_points + battle_dice(6, total)) - (
            enemy.skill_points + battle_dice(6, total)
        )
        time.sleep(1)
        if attack == 0:
            print("The swords clash and no damage is dealt to either opponent")
            time.sleep(2)
        if attack > 0:
            damage = (player.strength_points + dice(1)) - round(
                enemy.armor + dice(1) + (enemy.skill_points / 2)
            )
            if damage < 1:
                damage = 1
            print(f"{player.name} strikes {enemy.name} who looses {damage} HP")
            enemy.health_points -= damage
            print(f"{enemy.name.upper()} now has {enemy.health_points} HP left")
            time.sleep(2)
            if enemy.health_points < 1:
                print(
                    f"{enemy.name.upper()} recieves a final blow. \n{player.name.upper()} lifts the sword in triumph"
                )
                battle_over = input(
                    f"The fight is over {enemy.name.upper()} is defeated. Press enter to continue the quest: "
                )
                time.sleep(1)
                dead = enemy_lst[num]
                dead[3] = 0
                enemy_lst.pop(num)
                enemy_lst.append(dead)
                stat_points = 3
                add_stat_points(player, stat_points, enemy_lst)
        if attack < 0:
            damage = (enemy.strength_points + dice(1)) - round(
                (player.armor + dice(1) + (player.skill_points / 2))
            )
            if damage < 1:
                damage = 1
            print(
                f"{enemy.name.upper()} strikes {player.name.upper()} who looses {damage} HP"
            )
            player.health_points -= damage
            print(f"{player.name.upper()} now has {player.health_points} HP left")
            if player.health_points < 1:
                print(
                    f"{player.name.upper()} recieves a final blow. \n{enemy.name.upper()} lifts sword in triumph"
                )
                battle_over = input("The fight is over. Press enter: ")
                clear_screen()
                print(
                    f"\n\n\t\t⚔⚔⚔---GAME OVER---⚔⚔⚔\n\n \n\n\t\t☩‌☩‌☩‌--{player.name.upper()}‌--☩‌☩‌☩"
                )
                leave()
                main()
                break


class CharacterStats:
    """
    Object collects the character and selected enemy stats. __str__ used to make
    the print of the object prettier.
    """

    def __init__(
        self, char_type, name, strength_points, health_points, skill_points, armor
    ):
        self.char_type = char_type
        self.name = name
        self.strength_points = strength_points
        self.health_points = health_points
        self.skill_points = skill_points
        self.armor = armor

    def __str__(self):
        return f"{self.name.upper()} THE MIGHTY {self.char_type.upper()}\nSTRENGTH:\t{self.strength_points}\nHEALTH:\t\t{self.health_points}\nSWORD SKILL:\t{self.skill_points}\nARMOR:\t\t{self.armor}"


def character_input(enemy_lst):
    """
    Handles the user input to create the player character. Automates unique
    stats for the types human/elf/dwarf/orc.
    """
    clear_screen()
    game_title()
    print("HERO")
    name = input("NAME: ")
    time.sleep(1)
    while True:
        type_choice = input("1. Human\n2. Elf\n3. Dwarf\n4. Orc\n\nTYPE: ").lower()
        time.sleep(1)
        clear_screen()
        if type_choice == "1" or type_choice == "human":
            char_type = "human"
            strength_points = 2 + dice(1)
            health_points = 3 + dice(2)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(2)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "2" or type_choice == "elf":
            char_type = "elf"
            strength_points = 2 + dice(1)
            health_points = 2 + dice(1)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(3)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "3" or type_choice == "dwarf":
            char_type = "dwarf"
            strength_points = 3 + dice(2)
            health_points = 3 + dice(1)
            skill_points = 2 + dice(1)
            armor = dice(1)
            stat_points = dice(1)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "4" or type_choice == "orc":
            char_type = "orc"
            strength_points = 2 + dice(2)
            health_points = 2 + dice(1)
            skill_points = dice(1)
            armor = 3
            stat_points = dice(2)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        else:
            print(
                f"Choices available are Human/Elf/Dwarf/Orc\nYou entered '{type_choice}'"
            )

    add_stat_points(player, stat_points, enemy_lst)
    return player


def add_stat_points(player, stat_points, enemy_lst):
    """
    The final stage of the character creation which let's the user place stat_points
    of their choice.
    """
    while True:
        clear_screen()
        game_title()
        if stat_points < 1:
            clear_screen()
            game_title()
            print(f"You have {stat_points} points to add to your stats")
            print(player)
            leave()
            game_menu(player, enemy_lst)
        print(f"You have {stat_points} points to add to your stats")
        print(
            f"What stats would you like to improve?\n1. STRENGTH:\t{getattr(player, 'strength_points')}\n2. HEALTH:\t{getattr(player, 'health_points')}\n3. SWORD SKILL:\t{getattr(player, 'skill_points')}\n4. ARMOR:\t{getattr(player, 'armor')}\n"
        )
        if stat_points > 0:
            select_attribute = input("Choose attribute: ")

        if select_attribute == "1":
            activate_stat_points = int(input("How many points do you wish to add: "))

            if activate_stat_points <= stat_points:
                player.strength_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "2":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.health_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "3":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.skill_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "4":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.armor += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered '{select_attribute}'")


def get_enemy(enemy_lst, num):
    """
    Creates an "enemy"-instance from CharacterStats object
    """
    enemy_vals = enemy_lst[num]
    char_type = enemy_vals[0]
    name = enemy_vals[1]
    strength_points = int(enemy_vals[2])
    health_points = int(enemy_vals[3])
    skill_points = int(enemy_vals[4])
    armor = int(enemy_vals[5])
    enemy = CharacterStats(
        char_type, name, strength_points, health_points, skill_points, armor
    )
    return enemy, num


def story(player, enemy):
    """
    Api call to chat-gpt asking it to reply to a string prepared with type and name.
    Length limit of the reply is included in the string
    """
    clear_screen()
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f"Set up with dialouge that leads to {player.name} the {player.char_type} and {enemy.name} the {enemy.char_type} drawing their weapons and comencing a sword_battle against eachother. Maximum length 70 words"
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    print(f"\t\t⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔\n\n{reply}")
    messages.append({"role": "assistant", "content": reply})
    start_battle = input("\nPress Enter to start the battle")


def main():
    """
    Controls calls for the api and game functions. Prints the "title-page"
    """
    configure()
    enemy_lst = SHEET.get_all_values()[1:]
    clear_screen()
    game_title()
    print(
        "A RPG-adventure game powered by the story-telling of chat-gpt\n\t\t      Now enter the realm"
    )
    leave()
    clear_screen()
    player = "Hero has not been created"
    time.sleep(1)

    game_menu(player, enemy_lst)


main()
