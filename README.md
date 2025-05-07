# Advanced Stickman Trivia Game

## Authors

* Sumit Shrestha
* James Kim

## Project Overview

Advanced Stickman Trivia is an engaging and educational game application that combines trivia questions with an interactive user interface. Users can test their knowledge across various categories like History, Science, Movies, and Geography. The game features a welcoming animated main screen and a dedicated game screen for trivia gameplay, including a virtual keyboard for input and a scoring system.

This project was developed as a final project for CS122.

## Features

* **Animated Main Menu:**
    * Visually appealing sky-blue background with animated clouds rising and stickmen falling.
    * Interactive "Play" and "Exit" buttons with hover effects.
* **Trivia Gameplay:**
    * Selection from four trivia categories: History, Science, Movies, and Geography.
    * Questions are loaded from dedicated text files for each category.
    * Users input their answers using an on-screen virtual keyboard.
    * Three attempts are given to answer each question correctly.
* **User Interface:**
    * "How to Play" button providing instructions.
    * "Select Topic" dropdown menu for choosing trivia categories.
    * Clear display for questions and user input.
    * Score tracking visible to the user.
    * Customizable background image for the game screen.
* **Error Handling:**
    * Provides feedback for invalid inputs (e.g., submitting an empty answer).
    * Handles missing question files gracefully.

## File Structure
.
├── ui.py                   # Main application entry point, handles the initial animated UI screen
├── game_screen.py          # Manages the main gameplay screen, UI elements, and interactions
├── trivia_hangman.py       # Contains the core backend logic for trivia, question loading, and answer checking
├── history.txt             # Trivia questions for the History category
├── science.txt             # Trivia questions for the Science category
├── movies.txt              # Trivia questions for the Movies category
├── geography.txt           # Trivia questions for the Geography category
├── background.jpg          # Background image for the game screen
└── README.md               # This readme file

## Requirements

* Python 3.x
* Pillow (PIL Fork) library (`pip install Pillow`)
* Tkinter (usually included with standard Python installations)

## How to Run

1.  **Ensure all files are in the same directory:**
    * `ui.py`
    * `game_screen.py`
    * `trivia_hangman.py`
    * `history.txt`
    * `science.txt`
    * `movies.txt`
    * `geography.txt`
    * `background.jpg` (Note: The `game_screen.py` currently looks for `background.jpeg`. Ensure the filename matches or update the code.)
2.  **Install dependencies:**
    ```bash
    pip install Pillow
    ```
3.  **Run the main UI file from your terminal:**
    ```bash
    python ui.py
    ```

## Gameplay Instructions

1.  The game starts with an animated main menu. Click "Play" to begin or "Exit" to close.
2.  On the game screen, click "Select Topic" to choose a category (History, Science, Movies, or Geography).
3.  A question from the selected topic will appear.
4.  Use the on-screen virtual keyboard to type your answer into the input field.
5.  Click "Submit" to check your answer.
6.  You have 3 tries to guess the answer correctly.
7.  If you guess correctly, your score increases, and you can select a new topic for another question.
8.  If you run out of tries, the game will show the correct answer and your final score. The game then resets for you to play again.
9.  Click "How To Play" at any time for a reminder of the rules.

## Code Structure Overview

* **`ui.py` (Main Menu & Animations):**
    * `HangmanGame` class: Initializes the main Tkinter window, canvas, and animated elements.
    * `Cloud` class: Defines the behavior and appearance of animated clouds.
    * `Diver` class: Defines the behavior and appearance of animated stickmen (referred to as divers in the code).
    * Handles navigation to the game screen (`GameScreen`).
* **`game_screen.py` (Gameplay Screen):**
    * `GameScreen` class: Sets up the game interface, including the background image, question display, word display area, input field, virtual keyboard, and buttons ("Select Topic", "How To Play", "Submit").
    * Manages game state for the current round (tries remaining, current question/answer).
    * Interacts with `TriviaHangman` for game logic.
    * Handles user input and updates the UI accordingly (score, messages).
* **`trivia_hangman.py` (Backend Logic):**
    * `TriviaHangman` class: Manages the core game logic.
        * Loads questions, answers, and hints from topic-specific `.txt` files.
        * Provides methods to select a random question and check answers.
        * (Originally designed with hangman elements, now primarily supports trivia logic for the GUI).
