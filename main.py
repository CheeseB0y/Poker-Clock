import tkinter as tk
import math
import csv
from tkinter import filedialog
from pathlib import Path

class Round:
    def __init__(self, num, time=0, s_blind=0, b_blind=0):
        self.num = num
        self.time = time
        self.s_blind = s_blind
        self.b_blind = b_blind

class PokerClock:

    def __init__(self, rounds):
        self.root = tk.Tk()
        self.rounds = rounds
        self.num_rounds = len(rounds)
        self.round_index = 0
        self.round_num = tk.StringVar(value=f"Round: {self.rounds[self.round_index].num}")
        self.b_blind = tk.StringVar(value=f"Big Blind: {self.rounds[self.round_index].b_blind:,}")
        self.s_blind = tk.StringVar(value=f"Small Blind: {self.rounds[self.round_index].s_blind:,}")
        self.time_remaining = self.rounds[self.round_index].time * 60
        self.time_display = tk.StringVar(value=self.format_time_remaining())

        self.bg_color = "#0B6623"
        self.pause = True
        self.timer_button_text = tk.StringVar(value="Start Timer")

        self.root.title("Poker Clock")
        self.root.geometry("1200x900")
        self.root.configure(bg=self.bg_color)
        
        menubar = tk.Menu(self.root, bg="black", fg="white", relief="raised")
        self.root.config(menu=menubar)

        self.bg_color = "#0B6623"
        
        option_menu = tk.Menu(menubar, tearoff=0, bg="black", fg="white")
        menubar.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(label="New Game", command=self.new_game)
        option_menu.add_command(label="Edit Game", command=self.game_editor)
        option_menu.add_command(label="Game Overview", command=self.game_overview)
        option_menu.add_command(label="Restart Game", command=self.restart_game)
        option_menu.add_command(label="Exit", command=quit)

        self.root.columnconfigure((0, 1, 2), weight=1)
        self.root.rowconfigure((0, 1, 2, 3), weight=1)
        
        self.round_frame = tk.Frame(self.root, bg=self.bg_color)
        self.round_frame.grid(row=0, column=0, columnspan=3, sticky="NESW")

        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.grid(row=1, column=2, rowspan=2, sticky="NESW")

        self.time_frame = tk.Frame(self.root, bg=self.bg_color)
        self.time_frame.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="NESW")

        self.blind_frame = tk.Frame(self.root, bg=self.bg_color)
        self.blind_frame.grid(row=3, column=0, columnspan=2, sticky="NESW")

        self.round_number_label = tk.Label(self.round_frame, textvariable=self.round_num, bg="black", fg="white", font=("Arial", 60, "bold"))
        self.round_number_label.pack(fill="both", expand=True)
        self.timer_label = tk.Label(self.time_frame, textvariable=self.time_display, bg=self.bg_color, fg="white", font=("Arial", 120, "bold"))
        self.timer_label.pack(fill="both", expand=True)
        timer_button = tk.Button(self.button_frame, textvariable=self.timer_button_text, command=self.start_timer, bg="red", fg="white", font=("Arial", 30, "bold"), relief="raised")
        timer_button.pack(fill="both", expand=True, pady=100, padx=10)
        next_button = tk.Button(self.button_frame, text="Next Round", command=self.next_round, bg="black", fg="white", font=("Arial", 30, "bold"), relief="raised")
        next_button.pack(fill="both", expand=True, pady=100, padx=10)
        s_blind_label = tk.Label(self.blind_frame, textvariable=self.s_blind, bg="black", fg="white", relief="raised", font=("Arial", 30, "bold"))
        s_blind_label.pack(side="left", fill="both", expand=True, pady=10, padx=50)
        b_blind_label = tk.Label(self.blind_frame, textvariable=self.b_blind, bg="red", fg="white", relief="raised", font=("Arial", 30, "bold"))
        b_blind_label.pack(side="right", fill="both", expand=True, pady=10, padx=50)
        

        self.root.mainloop()

    def start_timer(self):
        if self.pause:
            self.pause = False
            self.timer_button_text.set("Pause Timer")
            self.countdown()
        else:
            self.pause_timer()
            self.timer_button_text.set("Resume Timer")

    def pause_timer(self):
        self.pause = True

    def countdown(self):
        if self.time_remaining > 0 and self.pause == False:
            self.time_display.set(self.format_time_remaining())
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)
        elif self.pause:
            pass
        else:
            self.time_display.set("0:00")
            self.flash = True
            self.flash_screen()

    def format_time_remaining(self): 
        mins = self.time_remaining / 60
        secs = self.time_remaining % 60
        if secs < 10:
            secs = "0" + str(secs)
        return f"{math.floor(mins)}:{secs}"

    
    # This needs to be like this for some reason
    def flash_screen(self, duration=10, speed=500):
        if duration > 0 and self.flash:
            self.root.configure(bg="black")
            self.round_frame.configure(bg="black")
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg="black")
            self.time_frame.configure(bg="black")
            self.timer_label.configure(bg="black")
            self.blind_frame.configure(bg="black")
            self.root.after(speed, lambda: self.flash_screen_2(duration, speed))
        else:
            self.root.configure(bg=self.bg_color)
            self.round_frame.configure(bg=self.bg_color)
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg=self.bg_color)
            self.time_frame.configure(bg=self.bg_color)
            self.timer_label.configure(bg=self.bg_color)
            self.blind_frame.configure(bg=self.bg_color)
    def flash_screen_2(self, duration, speed):
        if self.flash:
            self.root.configure(bg="white")
            self.round_frame.configure(bg="white")
            self.round_number_label.configure(bg="white")
            self.button_frame.configure(bg="white")
            self.time_frame.configure(bg="white")
            self.timer_label.configure(bg="white")
            self.blind_frame.configure(bg="white")
            self.root.after(speed, lambda: self.flash_screen(duration - 1, speed))
        else:
            self.root.configure(bg=self.bg_color)
            self.round_frame.configure(bg=self.bg_color)
            self.round_number_label.configure(bg="black")
            self.button_frame.configure(bg=self.bg_color)
            self.time_frame.configure(bg=self.bg_color)
            self.timer_label.configure(bg=self.bg_color)
            self.blind_frame.configure(bg=self.bg_color)

    def next_round(self):
        self.flash = False
        self.pause = True
        self.round_index += 1
        try:
            self.time_remaining = self.rounds[self.round_index].time * 60
        except IndexError:
            self.round_index -= 1
            self.time_remaining = self.rounds[self.round_index].time * 60
        self.time_display.set(value=self.format_time_remaining())
        self.timer_button_text.set("Start Timer")
        self.round_num.set(f"Round: {self.rounds[self.round_index].num}")
        self.b_blind.set(f"Big Blind: {self.rounds[self.round_index].b_blind:,}")
        self.s_blind.set(f"Small Blind: {self.rounds[self.round_index].s_blind:,}")
    
    def restart_game(self):
        self.flash = False
        self.pause = True
        self.round_index = 0
        self.time_remaining = self.rounds[self.round_index].time * 60
        self.time_display.set(value=self.format_time_remaining())
        self.timer_button_text.set("Start Timer")
        self.round_num.set(f"Round: {self.rounds[self.round_index].num}")
        self.b_blind.set(f"Big Blind: {self.rounds[self.round_index].b_blind:,}")
        self.s_blind.set(f"Small Blind: {self.rounds[self.round_index].s_blind:,}")

    def build_editor(self, window, rounds):
        window.geometry("800x600")
        window.configure(bg=self.bg_color)

        window.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        round_column_heading = tk.Frame(window, bg="red")
        round_column_heading.grid(row=0, column=1, sticky="NESW")
        self.round_column = tk.Frame(window, bg="red")
        self.round_column.grid(row=1, column=1, sticky='NESW')
        time_column_heading = tk.Frame(window, bg="black")
        time_column_heading.grid(row=0, column=2, sticky='NESW')
        self.time_column = tk.Frame(window, bg="black")
        self.time_column.grid(row=1, column=2, sticky='NESW')
        s_blind_column_heading = tk.Frame(window, bg="red")
        s_blind_column_heading.grid(row=0, column=3, sticky='NESW')
        self.s_blind_column = tk.Frame(window, bg="red")
        self.s_blind_column.grid(row=1, column=3, sticky='NESW')
        b_blind_column_heading = tk.Frame(window, bg="black")
        b_blind_column_heading.grid(row=0, column=4, sticky='NESW')
        self.b_blind_column = tk.Frame(window, bg="black")
        self.b_blind_column.grid(row=1, column=4, sticky='NESW')

        round_column_label = tk.Label(round_column_heading, text="Rounds:", bg="red", fg="white")
        round_column_label.pack(fill="both", expand=True, side="left")
        self.num_rounds_entry = tk.Entry(round_column_heading, width=2, bg="red", fg="white")
        self.num_rounds_entry.pack(fill="both", expand=True, side="right")
        self.num_rounds_entry.insert(tk.END, len(rounds))
        time_column_label = tk.Label(time_column_heading, text="Time", bg="black", fg="white")
        time_column_label.pack(fill="both", expand=True)
        s_blind_column_label = tk.Label(s_blind_column_heading, text="Small Blind", bg="red", fg="white")
        s_blind_column_label.pack(fill="both", expand=True)
        b_blind_column_label = tk.Label(b_blind_column_heading, text="Big Blind", bg="black", fg="white")
        b_blind_column_label.pack(fill="both", expand=True)

        self.time_list = []
        self.s_blind_list = []
        self.b_blind_list = []

        for (index, round) in enumerate(rounds):
            tk.Label(self.round_column, text=round.num, bg="red", fg="white").pack(fill="both", expand=True)
            self.time_list.append(tk.Entry(self.time_column, width=6, bg="black", fg="white"))
            self.time_list[index].pack(fill="both", expand=True)
            self.time_list[index].insert(tk.END, round.time)
            self.s_blind_list.append(tk.Entry(self.s_blind_column, width=10, bg="red", fg="white"))
            self.s_blind_list[index].pack(fill="both", expand=True)
            self.s_blind_list[index].insert(tk.END, round.s_blind)
            self.b_blind_list.append(tk.Entry(self.b_blind_column, width=10, bg="black", fg="white"))
            self.b_blind_list[index].pack(fill="both", expand=True)  
            self.b_blind_list[index].insert(tk.END, round.b_blind)

        button_frame = tk.Frame(window, bg=self.bg_color)
        button_frame.grid(row=self.num_rounds+2, column=1, columnspan=4, sticky="NESW")
        tk.Button(button_frame, text="Save Game", command=self.save_game, bg="black", fg="white").pack(side="left", fill="both", expand=True)
        tk.Button(button_frame, text="Export Game", command=self.export_game, bg="red", fg="white").pack(side="left", fill="both", expand=True)
        tk.Button(button_frame, text="Import Game", command=self.import_game, bg="black", fg="white").pack(side="left", fill="both", expand=True)

    def new_game(self):
        new_game_window = tk.Toplevel(self.root)
        new_game_window.title("Game Editor")
        self.build_editor(new_game_window, [])

    def game_editor(self):
        game_editor_window = tk.Toplevel(self.root)
        game_editor_window.title("Game Editor")
        self.build_editor(game_editor_window, self.rounds)

    def save_game(self):
        try:
            self.num_rounds = int(self.num_rounds_entry.get())
        except ValueError:
            self.num_rounds_entry.delete(0, tk.END)
            self.num_rounds_entry.insert(tk.END, self.num_rounds)
        rounds = []
        for i in range(self.num_rounds):
            try:
                rounds.append(Round(i+1, int(self.time_list[i].get()), int(self.s_blind_list[i].get()), int(self.b_blind_list[i].get())))
            except IndexError:
                rounds.append(Round(i+1))
            except ValueError:
                rounds.append(Round(i+1))
        self.rounds = rounds
        self.refresh_editor()

    def refresh_editor(self):
        for widget in self.round_column.winfo_children():
            widget.destroy()
        for widget in self.time_column.winfo_children():
            widget.destroy()
        self.s_blind_list.clear()
        for widget in self.s_blind_column.winfo_children():
            widget.destroy()
        self.b_blind_list.clear()
        for widget in self.b_blind_column.winfo_children():
            widget.destroy()
        self.time_list.clear()
        for (index, round) in enumerate(self.rounds):
            tk.Label(self.round_column, text=round.num, bg="red", fg="white").pack(fill="both", expand=True)
            self.time_list.append(tk.Entry(self.time_column, width=6, bg="black", fg="white"))
            self.time_list[index].pack(fill="both", expand=True)
            self.time_list[index].insert(tk.END, round.time)
            self.s_blind_list.append(tk.Entry(self.s_blind_column, width=10, bg="red", fg="white"))
            self.s_blind_list[index].pack(fill="both", expand=True)
            self.s_blind_list[index].insert(tk.END, round.s_blind)
            self.b_blind_list.append(tk.Entry(self.b_blind_column, width=10, bg="black", fg="white"))
            self.b_blind_list[index].pack(fill="both", expand=True)  
            self.b_blind_list[index].insert(tk.END, round.b_blind)

    def export_game(self):
        documents_dir = Path.home() / "Documents"
        poker_dir = documents_dir / "PokerClock"
        poker_dir.mkdir(parents=True, exist_ok=True)

        self.save_game()

        file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialdir=poker_dir,
            title="Choose where to save the game file.",
            filetypes=(("CVS files", "*.csv"),("All files","*.*"))
        )
        
        if file:
            with open(file, "w", newline="") as f:
                for round in self.rounds:
                    f.write(f"{round.num},{round.time},{round.s_blind},{round.b_blind}\n")

    def import_game(self):
        documents_dir = Path.home() / "Documents"
        poker_dir = documents_dir / "PokerClock"
        poker_dir.mkdir(parents=True, exist_ok=True)

        file = filedialog.askopenfilename(
            initialdir=poker_dir,
            title="Select a file",
            filetypes=(("CVS files", "*.csv"),("All files","*.*"))
        )

        rounds = []

        if file:
            with open(file, "r") as f:
                for row in csv.reader(f):
                    rounds.append(Round(int(row[0]), int(row[1]), int(row[2]), int(row[3])))
        
        self.rounds = rounds
        self.refresh_editor()

    def game_overview(self):
        game_overview_window = tk.Toplevel(self.root)
        game_overview_window.title("Game Editor")
        game_overview_window.geometry("800x600")
        game_overview_window.configure(bg=self.bg_color)

        game_overview_window.columnconfigure((0, 1, 2, 3), weight=1)
        for i in range(len(self.rounds)):
            game_overview_window.rowconfigure(i, weight=1)

        round_column = tk.Frame(game_overview_window, bg="red")
        round_column.grid(row=0, column=0, rowspan=len(self.rounds), sticky='NESW')
        time_column = tk.Frame(game_overview_window, bg="black")
        time_column.grid(row=0, column=1, rowspan=len(self.rounds), sticky='NESW')
        s_blind_column = tk.Frame(game_overview_window, bg="red")
        s_blind_column.grid(row=0, column=2, rowspan=len(self.rounds), sticky='NESW')
        b_blind_column = tk.Frame(game_overview_window, bg="black")
        b_blind_column.grid(row=0, column=3, rowspan=len(self.rounds), sticky='NESW')

        tk.Label(round_column, text="Round", bg="red", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky='NSWE')
        tk.Label(time_column, text="Time", bg="black", fg="white").grid(row=0, column=1, padx=10, pady=10, sticky='NSWE')
        tk.Label(s_blind_column, text="Small Blind", bg="red", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky='NSWE')
        tk.Label(b_blind_column, text="Big Blind", bg="black", fg="white").grid(row=0, column=3, padx=10, pady=10, sticky='NSWE')

        for (index, round) in enumerate(self.rounds):
            tk.Label(round_column, text=round.num, bg="red", fg="white").grid(row=index+1, column=0, padx=10, pady=10, sticky='NSWE')
            tk.Label(time_column, text=round.time, bg="black", fg="white").grid(row=index+1, column=1, padx=10, pady=10, sticky='NSWE')
            tk.Label(s_blind_column, text=round.s_blind, bg="red", fg="white").grid(row=index+1, column=2, padx=10, pady=10, sticky='NSWE')
            tk.Label(b_blind_column, text=round.b_blind, bg="black", fg="white").grid(row=index+1, column=3, padx=10, pady=10, sticky='NSWE')

if __name__ == '__main__':
    # Fix hard coded values later
    round1 = Round(1, 30, 1000, 2000)
    round2 = Round(2, 20, 2000, 4000)
    round3 = Round(3, 20, 3000, 6000)
    round4 = Round(4, 20, 5000, 10000)
    round5 = Round(5, 20, 10000, 20000)
    round6 = Round(6, 20, 15000, 30000)
    round7 = Round(7, 20, 25000, 50000)
    round8 = Round(8, 20, 50000, 100000)
    round9 = Round(9, 20, 75000, 150000)
    round10 = Round(10, 20, 100000, 200000)
    rounds = [round1, round2, round3, round4, round5, round6, round7, round8, round9, round10]
    PokerClock(rounds)