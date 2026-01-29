# DuckTales Maze

DuckTales Maze es un juego de laberinto inspirado en el clásico de Amiga "DuckTales: The Quest for Gold". El jugador, encarnando a un intrépido explorador, debe navegar por un sistema de cuevas generado proceduralmente, recolectar gemas y encontrar el tesoro antes de que la antorcha se apague. Pero cuidado, una momia ancestral patrulla el laberinto, y caer en un agujero oculto significa el fin de la aventura.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

En DuckTales Maze, el jugador explora un laberinto de 8x8 celdas. El objetivo principal es encontrar el tesoro oculto. Sin embargo, el tiempo es limitado por la duración de tu antorcha, y una momia errante te persigue si te acercas demasiado. El laberinto está lleno de trampas, como agujeros invisibles, aunque las celdas adyacentes con lodo te darán una pista del peligro. Recoge gemas para aumentar tu puntuación y demuestra tu habilidad para escapar de las profundidades de la cueva.

## Características

-   **Laberinto Dinámico**: Tablero de 8x8 celdas con paredes generadas proceduralmente, haciendo cada partida única.
-   **Momia Enemiga**: Una momia con inteligencia artificial que patrulla el laberinto y te persigue si entras en su rango de visión, ajustando su velocidad según su estado.
-   **Agujeros Ocultos**: Trampas mortales invisibles, señalizadas por celdas adyacentes con lodo.
-   **Antorcha Limitada**: Un temporizador de antorcha que añade una capa de urgencia; si se apaga, pierdes.
-   **Gemas y Puntuación**: Recolecta gemas (50$ cada una) dispersas por el laberinto para aumentar tu marcador.
-   **Tesoro Final**: Encuentra el tesoro para ganar la partida.
-   **Interfaz Gráfica Retro**: Utiliza Pygame para una interfaz visual que evoca la estética de los juegos clásicos, con celdas separadas por un "gap" y pasajes marcados.
-   **Condiciones de Derrota**: Pierdes si la momia te atrapa, caes en un agujero o tu antorcha se apaga.

## Requisitos

-   Python 3.x (se recomienda Python 3.11 o 3.12 para evitar problemas de instalación de Pygame)
-   Pygame

## Instalación

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/fransolerc/duckTales-maze.git
    ```

2.  Navega al directorio del proyecto:

    ```bash
    cd duckTales-maze
    ```

3.  Instala las dependencias:

    ```bash
    pip install pygame
    ```

## Uso

1.  Ejecuta el juego:

    ```bash
    python main.py
    ```

2.  Usa las teclas de dirección (`UP`, `DOWN`, `LEFT`, `RIGHT`) para mover a tu personaje a través del laberinto.
3.  **Objetivo**: Encuentra el tesoro antes de que la antorcha se apague, evitando a la momia y los agujeros ocultos.
4.  **Pistas**: Observa las celdas con lodo; indican la proximidad de un agujero.

## Estructura del Proyecto

-   `main.py`: Archivo principal que inicia el juego, maneja el bucle de eventos, el temporizador de la antorcha y la visualización de la puntuación.
-   `modules/gameMap.py`: Define la clase `GameMap` que gestiona la generación del laberinto (paredes, agujeros, lodo), la colocación de elementos, el dibujado del mapa y las condiciones de victoria/derrota.
-   `modules/cell.py`: Define la clase `Cell` que representa una celda individual del laberinto, incluyendo sus propiedades (tesoro, agujero, lodo, paredes, visitado).
-   `modules/player.py`: Define la clase `Player` que maneja la posición y puntuación del jugador, así como su lógica de movimiento.
-   `modules/mummy.py`: Define la clase `Mummy` que gestiona la posición de la momia y su inteligencia artificial (patrulla/persecución).
-   `modules/config.py`: Archivo de configuración que contiene parámetros como el tamaño de las celdas, márgenes y la paleta de colores del juego.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un `issue` o envía un `pull request` si deseas mejorar el proyecto.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT].
