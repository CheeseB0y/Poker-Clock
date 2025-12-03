"""
Poker Time is a simple timer application built for poker tournaments.
"""

import sys
import os
import math
import csv
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from PIL import Image, ImageTk

BG_COLOR = "#0B6623"


def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller bundle.

    Args:
        relative_path (str): Relative path to be accessed for assets

    Returns:
        absolute_path (str): Absolute path to be used from pyinstaller when packaged
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)  # pylint: disable=protected-access
    return os.path.join(os.path.abspath("."), relative_path)


class PokerTime:
    """
    Main Function

    Initalizes basic program functions and starts on the landing page
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Time")
        self.root.geometry("1200x900")
        self.root.configure(bg=BG_COLOR)
        self.is_landing_page = True
        self.rounds = None
        self.landing_page = LandingPage(self)
        self.root.mainloop()


class Round:
    """
    Round object

    Games will be stored as an array of round objects
    """

    def __init__(self, num, time=0, s_blind=0, b_blind=0):
        self.num = num
        self.time = time
        self.s_blind = s_blind
        self.b_blind = b_blind

    def __str__(self):
        return f"Round: {self.num}\nTime: {self.time}\nSmall Blind: {self.s_blind}\nBig Blind: {self.b_blind}"


class LandingPage:
    """
    Program start page

    Serves as a welcome page for the user
    From this page you are able to start a game
    """

    def __init__(self, poker_time):
        self.root = poker_time.root

        self.root.columnconfigure((0, 1, 2), weight=1)
        self.root.rowconfigure((0, 1), weight=1)

        title_frame = tk.Frame(self.root, bg="black")
        title_frame.grid(row=0, column=0, columnspan=3, sticky="NESW")
        image_frame = tk.Frame(self.root, bg=BG_COLOR)
        image_frame.grid(row=1, column=0, columnspan=2, rowspan=3, sticky="NESW")
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.grid(row=1, column=2, rowspan=3)

        title = tk.Label(
            title_frame,
            text="Welcome to Poker Time!",
            bg="black",
            fg="white",
            font=("Arial", 60, "bold"),
        )
        title.pack(fill="both", expand=True, padx=10, pady=10)

        image_path = resource_path("assets/landing_page_img.jpg")
        image_file = Image.open(image_path).resize((800, 500))
        image = ImageTk.PhotoImage(image_file)
        stock_image = tk.Label(image_frame, image=image)
        stock_image.image = image
        stock_image.pack(expand=True)

        new_game_button = tk.Button(
            button_frame,
            text="New Game",
            command=lambda: EditorPage(
                poker_time, new=True, from_landing_page=poker_time.is_landing_page
            ),
            bg="red",
            fg="white",
            relief="raised",
            font=("Arial", 30, "bold"),
        )
        new_game_button.pack(fill="both", expand=True, padx=10, pady=10)

    def destroy(self):
        """
        Destroy the landing page once a game is started

        Args:
            None

        Returns:
            None
        """
        for widget in self.root.winfo_children():
            widget.destroy()


class MenuBar:
    """
    Menu bar class for options
    """

    def __init__(self, game_page):
        self.root = game_page.root

        menubar = tk.Menu(self.root, bg="black", fg="white", relief="raised")
        self.root.config(menu=menubar)

        option_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
        menubar.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(
            label="New Game", command=lambda: EditorPage(game_page, new=True)
        )
        option_menu.add_command(
            label="Edit Game", command=lambda: EditorPage(game_page)
        )
        option_menu.add_command(
            label="Game Overview",
            command=lambda: GameOverview(self.root, game_page.game_state.rounds),
        )
        option_menu.add_command(label="Restart Game", command=game_page.restart_game)
        option_menu.add_command(label="Exit", command=sys.exit)


class GameState:
    """
    Keeps track of what round it is and the blinds
    Use for reference in other classes so there is no mixup
    """

    def __init__(self, rounds):
        self.rounds = rounds
        self.round_index = 0
        self.round_num = self.rounds[self.round_index].num
        self.time = self.rounds[self.round_index].time
        self.s_blind = self.rounds[self.round_index].s_blind
        self.b_blind = self.rounds[self.round_index].b_blind

    def next_round(self):
        """
        Increment round counter and update values

        Args:
            None

        Returns:
            None
        """
        if len(self.rounds) > self.round_index + 1:
            self.round_index += 1
        self.round_num = self.rounds[self.round_index].num
        self.time = self.rounds[self.round_index].time
        self.s_blind = self.rounds[self.round_index].s_blind
        self.b_blind = self.rounds[self.round_index].b_blind

    def restart_game(self):
        """
        Set round counter to zero and update values

        Args:
            None

        Returns:
            None
        """
        self.round_index = 0
        self.round_num = self.rounds[self.round_index].num
        self.time = self.rounds[self.round_index].time
        self.s_blind = self.rounds[self.round_index].s_blind
        self.b_blind = self.rounds[self.round_index].b_blind

    def update_rounds(self, rounds):
        """
        Update round values when a change is made in the game editor

        Args:
            rounds (arr[Round]): New rounds to be applied to the GameState instance

        Returns:
            None
        """
        self.rounds = rounds
        self.round_index = min(self.round_index, len(rounds) - 1)
        self.round_num = self.rounds[self.round_index].num
        self.time = self.rounds[self.round_index].time
        self.s_blind = self.rounds[self.round_index].s_blind
        self.b_blind = self.rounds[self.round_index].b_blind


class Timer:
    """
    Timer object

    Handles start/stop formatting and other logic
    """

    def __init__(self, container, game_page):
        self.root = game_page.root
        self.game_page = game_page

        self.is_paused = True
        self.time_remaining = game_page.game_state.time * 60
        self.time_var = tk.StringVar(value=self.format_time(self.time_remaining))
        self.timer_label = tk.Label(
            container,
            textvariable=self.time_var,
            bg=BG_COLOR,
            fg="white",
            font=("Arial", 120, "bold"),
        )
        self.timer_label.pack(fill="both", expand=True)

    def start(self):
        """
        Start timer

        if timer is started pause timer
        if timer is zero reset timer

        Args:
            None

        Returns:
            None
        """
        if self.is_paused:
            self.unpause()
            self.game_page.timer_button.set_text("Pause Timer")
            self.countdown()
        elif self.time_remaining == 0:
            self.pause()
            self.game_page.stop_flashing()
            self.time_remaining = self.game_page.game_state.time * 60
            self.time_var.set(self.format_time(self.time_remaining))
            self.game_page.timer_button.set_text("Start Timer")
        else:
            self.pause()
            self.game_page.timer_button.set_text("Resume Timer")

    def pause(self):
        """Pause timer"""
        self.is_paused = True

    def unpause(self):
        """Unpause timer"""
        self.is_paused = False

    def countdown(self):
        """
        Timer countdown

        Args:
            None

        Returns:
            None
        """
        if self.time_remaining > 0 and not self.is_paused:
            self.time_var.set(self.format_time(self.time_remaining))
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)
        elif self.is_paused:
            pass
        else:
            self.time_var.set("0:00")
            self.game_page.timer_button.set_text("Reset Timer")
            self.game_page.flash_screen()

    def format_time(self, time):
        """
        Format time for reable display

        Args:
            time (int): Time in seconds

        Returns:
            time (str): Time in a readable clock format mm:ss
        """
        mins = time / 60
        secs = time % 60
        if secs < 10:
            secs = "0" + str(secs)
        return f"{math.floor(mins)}:{secs}"


class TimerButton:
    """
    Timer start/pause/reset button

    abstracted so that the button text can be easily modified
    """

    def __init__(self, container, game_page):
        self.timer_button_text = tk.StringVar(value="Start Timer")
        timer_button = tk.Button(
            container,
            textvariable=self.timer_button_text,
            command=game_page.timer.start,
            bg="red",
            fg="white",
            font=("Arial", 30, "bold"),
            relief="raised",
        )
        timer_button.pack(fill="both", expand=True, pady=50, padx=10)

    def set_text(self, text):
        """
        Set button label text

        Args:
            text (str): Text to be set as button label

        Returns:
            None
        """
        self.timer_button_text.set(value=text)


class GamePage:
    """
    Main game page
    """

    def __init__(self, poker_time):
        self.root = poker_time.root

        if poker_time.rounds is not None:
            poker_time.landing_page.destroy()
            poker_time.is_landing_page = False

        if not poker_time.is_landing_page:
            self.game_state = GameState(poker_time.rounds)

            self.round_num = tk.StringVar(value=f"Round: {self.game_state.round_num}")
            self.s_blind = tk.StringVar(
                value=f"Small Blind: {self.game_state.s_blind:,}"
            )
            self.b_blind = tk.StringVar(value=f"Big Blind: {self.game_state.b_blind:,}")

            MenuBar(self)
            self.root.columnconfigure((0, 1, 2), weight=1)
            self.root.rowconfigure((0, 1, 2, 3), weight=1)

            self.round_frame = tk.Frame(self.root, bg=BG_COLOR)
            self.round_frame.grid(row=0, column=0, columnspan=3, sticky="NESW")
            self.button_frame = tk.Frame(self.root, bg=BG_COLOR)
            self.button_frame.grid(row=1, column=2, rowspan=2, sticky="NESW")
            self.time_frame = tk.Frame(self.root, bg=BG_COLOR)
            self.time_frame.grid(
                row=1, column=0, rowspan=2, columnspan=2, sticky="NESW"
            )
            self.blind_frame = tk.Frame(self.root, bg=BG_COLOR)
            self.blind_frame.grid(row=3, column=0, columnspan=2, sticky="NESW")

            self.round_number_label = tk.Label(
                self.round_frame,
                textvariable=self.round_num,
                bg="black",
                fg="white",
                font=("Arial", 60, "bold"),
            )
            self.round_number_label.pack(fill="both", expand=True)
            self.timer = Timer(self.time_frame, self)
            self.timer_button = TimerButton(self.button_frame, self)
            next_button = tk.Button(
                self.button_frame,
                text="Next Round",
                command=self.next_round,
                bg="black",
                fg="white",
                font=("Arial", 30, "bold"),
                relief="raised",
            )
            next_button.pack(fill="both", expand=True, pady=50, padx=10)
            reset_button = tk.Button(
                self.button_frame,
                text="Reset Timer",
                command=self.restart_timer,
                bg="red",
                fg="white",
                font=("Arial", 30, "bold"),
                relief="raised",
            )
            reset_button.pack(fill="both", expand=True, pady=50, padx=10)
            s_blind_label = tk.Label(
                self.blind_frame,
                textvariable=self.s_blind,
                bg="black",
                fg="white",
                relief="raised",
                font=("Arial", 30, "bold"),
            )
            s_blind_label.pack(side="left", fill="both", expand=True, pady=10, padx=50)
            b_blind_label = tk.Label(
                self.blind_frame,
                textvariable=self.b_blind,
                bg="red",
                fg="white",
                relief="raised",
                font=("Arial", 30, "bold"),
            )
            b_blind_label.pack(side="right", fill="both", expand=True, pady=10, padx=50)

            self.is_flashing = False

    def flash_screen(self, duration=10, speed=500):
        """
        Flashes screen on timer completion

        Args:
            duration (int, optional): number of screen flash cycles
            speed (int, optional): time between flashes in miliseconds

        Returns:
            None
        """
        self.is_flashing = True
        self.flash_1(duration, speed)

    def stop_flashing(self):
        """
        Stops screen flashing

        Args:
            None

        Returns:
            None
        """
        self.is_flashing = False

    def flash_1(self, duration, speed):
        """
        First part of flash sequence
        should not be called directly

        Args:
            duration (int): number of screen flash cycles
            speed (int): time between flashes in miliseconds

        Returns:
            None
        """
        if duration > 0 and self.is_flashing:
            self.root.configure(bg="black")
            self.round_frame.configure(bg="black")
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg="black")
            self.time_frame.configure(bg="black")
            self.timer.timer_label.configure(bg="black")
            self.blind_frame.configure(bg="black")
            self.root.after(speed, lambda: self.flash_2(duration, speed))
        else:
            self.root.configure(bg=BG_COLOR)
            self.round_frame.configure(bg=BG_COLOR)
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg=BG_COLOR)
            self.time_frame.configure(bg=BG_COLOR)
            self.timer.timer_label.configure(bg=BG_COLOR)
            self.blind_frame.configure(bg=BG_COLOR)

    def flash_2(self, duration, speed):
        """
        Second part of flash sequence
        should not be called directly

        Args:
            duration (int): number of screen flash cycles
            speed (int): time between flashes in miliseconds

        Returns:
            None
        """
        if self.is_flashing:
            self.root.configure(bg="white")
            self.round_frame.configure(bg="white")
            self.round_number_label.configure(bg="white")
            self.button_frame.configure(bg="white")
            self.time_frame.configure(bg="white")
            self.timer.timer_label.configure(bg="white")
            self.blind_frame.configure(bg="white")
            self.root.after(speed, lambda: self.flash_1(duration - 1, speed))
        else:
            self.root.configure(bg=BG_COLOR)
            self.round_frame.configure(bg=BG_COLOR)
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg=BG_COLOR)
            self.time_frame.configure(bg=BG_COLOR)
            self.timer.timer_label.configure(bg=BG_COLOR)
            self.blind_frame.configure(bg=BG_COLOR)

    def refresh_round_values(self):
        """
        Refresh values on screen

        Args:
            None

        Returns:
            None
        """
        self.timer.time_remaining = self.game_state.time * 60
        self.timer.time_var.set(value=self.timer.format_time(self.timer.time_remaining))
        self.timer_button.set_text("Start Timer")
        self.round_num.set(f"Round: {self.game_state.round_num}")
        self.s_blind.set(f"Small Blind: {self.game_state.s_blind:,}")
        self.b_blind.set(f"Big Blind: {self.game_state.b_blind:,}")

    def next_round(self):
        """
        Starts next round

        Args:
            None

        Returns:
            None
        """
        self.timer.pause()
        self.stop_flashing()
        self.game_state.next_round()
        self.refresh_round_values()

    def restart_game(self):
        """
        Restarts game from round 1

        Args:
            None

        Returns:
            None
        """
        self.timer.pause()
        self.stop_flashing()
        self.game_state.restart_game()
        self.refresh_round_values()

    def restart_timer(self):
        self.timer.pause()
        self.stop_flashing()
        self.timer.time_remaining = self.timer.game_page.game_state.time * 60
        self.timer.time_var.set(self.timer.format_time(self.timer.time_remaining))
        self.timer.game_page.timer_button.set_text("Start Timer")


class EditorPage:
    """
    Game editor window

    create a new game or edit an existing one
    import or export game files as csv
    """

    def __init__(self, ctx, new=False, from_landing_page=False):
        window = tk.Toplevel(ctx.root)
        self.ctx = ctx
        self.from_landing_page = from_landing_page
        if new:
            window.title("New Game")
            self.rounds = []
        else:
            window.title("Edit Game")
            self.rounds = self.ctx.game_state.rounds

        window.geometry("800x600")
        window.configure(bg=BG_COLOR)
        window.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        round_column_heading = tk.Frame(window, bg="red")
        round_column_heading.grid(row=0, column=1, sticky="NESW")
        self.round_column = tk.Frame(window, bg="red")
        self.round_column.grid(row=1, column=1, sticky="NESW")

        time_column_heading = tk.Frame(window, bg="black")
        time_column_heading.grid(row=0, column=2, sticky="NESW")
        self.time_column = tk.Frame(window, bg="black")
        self.time_column.grid(row=1, column=2, sticky="NESW")

        s_blind_column_heading = tk.Frame(window, bg="red")
        s_blind_column_heading.grid(row=0, column=3, sticky="NESW")
        self.s_blind_column = tk.Frame(window, bg="red")
        self.s_blind_column.grid(row=1, column=3, sticky="NESW")

        b_blind_column_heading = tk.Frame(window, bg="black")
        b_blind_column_heading.grid(row=0, column=4, sticky="NESW")
        self.b_blind_column = tk.Frame(window, bg="black")
        self.b_blind_column.grid(row=1, column=4, sticky="NESW")

        round_column_label = tk.Label(
            round_column_heading, text="Rounds:", bg="red", fg="white"
        )
        round_column_label.pack(fill="both", expand=True, side="left")
        self.num_rounds_entry = tk.Entry(
            round_column_heading, width=2, bg="red", fg="white"
        )
        self.num_rounds_entry.pack(fill="both", expand=True, side="right")
        self.num_rounds_entry.insert(tk.END, len(self.rounds))
        time_column_label = tk.Label(
            time_column_heading, text="Time", bg="black", fg="white"
        )
        time_column_label.pack(fill="both", expand=True)
        s_blind_column_label = tk.Label(
            s_blind_column_heading, text="Small Blind", bg="red", fg="white"
        )
        s_blind_column_label.pack(fill="both", expand=True)
        b_blind_column_label = tk.Label(
            b_blind_column_heading, text="Big Blind", bg="black", fg="white"
        )
        b_blind_column_label.pack(fill="both", expand=True)

        self.time_list = []
        self.s_blind_list = []
        self.b_blind_list = []

        for index, r in enumerate(self.rounds):
            tk.Label(self.round_column, text=r.num, bg="red", fg="white").pack(
                fill="both", expand=True
            )
            self.time_list.append(
                tk.Entry(self.time_column, width=6, bg="black", fg="white")
            )
            self.time_list[index].pack(fill="both", expand=True)
            self.time_list[index].insert(tk.END, r.time)
            self.s_blind_list.append(
                tk.Entry(self.s_blind_column, width=10, bg="red", fg="white")
            )
            self.s_blind_list[index].pack(fill="both", expand=True)
            self.s_blind_list[index].insert(tk.END, r.s_blind)
            self.b_blind_list.append(
                tk.Entry(self.b_blind_column, width=10, bg="black", fg="white")
            )
            self.b_blind_list[index].pack(fill="both", expand=True)
            self.b_blind_list[index].insert(tk.END, r.b_blind)

        button_frame = tk.Frame(window, bg=BG_COLOR)
        button_frame.grid(row=2, column=1, columnspan=4, sticky="NESW")
        tk.Button(
            button_frame,
            text="Save Game",
            command=self.save_game,
            bg="black",
            fg="white",
        ).pack(side="left", fill="both", expand=True)
        tk.Button(
            button_frame,
            text="Export Game",
            command=self.export_game,
            bg="red",
            fg="white",
        ).pack(side="left", fill="both", expand=True)
        tk.Button(
            button_frame,
            text="Import Game",
            command=self.import_game,
            bg="black",
            fg="white",
        ).pack(side="left", fill="both", expand=True)
        if from_landing_page:
            tk.Button(
                button_frame,
                text="Start Game",
                command=lambda: GamePage(self.ctx),
                bg="red",
                fg="white",
            ).pack(side="left", fill="both", expand=True)

    def refresh_editor(self):
        """
        Refresh editor screen when changes are made

        Args:
            None

        Returns:
            None
        """
        for widget in self.round_column.winfo_children():
            widget.destroy()
        self.time_list.clear()
        for widget in self.time_column.winfo_children():
            widget.destroy()
        self.s_blind_list.clear()
        for widget in self.s_blind_column.winfo_children():
            widget.destroy()
        self.b_blind_list.clear()
        for widget in self.b_blind_column.winfo_children():
            widget.destroy()
        self.num_rounds_entry.delete(0, tk.END)
        self.num_rounds_entry.insert(tk.END, len(self.rounds))
        for index, r in enumerate(self.rounds):
            tk.Label(self.round_column, text=r.num, bg="red", fg="white").pack(
                fill="both", expand=True
            )
            self.time_list.append(
                tk.Entry(self.time_column, width=6, bg="black", fg="white")
            )
            self.time_list[index].pack(fill="both", expand=True)
            self.time_list[index].insert(tk.END, r.time)
            self.s_blind_list.append(
                tk.Entry(self.s_blind_column, width=10, bg="red", fg="white")
            )
            self.s_blind_list[index].pack(fill="both", expand=True)
            self.s_blind_list[index].insert(tk.END, r.s_blind)
            self.b_blind_list.append(
                tk.Entry(self.b_blind_column, width=10, bg="black", fg="white")
            )
            self.b_blind_list[index].pack(fill="both", expand=True)
            self.b_blind_list[index].insert(tk.END, r.b_blind)

    def save_game(self):
        """
        Save editor values

        Args:
            None

        Returns:
            None
        """
        try:
            num_rounds = int(self.num_rounds_entry.get())
        except ValueError:
            self.num_rounds_entry.delete(0, tk.END)
            self.num_rounds_entry.insert(tk.END, len(self.rounds))
            num_rounds = len(self.rounds)
        rounds = []
        for i in range(num_rounds):
            try:
                rounds.append(
                    Round(
                        i + 1,
                        int(self.time_list[i].get()),
                        int(self.s_blind_list[i].get()),
                        int(self.b_blind_list[i].get()),
                    )
                )
            except IndexError:
                rounds.append(Round(i + 1))
            except ValueError:
                rounds.append(Round(i + 1))
        if self.from_landing_page:
            self.ctx.rounds = rounds
        else:
            self.ctx.game_state.update_rounds(rounds)
            self.ctx.refresh_round_values()
        self.rounds = rounds
        self.refresh_editor()

    def export_game(self):
        """
        Export game as CSV

        Args:
            None

        Returns:
            None
        """
        documents_dir = Path.home() / "Documents"
        poker_dir = documents_dir / "PokerTime"
        poker_dir.mkdir(parents=True, exist_ok=True)

        self.save_game()

        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir=poker_dir,
            title="Choose where to save the game file.",
            filetypes=(("CVS files", "*.csv"), ("All files", "*.*")),
        )

        if self.from_landing_page:
            source = self.ctx.rounds
        else:
            source = self.ctx.game_state.rounds

        if file:
            with open(file, "w", newline="", encoding="utf-8") as f:
                for r in source:
                    f.write(f"{r.num},{r.time},{r.s_blind},{r.b_blind}\n")

    def import_game(self):
        """
        Import a game from a CSV file

        Args:
            None

        Returns:
            None
        """
        documents_dir = Path.home() / "Documents"
        poker_dir = documents_dir / "PokerTime"
        poker_dir.mkdir(parents=True, exist_ok=True)

        file = filedialog.askopenfilename(
            initialdir=poker_dir,
            title="Select a file",
            filetypes=(("CVS files", "*.csv"), ("All files", "*.*")),
        )

        rounds = []

        if file:
            with open(file, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    rounds.append(
                        Round(int(row[0]), int(row[1]), int(row[2]), int(row[3]))
                    )

        if self.from_landing_page:
            self.ctx.rounds = rounds
        else:
            self.ctx.game_state.update_rounds(rounds)
            self.ctx.refresh_round_values()
        self.rounds = rounds
        self.refresh_editor()


class GameOverview:
    """
    Basic overview page to see all round data
    """

    def __init__(self, root, rounds):
        window = tk.Toplevel(root)
        window.title("Game Overview")
        window.geometry("800x600")
        window.configure(bg=BG_COLOR)

        window.columnconfigure((0, 1, 2, 3), weight=1)
        for i in range(len(rounds)):
            window.rowconfigure(i, weight=1)

        round_column = tk.Frame(window, bg="red")
        round_column.grid(row=0, column=0, rowspan=len(rounds), sticky="NESW")
        time_column = tk.Frame(window, bg="black")
        time_column.grid(row=0, column=1, rowspan=len(rounds), sticky="NESW")
        s_blind_column = tk.Frame(window, bg="red")
        s_blind_column.grid(row=0, column=2, rowspan=len(rounds), sticky="NESW")
        b_blind_column = tk.Frame(window, bg="black")
        b_blind_column.grid(row=0, column=3, rowspan=len(rounds), sticky="NESW")

        tk.Label(round_column, text="Round", bg="red", fg="white").grid(
            row=0, column=0, padx=10, pady=10, sticky="NSWE"
        )
        tk.Label(time_column, text="Time", bg="black", fg="white").grid(
            row=0, column=1, padx=10, pady=10, sticky="NSWE"
        )
        tk.Label(s_blind_column, text="Small Blind", bg="red", fg="white").grid(
            row=0, column=2, padx=10, pady=10, sticky="NSWE"
        )
        tk.Label(b_blind_column, text="Big Blind", bg="black", fg="white").grid(
            row=0, column=3, padx=10, pady=10, sticky="NSWE"
        )

        for index, r in enumerate(rounds):
            tk.Label(round_column, text=r.num, bg="red", fg="white").grid(
                row=index + 1, column=0, padx=10, pady=10, sticky="NSWE"
            )
            tk.Label(time_column, text=r.time, bg="black", fg="white").grid(
                row=index + 1, column=1, padx=10, pady=10, sticky="NSWE"
            )
            tk.Label(s_blind_column, text=r.s_blind, bg="red", fg="white").grid(
                row=index + 1, column=2, padx=10, pady=10, sticky="NSWE"
            )
            tk.Label(b_blind_column, text=r.b_blind, bg="black", fg="white").grid(
                row=index + 1, column=3, padx=10, pady=10, sticky="NSWE"
            )


if __name__ == "__main__":
    PokerTime()
