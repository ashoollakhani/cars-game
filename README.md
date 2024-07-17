# Cars Game 🚗

We were assigned to create a Pygame implementation of the Car Racing game mainly using an object-oriented programming approach. We chose to develop a "Cars" movie-themed racing game. 🎥

---

## "Cars" Racing Game 🏁

The game is a **Cars** themed racing game, where the player controls Lightning McQueen on a racing track. The goal of the game is to race against a stream of other cars without crashing for as long as possible, accumulating points from the time played. The game contains different kinds of power ups that the player can get by driving into them. The game contains a special game mode where the player is able to shoot other cars. In the special game mode, there are no power ups but there are bombs on the track that end the game if the player crashes into them. The game can also be played in multiplayer, where two players choose their cars' colors and race on the same track. In multiplayer, the player that doesn't crash wins the race. 🚦🏆

---

## Installation Instructions 🛠️

- Open the files in PyCharm.
- Run `main.py`.
- The game opens and you can explore the different features and play!

---

## Project Structure 📁

The project has seven code files which are named `car`, `game`, `gamemode`, `interface`, `main`, `multiplayer`, and `powerups`. In addition, there are two files storing the images and the sounds used in the game. 🎨🔊

- The `car` file is used to create the `Car` class, which is used to create cars in the other files.
- The `game` file takes care of the game itself, allowing the player to move their car and enabling the spawning of enemy cars and power ups.
- The `gamemode` file does the same for the special game mode, making sure the player can shoot at the incoming cars and bombs appearing on the road.
- `Interface` is used to display the other screens in the game like settings, credits, info, how to play, game, select difficulty, and select game mode screen.
- The `multiplayer` file has the functionalities for the multiplayer game. It ensures that the two cars' colors can be chosen in the beginning, the cars can't go through each other and at the end of a race there is a winner.
- Power ups are defined in the `powerup` file.
- Lastly, the `main` file is used for running the game.

---
