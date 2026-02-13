# DuckTales Maze

DuckTales Maze is a maze game inspired by the Amiga classic "DuckTales: The Quest for Gold". The player, embodying an intrepid explorer, must navigate a procedurally generated cave system, collect gems, and find the treasure before the torch goes out. But beware, an ancient mummy patrols the maze, and falling into a hidden hole means the end of the adventure.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributions](#contributions)
- [License](#license)

## Description

In DuckTales Maze, the player explores an 8x8 cell maze. The main objective is to find the hidden treasure. However, time is limited by the duration of your torch, and a wandering mummy chases you if you get too close. The maze is full of traps, such as invisible holes, although adjacent cells with mud will give you a hint of the danger. Collect gems to increase your score and prove your skill in escaping the depths of the cave.

## Features

-   **Dynamic Maze**: 8x8 cell board with procedurally generated walls, making every game unique.
-   **Enemy Mummy**: An AI-controlled mummy that patrols the maze and chases you if you enter its line of sight, adjusting its speed based on its state.
-   **Hidden Holes**: Invisible deadly traps, signaled by adjacent cells with mud.
-   **Limited Torch**: A torch timer that adds a layer of urgency; if it goes out, you lose.
-   **Gems and Scoring**: Collect gems ($50 each) scattered throughout the maze to increase your score.
-   **Final Treasure**: Find the treasure to win the game.
-   **Retro GUI**: Uses Pygame for a visual interface that evokes the aesthetic of classic games, with cells separated by a "gap" and marked passages.
-   **Defeat Conditions**: You lose if the mummy catches you, you fall into a hole, or your torch goes out.

## Requirements

-   Python 3.x (Python 3.11 or 3.12 is recommended to avoid Pygame installation issues)
-   Pygame

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/fransolerc/duckTales-maze.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd duckTales-maze
    ```

3.  Install dependencies:

    ```bash
    pip install pygame
    ```

## Usage

1.  Run the game:

    ```bash
    python main.py
    ```

2.  Use the arrow keys (`UP`, `DOWN`, `LEFT`, `RIGHT`) to move your character through the maze.
3.  **Objective**: Find the treasure before the torch goes out, avoiding the mummy and hidden holes.
4.  **Hints**: Observe cells with mud; they indicate the proximity of a hole.

## Project Structure

-   `main.py`: Main file that starts the game, handles the event loop, torch timer, and score display.
-   `modules/gameMap.py`: Defines the `GameMap` class that manages maze generation (walls, holes, mud), item placement, map drawing, and win/loss conditions.
-   `modules/cell.py`: Defines the `Cell` class representing an individual maze cell, including its properties (treasure, hole, mud, walls, visited).
-   `modules/player.py`: Defines the `Player` class handling player position, score, and movement logic.
-   `modules/mummy.py`: Defines the `Mummy` class managing the mummy's position and AI (patrol/chase).
-   `modules/config.py`: Configuration file containing parameters such as cell size, margins, and the game color palette.

## Contributions

Contributions are welcome. Please open an `issue` or submit a `pull request` if you wish to improve the project.

## License

This project is licensed under the [MIT License].