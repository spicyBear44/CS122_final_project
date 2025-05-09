import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import random
from trivia_hangman import TriviaHangman


class GameScreen:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        self.game = TriviaHangman()

        self.canvas = tk.Canvas(self.root, width=800, height=800, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background image
        og_image = Image.open("background.jpeg")
        resized_image = og_image.resize((800, 800), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Game state
        self.reset_game_state()

        # UI elements
        self.create_topic_button()
        self.create_how_to_play_button()
        self.create_question_display()
        self.create_word_display()
        self.create_input_frame()
        self.create_keyboard()

        # Hide input and keyboard initially
        self.keyboard_frame.place_forget()
        self.input_frame.place_forget()

        # Submit button
        self.submit_btn = tk.Button(
            self.root,
            text="Submit",
            font=("Comic Sans MS", 16, "bold"),
            bg="white",
            fg="black",
            command=self.submit_guess
        )
        self.submit_btn.place_forget()

        # Score feature
        self.score = 0
        self.create_score_badge()

    def reset_round_state(self):
        self.tries_remaining = 3
        self.current_question = ""
        self.current_answer = ""
        self.current_hint = ""

    def reset_game_state(self):
        self.reset_round_state()
        self.game_started = False
        self.game_elements_visible = False

    def create_question_display(self):
        self.question_frame = tk.Frame(self.canvas, bg="white", bd=2, highlightbackground="black", highlightthickness=2)
        self.question_label = tk.Label(
            self.question_frame,
            text="",
            font=("Comic Sans MS", 16),
            bg="white",
            fg="black",
            wraplength=650,
            justify="center"
        )
        self.question_label.pack(expand=True, fill="both")

        self.question_window = self.canvas.create_window(
        400, 320, window=self.question_frame, width=700, height=100
        )
        self.canvas.itemconfigure(self.question_window, state="hidden")

    def create_word_display(self):
        self.word_display = self.canvas.create_text(
            400, 340,
            text="",
            font=("Comic Sans MS", 40, "bold"),
            fill="white",
            state="hidden"
        )

    def create_input_frame(self):
        self.input_var = tk.StringVar()
        self.input_frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=2)
        self.input_display = tk.Label(
            self.input_frame,
            textvariable=self.input_var,
            font=("Comic Sans MS", 24),
            bg="white",
            fg="black"
        )
        self.input_display.pack(fill="both", expand=True)

    def create_keyboard(self):
        self.keyboard_frame = tk.Frame(self.root, bg="white", highlightbackground="black", highlightthickness=2)
        self.keyboard_frame.place(x=150, y=600, width=508, height=150)

        # Keyboard layout
        keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
        ]

        for i, row in enumerate(keyboard_layout):
            for j, key in enumerate(row):
                # Create each button with a more refined style
                btn = tk.Button(self.keyboard_frame, text=key, font=("Comic Sans MS", 12, "bold"),
                                width=4, height=2, relief="flat", bg="#5c5c5c", fg="black", activebackground="#87CEEB",
                                activeforeground="black", bd=0, highlightthickness=0,
                                command=lambda k=key: self.key_pressed(
                                    k) if k != 'delete' else self.backspace_pressed())
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

                self.keyboard_frame.grid_rowconfigure(i, weight=1)
                self.keyboard_frame.grid_columnconfigure(j, weight=1)

        backspace_btn = tk.Button(self.keyboard_frame, text="delete", font=("Comic Sans MS", 12, "bold"), width=5,
                                  height=2,
                                  relief="flat", bg="white", fg="black", activebackground="#87CEEB",
                                  activeforeground="black",
                                  bd=0, highlightthickness=0, command=self.backspace_pressed)
        backspace_btn.grid(row=3, column=15, padx=5, pady=5, sticky="nsew")

    def select_topic(self, topic):
        content = self.game.load_question(topic.lower())
        self.current_question = content['question']
        self.current_answer = content['answer'].upper()
        self.current_hint = content['hint']

        self.question_label.config(text=self.current_question)
        self.input_var.set("")
        if not self.game_elements_visible:
            self.game_elements_visible = True
            self.update_game_visibility()



    def update_game_visibility(self):
        state = 'normal' if self.game_elements_visible else 'hidden'
        self.canvas.itemconfigure(self.question_window, state=state)
        self.canvas.itemconfigure(self.word_display, state=state)

        if self.game_elements_visible:
            self.keyboard_frame.place(x=150, y=560, width=508, height=150)
            self.input_frame.place(x=200, y=490, width=400, height=60)
            self.submit_btn.place(x=340, y=740, width=120, height=50)
        else:
            self.keyboard_frame.place_forget()
            self.input_frame.place_forget()
            self.submit_btn.place_forget()

    def create_topic_button(self):
        self.create_button(180, 20, 310, 60, "Select Topic", "topic", self.show_topic_menu)

    def create_how_to_play_button(self):
        self.create_button(20, 20, 150, 60, "How To Play", "how_to_play", self.show_instructions)

    def create_score_badge(self):
        x1,y1,x2,y2 = 630, 20, 754, 60
        tag = "score"
        bg_tag, text_tag = f"{tag}_bg", f"{tag}_text"
        self.create_rounded_rectangle(x1,y1,x2,y2,radius=20,fill="white", outline="lightblue", width=4, tags=bg_tag)
        self.score_text = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"Score: {self.score}",
                                                  font=("Comic Sans MS", 16, "bold"), fill="black", tags=text_tag)

    def update_score(self, points):
        self.score += points
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def create_button(self, x1, y1, x2, y2, text, tag, command):
        bg_tag, text_tag, hitbox_tag = f"{tag}_btn_bg", f"{tag}_btn_text", f"{tag}_btn"
        self.create_rounded_rectangle(x1, y1, x2, y2, radius=25, fill="white", outline="lightblue", width=3,
                                      tags=bg_tag)
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text,
                                font=("Comic Sans MS", 16, "bold"), fill="black", tags=text_tag)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="", outline="", width=0, tags=hitbox_tag)
        self.canvas.tag_bind(hitbox_tag, "<Enter>", lambda e: self.button_hover_effect(tag, True))
        self.canvas.tag_bind(hitbox_tag, "<Leave>", lambda e: self.button_hover_effect(tag, False))
        self.canvas.tag_bind(hitbox_tag, "<Button-1>", command)

    def show_topic_menu(self, event=None):
        menu = tk.Menu(self.root, tearoff=0, font=("Comic Sans MS", 12))
        for topic in ['History', 'Science', 'Movies', 'Geography']:
            menu.add_command(label=topic, command=lambda t=topic.lower(): self.select_topic(t))
        menu.post(self.root.winfo_rootx() + 180, self.root.winfo_rooty() + 60)

    def button_hover_effect(self, btn_type, hovering):
        bg_tag = f"{btn_type}_btn_bg"
        self.canvas.itemconfig(bg_tag, fill="lightblue" if hovering else "white", width=9 if hovering else 2)

    def show_instructions(self, event=None):
        messagebox.showinfo("Instructions", """HOW TO PLAY:
            • You have 3 tries to guess the hidden word.
            • Each wrong guess costs a life.
            • After 3 misses, it's game over!

            Type your guess, hit Submit, and good luck!
            """)

    def key_pressed(self, key):
        self.input_var.set(self.input_var.get() + key)

    def backspace_pressed(self):
        self.input_var.set(self.input_var.get()[:-1])

    def submit_guess(self):
        guess = self.input_var.get().upper()
        if not guess:
            messagebox.showinfo("Error", "Please enter a word before submitting")
            return
        if guess == self.current_answer:
            messagebox.showinfo("Congratulations!", "You guessed correctly!")
            self.canvas.itemconfig(self.word_display, text=self.current_answer)
            self.update_score(5)
            self.reset_round_state()
            self.update_game_visibility()
        else:
            self.tries_remaining -= 1
            if self.tries_remaining > 0:
                messagebox.showinfo("Incorrect", f"{self.tries_remaining} tries remaining.")
                self.input_var.set("")
            else:
                messagebox.showinfo("Game Over", f"The word was {self.current_answer}. Your final score is {self.score}")
                self.canvas.itemconfig(self.word_display, text=self.current_answer)
                self.reset_game_state()
                self.score = 0
                self.update_score(0)

                self.update_game_visibility()

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
                  x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
                  x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)