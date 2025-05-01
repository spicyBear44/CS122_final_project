import os
import random


class TriviaHangman:
    def __init__(self):
        self.topics = {
            'history': 'history.txt',
            'science': 'science.txt',
            'movies': 'movies.txt',
            'geography': 'geography.txt'
        }

        self.max_attempts = 3
        self.attempts_left = self.max_attempts
        self.current_question = ""
        self.current_answer = ""
        self.hidden_answer = []
        self.hint_displayed = False


    def load_question(self, topic):
        try:
            with open(self.topics[topic], 'r') as f:
                questions = f.read().strip().split('\n')
                question_data = random.choice(questions).split('|')
                return {
                    'question': question_data[0],
                    'answer': question_data[1],
                    'hint': question_data[2] if len(question_data) > 2 else "No hint available"
                }
        except FileNotFoundError:
            print(f"Question file for {topic} not found.")


    def display_game_state(self):
        print("\nTopic: " + self.current_topic.capitalize())
        print("\nQuestion: " + self.current_question)
        print("\nAnswer: " + " ".join(self.hidden_answer))

        print(f"\nAttempts left: {self.attempts_left}")


    def update_hidden_answer(self, guess):
        revealed = False
        for i, char in enumerate(self.current_answer):
            if char.lower() == guess.lower():
                self.hidden_answer[i] = char
                revealed = True
        return revealed

    def is_answer_complete(self):
        return "_" not in self.hidden_answer

    def check_answer(self, guess):
        print(f"{guess}, {self.current_answer}")
        return guess.lower() == self.current_answer.lower()

    def initialize_hidden_answer(self):
        self.hidden_answer = []
        for char in self.current_answer:
            if char.isalpha():
                self.hidden_answer.append("_")
            else:
                self.hidden_answer.append(char)

    def play(self):
        print("Welcome to Trivia Hangman!")
        print("\nChoose a topic:")

        for i, topic in enumerate(self.topics.keys(), 1):
            print(f"{i}. {topic.capitalize()}")

        while True:
            choice = input("\nEnter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                self.current_topic = list(self.topics.keys())[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

        question_data = self.load_question(self.current_topic)
        self.current_question = question_data['question']
        self.current_answer = question_data['answer']

        self.attempts_left = self.max_attempts
        self.hint_displayed = False
        self.initialize_hidden_answer()

        while True:
            self.display_game_state()

            if self.is_answer_complete():
                print(f"\nCongratulations! You've revealed the answer: {self.current_answer}")
                break

            guess = input("\nGuess a letter or the full answer: ").strip()

            if not guess:
                print("Please enter a guess.")
                continue

            if self.check_answer(guess):
                if len(guess) == 1:
                    if self.is_answer_complete():
                        self.display_game_state()
                        print(f"\nCongratulations! You've revealed the answer: {self.current_answer}")
                        break
                else:
                    self.hidden_answer = list(self.current_answer)
                    self.display_game_state()
                    print(f"\nCorrect! The answer is: {self.current_answer}")
                    break
            else:
                self.attempts_left -= 1
                if len(guess) == 1:
                    print(f"\nThe letter '{guess}' is not in the answer.")
                else:
                    print(f"\n'{guess}' is not the correct answer.")

                if self.attempts_left == 0:
                    self.hidden_answer = list(self.current_answer)
                    self.display_game_state()
                    print(f"\nGame Over! The correct answer was: {self.current_answer}")
                    break

    def play_again(self):
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()
        return choice == 'y'


def main():
    game = TriviaHangman()

    while True:
        game.play()
        if not game.play_again():
            print("Thanks for playing Trivia Hangman!")
            break


if __name__ == "__main__":
    main()