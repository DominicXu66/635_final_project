#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 05:36:34 2024

@author: xuduoyifu
"""
import os
import random

def clear_console():
        print("\n" * 100)

def print_map(game_map, player_pos):
    """Print the game map"""
    clear_console()  # Clear screen before printing
    for i in range(len(game_map)):
        row = ""
        for j in range(len(game_map[i])):
            if (i, j) == player_pos:
                row += "P "  # Player's position
            else:
                row += game_map[i][j] + " "
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
    num_monsters = (m * n) // 10  # Number of monsters

    for _ in range(num_obstacles):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        game_map[x][y] = "X"  # Obstacle

    for _ in range(num_monsters):
        x, y = random.randint(0, m - 1), random.randint(0, n - 1)
        if game_map[x][y] == ".":  # Ensure not to overwrite obstacles
            game_map[x][y] = "M"  # Monster

    return game_map

def game_loop(m, n):
    """Main game loop"""
    game_map = generate_map(m, n)
    player_pos = (0, 0)  # Player starting position
    destination = (m - 1, n - 1)  # Destination position
    game_map[m - 1][n - 1] = "D"  # Mark the destination

    while player_pos != destination:
        print_map(game_map, player_pos)  # Print the updated map
        print("Use W/A/S/D to move. Enter 'q' to quit.")
        move = input("Your move: ").lower()

        if move == "q":
            print("Game over! You quit the game.")
            break

        player_pos = move_player(player_pos, move, game_map)

        if game_map[player_pos[0]][player_pos[1]] == "M":
            clear_console()
            print("You were eaten by a monster! Game over!")
            break

    if player_pos == destination:
        clear_console()
        print("Congratulations! You reached the destination!")

# Start the game
game_loop(10, 10)
