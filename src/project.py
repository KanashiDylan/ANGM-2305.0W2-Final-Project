import random
import time
import sys
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

# --- Utility Functions (Typewriter-style printing) ---
def print_and_hyber(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_and_sleep(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_and_rise(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_and_wake(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# --- Player State ---
player = {
    "name": "Sora",
    "hp": 30,
    "mp": 10,
    "max_hp": 30,
    "max_mp": 10,
    "items": {"Potion": 2, "Ether": 1},
    "world": 1,
    "xp": 0,
    "level": 1,
    "miles": 0
}

# --- World Names and Colors ---
world_names = {
    1: ("Realm of Darkness", Fore.MAGENTA),
    2: ("Traverse Town", Fore.YELLOW),
    3: ("Hollow Bastion", Fore.LIGHTMAGENTA_EX)
}

# --- Enemy Data ---
enemies = {
    1: [{"name": "Shadow", "hp": 8, "atk": (2, 4)}],
    2: [{"name": "Soldier", "hp": 12, "atk": (3, 5)}],
    3: [{"name": "Large Body", "hp": 18, "atk": (4, 6)}]
}

# --- Restore Status ---
def restore_status():
    player["hp"] = player["max_hp"]
    player["mp"] = player["max_mp"]
    print_and_sleep(f"{Fore.GREEN}HP and {Fore.BLUE}MP fully restored!")

# --- Display Bars ---
def display_bars(name, hp, max_hp, mp=None, max_mp=None, is_enemy=False):
    bar_length = 15
    hp_ratio = max(0, min(hp/max_hp, 1))
    filled = int(bar_length * hp_ratio)
    empty = bar_length - filled
    hp_bar = "=" * filled + "-" * empty
    hp_color = Fore.GREEN if hp_ratio > 0.6 else Fore.YELLOW if hp_ratio > 0.3 else Fore.RED

    if mp is not None:
        mp_ratio = max(0, min(mp/max_mp,1))
        filled_mp = int(bar_length * mp_ratio)
        empty_mp = bar_length - filled_mp
        mp_bar = "=" * filled_mp + "-" * empty_mp
        mp_color = Fore.BLUE
    else:
        mp_bar = ""
        mp_color = ""

    if is_enemy:
        print(Fore.MAGENTA + f"{name}" + Style.RESET_ALL)
        print(f"{Fore.GREEN}HP [{hp_bar}] {hp}/{max_hp}{Style.RESET_ALL}")
    else:
        print(Fore.CYAN + f"{name}" + Style.RESET_ALL)
        print(f"{Fore.GREEN}HP [{hp_bar}] {hp}/{max_hp}{Style.RESET_ALL}")
        if mp is not None:
            print(f"{Fore.BLUE}MP [{mp_bar}] {mp}/{max_mp}{Style.RESET_ALL}")

# --- XP Bar Display ---
def display_xp_bar():
    bar_length = 20
    needed = player["level"] * 30
    ratio = player["xp"] / needed
    filled = int(bar_length * ratio)
    bar = "=" * filled + "-" * (bar_length-filled)
    print(Fore.GREEN + f"XP [{bar}] {player['xp']}/{needed}" + Style.RESET_ALL)

# --- Level Up ---
def level_check():
    while player["xp"] >= player["level"] * 30:
        player["level"] += 1
        player["max_hp"] += 5
        player["max_mp"] += 2
        restore_status()
        print_and_sleep(f"Level Up! Now Level {player['level']}!")

# --- Items ---
def use_item():
    print("Your items:", player["items"])
    item = input("Use which item? ").capitalize()
    if item in player["items"] and player["items"][item] > 0:
        if item == "Potion":
            player["hp"] = min(player["hp"] + 15, player["max_hp"])
            player["items"][item] -= 1
            print_and_sleep(f"{Fore.GREEN}Potion used! +15 HP{Style.RESET_ALL}")
        elif item == "Ether":
            player["mp"] = min(player["mp"] + 5, player["max_mp"])
            player["items"][item] -= 1
            print_and_sleep(f"{Fore.BLUE}Ether used! +5 MP{Style.RESET_ALL}")
    else:
        print_and_sleep("Can't use that.")

# --- Battle System ---
def battle():
    enemy = random.choice(enemies[player["world"]]).copy()
    e_hp = enemy["hp"]
    print_and_sleep(Fore.MAGENTA + f"A {enemy['name']} appears!" + Style.RESET_ALL)

    while player["hp"] > 0 and e_hp > 0:
        display_bars(player["name"], player["hp"], player["max_hp"], player["mp"], player["max_mp"])
        display_bars(enemy["name"], e_hp, enemy["hp"], is_enemy=True)
        print("1) Attack  2) Magic  3) Item  4) Run")
        choice = input("> ")

        if choice == "1":
            dmg = random.randint(3,6)
            e_hp -= dmg
            print_and_sleep(f"You strike fiercely! {Fore.RED}{dmg} DMG{Style.RESET_ALL}")
        elif choice == "2":
            magic_choice = input("Choose a spell: 1) Firaga 2) Thundaga 3) Blizzaga\n> ")
            if magic_choice == "1":
                dmg = random.randint(6,12)
                e_hp -= dmg
                print_and_sleep(Fore.RED + f"Firaga hits with {dmg} DMG!" + Style.RESET_ALL)
            elif magic_choice == "2":
                dmg = random.randint(6,12)
                e_hp -= dmg
                print_and_sleep(Fore.YELLOW + f"Thundaga hits with {dmg} DMG!" + Style.RESET_ALL)
            elif magic_choice == "3":
                dmg = random.randint(6,12)
                e_hp -= dmg
                print_and_sleep(Fore.BLUE + f"Blizzaga hits with {dmg} DMG!" + Style.RESET_ALL)
            else:
                print_and_sleep("Invalid magic!")
        elif choice == "3":
            use_item()
        elif choice == "4":
            print_and_sleep("You escape safely!")
            return
        else:
            print_and_sleep("Invalid choice!")

        if e_hp > 0:
            edmg = random.randint(*enemy["atk"])
            player["hp"] -= edmg
            print_and_sleep(f"{enemy['name']} strikes back! {Fore.RED}{edmg} DMG{Style.RESET_ALL}")

    if player["hp"] > 0:
        xp_gain = 10 * player["world"]
        player["xp"] += xp_gain
        drop = random.choice(["Potion", "Ether", "Elixir"])
        player["items"].setdefault(drop,0)
        player["items"][drop] += 1
        print_and_sleep(Fore.YELLOW + f"You have received {drop}!" + Style.RESET_ALL)
        display_xp_bar()
        level_check()
    else:
        print_and_sleep("You lost... Your heart fades.")
        restore_status()

# --- Actions ---
def travel():
    distance = random.randint(30, 60)
    player["miles"] += distance
    print_and_sleep(f"You travel forward... {distance} miles covered! Total miles: {player['miles']}")
    if random.random() < 0.3:
        battle()
    if player["miles"] >= player["world"] * 150 and player["world"] < 3:
        player["world"] += 1
        name, color = world_names[player["world"]]
        print_and_sleep(f"You have arrived at {color}{name}{Style.RESET_ALL}!")

def rest():
    restore_status()

def venture():
    print_and_sleep("You search the area...")
    found = random.choice(["Potion", "Ether", None])
    if found:
        player["items"].setdefault(found,0)
        player["items"][found] += 1
        color = Fore.GREEN if found=="Potion" else Fore.BLUE
        print_and_sleep(f"You found {color}{found}{Style.RESET_ALL}!")
    else:
        print_and_sleep("Nothing found...")
    if random.random() < 0.5:
        battle()

# --- Game Loop ---
def game_loop():
    print_and_sleep("Your heart is your guiding key...")
    while player["world"] <= 3 and player["hp"] > 0:
        name, color = world_names[player["world"]]
        print(f"\nCurrent World: {color}{name}{Style.RESET_ALL}")
        print("1) Travel  2) Rest  3) Venture")
        cmd = input("> ")
        if cmd == "1": travel()
        elif cmd == "2": rest()
        elif cmd == "3": venture()
        else: print_and_sleep("Invalid command!")

    if player["hp"] > 0:
        print_and_wake("You have reached the final destination... Victory!")
    else:
        print_and_wake("Game Over... Your heart fades.")

# --- Start Game ---
game_loop()
