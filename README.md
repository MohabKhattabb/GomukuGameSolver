# Gomoku Game Solver

This project implements a Gomoku game solver with both human vs. AI and AI vs. AI modes. The AI utilizes the Minimax algorithm for decision-making, enhanced with Alpha-Beta pruning for optimization. The game engine manages the game state, user interactions, and the flow of the game.

## Features

- **Human vs. AI Mode**: Play against an AI opponent that uses the Minimax algorithm to determine its moves.
- **AI vs. AI Mode**: Watch two AI players compete against each other using Alpha-Beta pruning for efficient decision-making.
- **Game Engine**: A robust engine that manages the game state, validates moves, and checks for win conditions.
- **User Interface**: A console-based UI that allows for easy interaction and display of the game board.

## Project Structure

```
gomoku-game-solver/
├── src/
│   ├── main.py                # Entry point of the application
│   ├── game/                  # Game-related modules
│   ├── ai/                    # AI-related modules
│   ├── ui/                    # User interface modules
│   └── utils/                 # Utility modules
├── tests/                     # Unit tests for the project
├── .gitignore                 # Files to ignore in version control
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gomoku-game-solver
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python src/main.py
   ```

## Usage

- Follow the prompts in the console to play the game.
- Choose between playing against the AI or watching two AIs compete.

## Algorithms

- **Minimax Algorithm**: A decision-making algorithm used for minimizing the possible loss in a worst-case scenario.
- **Alpha-Beta Pruning**: An optimization technique for the Minimax algorithm that reduces the number of nodes evaluated in the search tree.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.