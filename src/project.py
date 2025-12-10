import random
import time
import sys
from colorama import Fore, Style, init

# --- Colorama Setup ---
init(autoreset=True, convert=True)

# --- Safe Color Helpers ---
def ctext(color, text):
    return f"{color}{text}{Style.RESET_ALL}"

def cprint(color, text):
    print(ctext(color, text))

# --- Typewriter Printing ---
def type_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def sleep_print(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- Player Data ---
player = {
    "name": "Sora",
    "hp": 30,
    "max_hp": 30,
    "mp": 10,
    "max_mp": 10,
    "xp": 0,
    "level": 1,
    "miles": 0,
    "world": 1,
    "items": ["Potion", "Ether", "Elixir"],
}

# --- World List w/ Colors ---
world_names = {
    1: ("Realm of Darkness", Fore.MAGENTA),
    2: ("Traverse Town", Fore.YELLOW),
    3: ("Hollow Bastion", Fore.LIGHTMAGENTA_EX),
}

# --- Enemy Data ---
enemies = [
    {"name": "Shadow", "hp": 8, "max_hp": 8, "dmg": (2, 4)},
    {"name": "Soldier", "hp": 12, "max_hp": 12, "dmg": (2, 5)},
    {"name": "Large Body", "hp": 20, "max_hp": 20, "dmg": (3, 6)},
]

# --- Bars ---
def bar(current, max_value, width=15):
    filled = int((current / max_value) * width)
    empty = width - filled
    return f"[{'=' * filled}{'-' * empty}]"

# --- Display Player Stats ---
def show_stats(enemy=None):
    # Player
    print(ctext(Fore.CYAN, player["name"]))
    hp_color = Fore.GREEN if player["hp"] > player["max_hp"] * 0.5 else Fore.YELLOW if player["hp"] > player["max_hp"] * 0.25 else Fore.RED
    print(f"{ctext(Fore.GREEN, 'HP')} {ctext(hp_color, bar(player['hp'], player['max_hp']))} {player['hp']}/{player['max_hp']}")
    print(f"{ctext(Fore.BLUE, 'MP')} {ctext(Fore.BLUE, bar(player['mp'], player['max_mp']))} {player['mp']}/{player['max_mp']}")

    # Enemy
    if enemy:
        print(ctext(Fore.RED, enemy["name"]))
        enemy_color = Fore.GREEN if enemy["hp"] > enemy["max_hp"] * 0.5 else Fore.YELLOW if enemy["hp"] > enemy["max_hp"] * 0.25 else Fore.RED
        print(f"HP {ctext(enemy_color, bar(enemy['hp'], enemy['max_hp']))} {enemy['hp']}/{enemy['max_hp']}")
    print()

# --- Level Up ---
def gain_xp(amount):
    player["xp"] += amount
    required = player["level"] * 30
    if player["xp"] >= required:
        player["xp"] -= required
        player["level"] += 1
        type_print(ctext(Fore.GREEN, f"Level Up! You are now level {player['level']}"))
        # Heal on level up
        player["max_hp"] += 5
        player["max_mp"] += 2
        player["hp"] = player["max_hp"]
        player["mp"] = player["max_mp"]

# --- Rewards ---
def give_reward():
    item = random.choice(["Potion", "Ether", "Elixir"])
    cprint(Fore.YELLOW, f"You received: {item}!")
    if item == "Potion":
        player["items"].append(item)
    elif item == "Ether":
        player["items"].append(item)
    elif item == "Elixir":
        player["items"].append(item)

# --- Magic Damage ---
def magic_spell():
    print("Choose a spell:")
    print(ctext(Fore.RED, "1) Firaga"))
    print(ctext(Fore.YELLOW, "2) Thundaga"))
    print(ctext(Fore.BLUE, "3) Blizzaga"))
    choice = input("> ")
    if choice == "1":
        return "Firaga", Fore.RED, random.randint(6, 12)
    if choice == "2":
        return "Thundaga", Fore.YELLOW, random.randint(7, 13)
    if choice == "3":
        return "Blizzaga", Fore.BLUE, random.randint(5, 11)
    return None, None, 0

# --- Battle System ---
def battle():
    enemy = random.choice(enemies)
    enemy = {**enemy}  # local copy
    type_print(ctext(Fore.MAGENTA, f"A {enemy['name']} appears!"))

    while enemy["hp"] > 0 and player["hp"] > 0:
        show_stats(enemy)
        print("1) Attack  2) Magic  3) Item  4) Run")
        cmd = input("> ")

        # --- Attack ---
        if cmd == "1":
            dmg = random.randint(3, 6)
            enemy["hp"] = max(enemy["hp"] - dmg, 0)
            type_print(f"You strike fiercely! {ctext(Fore.RED, str(dmg)+' DMG')}")
        # --- Magic ---
        elif cmd == "2":
            if player["mp"] < 3:
                type_print("Not enough MP!")
                continue
            spell, color, dmg = magic_spell()
            if not spell:
                continue
            player["mp"] -= 3
            enemy["hp"] = max(enemy["hp"] - dmg, 0)
            type_print(ctext(color, f"{spell} hits for {dmg} DMG!"))
        # --- Item ---
        elif cmd == "3":
            if not player["items"]:
                type_print("No items!")
                continue
            print("Choose item:")
            for i, it in enumerate(player["items"]):
                print(f"{i+1}) {it}")
            idx = int(input("> ")) - 1
            item = player["items"].pop(idx)
            if item == "Potion":
                player["hp"] = min(player["hp"] + 25, player["max_hp"])
            elif item == "Ether":
                player["mp"] = min(player["mp"] + 10, player["max_mp"])
            elif item == "Elixir":
                player["hp"] = min(player["hp"] + 20, player["max_hp"])
                player["mp"] = min(player["mp"] + 20, player["max_mp"])
            type_print(ctext(Fore.GREEN, f"{item} used!"))
        # --- Run ---
        elif cmd == "4":
            type_print("You escape!")
            return
        else:
            continue

        # enemy turn
        if enemy["hp"] > 0:
            dmg = random.randint(*enemy["dmg"])
            player["hp"] = max(player["hp"] - dmg, 0)
            type_print(f"{enemy['name']} strikes back! {ctext(Fore.RED, str(dmg)+' DMG')}")

    if player["hp"] > 0:
        type_print(ctext(Fore.GREEN, f"You defeated {enemy['name']}!"))
        gain_xp(15)
        give_reward()

# --- Travel ---

def get_world():
    name, color = world_names[player["world"]]
    return ctext(color, name)

def travel():
    distance = random.randint(30, 60)
    player["miles"] += distance
    type_print(f"You travel: {distance} miles (Total: {player['miles']})")
    if random.random() < 0.3:
        battle()
    if player["miles"] >= player["world"] * 150 and player["world"] < 3:
        player["world"] += 1
        type_print(f"You have arrived at {get_world()}!")

# --- Rest ---
def rest():
    player["hp"] = player["max_hp"]
    player["mp"] = player["max_mp"]
    type_print("You rest and recover...")

# --- Venture ---
def venture():
    type_print("You explore the area...")
    if random.random() < 0.4:
        give_reward()
    else:
        type_print("Nothing found...")

# --- Game Loop ---
def game_loop():
    type_print("Your heart is your guiding key...")
    while player["world"] <= 3 and player["hp"] > 0:
        print()
        print(f"Current World: {get_world()}")
        print("1) Travel  2) Rest  3) Venture")
        cmd = input("> ")
        if cmd == "1": travel()
        elif cmd == "2": rest()
        elif cmd == "3": venture()
        else: type_print("Invalid option.")

    if player["hp"] > 0:
        type_print("You reach the final world... Victory!")
    else:
        type_print("Your heart fades...")

game_loop()

