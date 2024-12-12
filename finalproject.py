import os
import random
from colorama import Fore, Style, init
from IPython import get_ipython

# Initialize colorama
init(autoreset=True)

# Emojis for visualization
EMOJIS = {
    "player": "🚶",  # Player
    "monster": "👹",  # Monster
    "boss": "😈",
    "obstacle": "⬛",  # Obstacle
    "destination": "🏁",  # Destination
    "empty": "⬜",  # Empty space
    "heal": "❤️",  # Healing tile
    "power_up": "💪",  # Attack power-up tile
    "chance": "❓"  # Chance tile
}

def clear_console():
    """Clear the console"""
    get_ipython().magic('clear')

def print_map(game_map, player_pos):
    """Print the game map with emojis"""
    for i in range(len(game_map)):
        row = ""
        for j in range(len(game_map[i])):
            if (i, j) == player_pos:
                row += EMOJIS["player"] + " "  # Player's position
            elif game_map[i][j] == "X":
                row += EMOJIS["obstacle"] + " "  # Obstacle
            elif game_map[i][j] == "M":
                row += EMOJIS["monster"] + " "  # Monster
            elif game_map[i][j] == "B":
                row += EMOJIS["boss"] + " "  # Boss    
            elif game_map[i][j] == "D":
                row += EMOJIS["destination"] + " "  # Destination
            elif game_map[i][j] == "H":
                row += EMOJIS["heal"] + " "  # Healing tile
            elif game_map[i][j] == "P":
                row += EMOJIS["power_up"] + " "  # Attack power-up tile
            elif game_map[i][j] == "C":
                row += EMOJIS["chance"] + " "  # Chance tile
            else:
                row += EMOJIS["empty"] + " "  # Empty space
        print(row)

def move_player(player_pos, direction, game_map):
    """Move the player"""
    x, y = player_pos
    if direction == "w" and x > 0 and game_map[x - 1][y] != "X":
        x -= 1
    elif direction == "s" and x < len(game_map) - 1 and game_map[x + 1][y] != "X":
        x += 1
    elif direction == "a" and y > 0 and game_map[x][y - 1] != "X":
        y -= 1
    elif direction == "d" and y < len(game_map[0]) - 1 and game_map[x][y + 1] != "X":
        y += 1
    return (x, y)

def generate_map(m, n):
    """Generate a random game map"""
    game_map = [["." for _ in range(n)] for _ in range(m)]
    num_obstacles = (m * n) // 5  # Number of obstacles
    num_monsters = (m * n) // 15  # Number of monsters
    num_boss = 1
    num_healing_tiles = (m * n) // 20  # Number of healing tiles
    num_power_up_tiles = (m * n) // 25  # Number of attack power-up tiles
    num_chance_tiles = (m * n) // 30  # Number of chance tiles

    for _ in range(num_obstacles):
        x, y = random.randint(0, m - 2), random.randint(0, n - 2)
        game_map[x][y] = "X"  # Obstacle

    monster_positions = []
    for _ in range(num_monsters):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":  # Ensure not to overwrite obstacles
            game_map[x][y] = "M"  # Monster
            monster_positions.append((x, y))
    for _ in range(num_boss):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":
            game_map[x][y] = "B"  # boss
    for _ in range(num_healing_tiles):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":
            game_map[x][y] = "H"  # Healing tile

    for _ in range(num_power_up_tiles):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":
            game_map[x][y] = "P"  # Power-up tile

    for _ in range(num_chance_tiles):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":
            game_map[x][y] = "C"  # Chance tile

    return game_map, monster_positions

def handle_tile_effect(player, tile, game_map, player_pos):
    """Handle effects of landing on special tiles"""
    if tile == "H":  # Healing tile
        clear_console()
        heal_amount = random.randint(5, 10)
        player['hp'] = min(player['hp'] + heal_amount, player['max_hp'])
        print(f"You stepped on a healing tile and restored {heal_amount} HP!")

    elif tile == "P":  # Power-up tile
        clear_console()
        attack_increase = random.randint(1, 3)
        player['attack'] += attack_increase
        print(f"You stepped on a power-up tile and gained {attack_increase} attack power!")

    elif tile == "C":  # Chance tile
        clear_console()
        handle_chance_tile(player, game_map, player_pos)

def handle_chance_tile(player, game_map, player_pos):
    """Handle the random effects of a chance tile"""
    effects = [
        lambda: random_heal(player),
        lambda: halve_hp(player),
        lambda: increase_max_hp(player),
        lambda: spawn_monsters_around(player_pos, game_map, range_=1),
        lambda: spawn_monsters_around(player_pos, game_map, range_=2),
        lambda: teleport_player(player, game_map),
        lambda: increase_attack(player),
        lambda: decrease_attack(player),
        lambda: kill_all_monsters(game_map),
        lambda: spawn_boss_near_destination(game_map)
    ]
    effect = random.choice(effects)
    effect()

def random_heal(player):
    heal_amount = random.randint(5, 15)
    player['hp'] = min(player['hp'] + heal_amount, player['max_hp'])
    print(f"Chance tile effect: You healed {heal_amount} HP!")


def halve_hp(player):
    player['hp'] //= 2
    print("Chance tile effect: Your HP was halved!")


def increase_max_hp(player):
    increase = random.randint(1, 3)
    player['max_hp'] += increase
    player['hp'] += increase
    print(f"Chance tile effect: Your max HP increased by {increase}!")


def spawn_monsters_around(pos, game_map, range_=1):
    x, y = pos
    for i in range(x - range_, x + range_ + 1):
        for j in range(y - range_, y + range_ + 1):
            if 0 <= i < len(game_map) and 0 <= j < len(game_map[0]) and game_map[i][j] == ".":
                game_map[i][j] = "M"
    print(f"Chance tile effect: Monsters spawned around you in a range of {range_}!")


def teleport_player(player, game_map):
    empty_tiles = [(i, j) for i in range(len(game_map)) for j in range(len(game_map[0])) if game_map[i][j] == "."]
    if empty_tiles:
        new_pos = random.choice(empty_tiles)
        print(f"Chance tile effect: You were teleported to a new position: {new_pos}!")

        return new_pos

def increase_attack(player):
    increase = random.randint(2, 5)
    player['attack'] += increase
    print(f"Chance tile effect: Your attack increased by {increase}!")

def decrease_attack(player):
    decrease = random.randint(1, 3)
    player['attack'] = max(1, player['attack'] - decrease)
    print(f"Chance tile effect: Your attack decreased by {decrease}!")


def kill_all_monsters(game_map):
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[i][j] == "M":
                game_map[i][j] = "."
    print("Chance tile effect: All monsters on the map were killed!")


def spawn_boss_near_destination(game_map,range_=1):
    destinations = [(i, j) for i in range(len(game_map)) for j in range(len(game_map[0])) if game_map[i][j] == "D"]
    for dest in destinations:
        x,y = dest[0],dest[1]
        for i in range(x - range_, x + range_ + 1):
            for j in range(y - range_, y + range_ + 1):
                if 0 <= i < len(game_map) and 0 <= j < len(game_map[0]) and game_map[i][j] == ".":
                    game_map[i][j] = "B"
    print("Chance tile effect: Strong monsters spawned near the destination!")




def battle(player, monster):
    """Handle battle between player and monster"""
    print("A battle has started!")
    print(f"Player HP: {player['hp']} / {player['max_hp']}, Attack: {player['attack']}")
    print(Fore.RED + f"Monster HP: {monster['hp']}, Attack: {monster['attack']}")

    while player['hp'] > 0 and monster['hp'] > 0:
        # Both player and monster attack simultaneously
        monster['hp'] -= player['attack']
        player['hp'] -= monster['attack']

        # Display round results
        print(f"Player dealt {player['attack']} damage! Monster HP: {Fore.RED + str(max(0, monster['hp']))}")
        print(f"Monster dealt {monster['attack']} damage! Player HP: {max(0,player['hp'])} / {player['max_hp']}")
        # Check if the player is defeated
        
        if player['hp'] <= 0:
            print("Oh no!!")
            print("You were defeated by the monster!")
            return None  # Player dies
        # Check if the monster is defeated
        if monster['hp'] <= 0:
            print("Congratulation!!")
            print("You defeated the monster!")
            return player  # Player survives with remaining HP

    return player

def game_loop(m, n):
    """Main game loop"""
    game_map, monster_positions = generate_map(m, n)
    player_pos = (0, 0)  # Player starting position
    destination = (m - 1, n - 1)  # Destination position
    game_map[m - 1][n - 1] = "D"  # Mark the destination

    # Initialize player stats
    player = {"hp": 20, "max_hp": 20, "attack": 5}
    boss = {"hp": 30, "attack": 8}

    # Create monster stats
    monsters = {pos: {"hp": random.randint(5, 15), "attack": random.randint(2, 6)} for pos in monster_positions}

    while player_pos != destination:
        print_map(game_map, player_pos)
        print(f"Player HP: {player['hp']} / {player['max_hp']}, Attack: {player['attack']}")
        print("Use W/A/S/D to move. Enter 'q' to quit.")
        move = input("Your move: ").lower()

        if move == "q":
            print("Game over! You quit the game.")
            break
        
        # Move player and get new position
        new_pos = move_player(player_pos, move, game_map)
        player_pos = new_pos
        
        if game_map[player_pos[0]][player_pos[1]] == ".":
            clear_console()

        # Check the type of tile the player landed on
        current_tile = game_map[player_pos[0]][player_pos[1]]

        if current_tile in ["H", "P", "C"]:
            handle_tile_effect(player, current_tile, game_map, player_pos)
            game_map[player_pos[0]][player_pos[1]] = "."

        # Check if player encounters a monster
        if current_tile == "M":
            new_monster = {"hp": random.randint(5, 15), "attack": random.randint(2, 6)}
            player = battle(player, new_monster)
            if player is None:
                print("Game over! You lost the battle.")
                break
            else:
                # Remove defeated monster from the map
                del monsters[player_pos]
                game_map[player_pos[0]][player_pos[1]] = "."
        if current_tile == "B":
            player = battle(player, boss)
            if player is None:
                print("Game over! You lost the battle.")
                break
            else:
                # Remove defeated monster from the map
                del monsters[player_pos]
                game_map[player_pos[0]][player_pos[1]] = "."
        if player_pos in monsters:
            monster = monsters[player_pos]
            player = battle(player, monster)
            if player is None:
                print("Game over! You lost the battle.")
                break
            else:
                # Remove defeated monster from the map
                del monsters[player_pos]
                game_map[player_pos[0]][player_pos[1]] = "."

    if player_pos == destination and player is not None:
        print("Congratulations! You reached the destination!")

# Start the game
game_loop(10, 10)
