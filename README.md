# Othello

The game consists of a square board (N x N). This is the  total area in the board.
The game is played between two players (one or both them can be the machine). The objective of the game is
to acquire maximum positions in the board from an initial position in which both
players own two positions each.

The players are distinguished as black or white color.

The game rules dictate that if a player owns two positions that are in a straight line along the horizontal,
vertical or diagonal axes, the player must also own (and hence acquires) the positions in between (which are
owned by the other player).

## Module Overview

1. ./src/game_zone.py: It provides a simple graphical user interface to visualize the bidding process.

2. ./src/manager.py: represents the behaviour of the landlord who manages the entire process.

3. ./src/utilities.py: contains useful functions that can be used by the AI agents and/or the manager.

4. ./src/randy_ai.py: An agent that plays a random turn out of all available moves.

5. ./src/agent.py: A sample agent that uses classic AI algorithms (minmax, alpha beta pruning etc) to beat the the opponents.
You are welcome to write as many new agents as independent files and contribute.

## Playing the game

To run the code, you can either run two separate agents against each other using:

```bash
        python3 game_zone.py -d N -a <agent1> -b <agent2>
```

or you can run one agent against an interactive user:

```bash
        python3 game_zone.py -d N -a <agent1>
```

In both cases, N denotes the board size. Optionally, you can also specify three flags:

* -l <limit>, where <limit> is an integer representing the depth limit

* -c, which enables caching

* -o which enables optimal node ordering for α/β-pruning
