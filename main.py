import tkinter as tk
import math

class Round:
    def __init__(self, num, time, s_blind, b_blind):
        self.num = num
        self.time = time
        self.s_blind = s_blind
        self.b_blind = b_blind

class PokerClock:

    def __init__(self, rounds):
        self.root = tk.Tk()
        self.rounds = rounds

        self.root.title("Poker Clock")
        self.root.geometry("1200x900")
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        option_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=option_menu)
        option_menu.add_command(label="New Game", command=self.game_editor)
        option_menu.add_command(label="Edit Game")
        option_menu.add_command(label="Exit", command=quit)

        self.round_index = 0
        self.round_num = tk.StringVar(value=f"Round: {rounds[self.round_index].num}")
        self.b_blind = tk.StringVar(value=f"Big Blind: {rounds[self.round_index].b_blind:,}")
        self.s_blind = tk.StringVar(value=f"Small Blind: {rounds[self.round_index].s_blind:,}")

        self.time_remaining = rounds[self.round_index].time * 60
        self.time_display = tk.StringVar(value=self.format_time_remaining())

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.columnconfigure(5, weight=1)

        top_menu_box = tk.Frame(self.root, bg='red')
        top_menu_box.grid(row=0, column=1, sticky='WE')
        time_frame = tk.Frame(self.root, bg='green')
        time_frame.grid(row=1, column=1, sticky='WE')

        round_number_label = tk.Label(top_menu_box, textvariable=self.round_num).grid(row=0, column=1, padx=10, pady=10, sticky='NSWE')
        timer_label = tk.Label(time_frame, textvariable=self.time_display).grid(row=1, column=1, padx=10, pady=10, sticky='NSWE')
        timer_button = tk.Button(self.root, text="Start timer", command=self.start_timer).grid(row=1, column=2, padx=10, pady=10, sticky='NSWE')
        s_blind_label = tk.Label(self.root, textvariable=self.s_blind).grid(row=2, column=1, padx=10, pady=10, sticky='NSWE')
        b_blind_label = tk.Label(self.root, textvariable=self.b_blind).grid(row=2, column=2, padx=10, pady=10, sticky='NSWE')
        next_button = tk.Button(self.root, text="Next round", command=self.next_round).grid(row=2, column=3, padx=10, pady=10, sticky='NSWE')

        self.root.mainloop()

    def start_timer(self):
        self.pause = False
        self.countdown()

    def countdown(self):
        if self.time_remaining > 0 and self.pause == False:
            self.time_display.set(self.format_time_remaining())
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)
        else:
            self.time_display.set("0:00")
            self.flash_screen()

    def format_time_remaining(self): 
        mins = self.time_remaining / 60
        secs = self.time_remaining % 60
        if secs < 10:
            secs = "0" + str(secs)
        return f"{math.floor(mins)}:{secs}"

    
    # This needs to be like this for some reason
    def flash_screen(self, duration=10, speed=500):
        if duration > 0:
            self.root.configure(bg="black")
            self.root.after(speed, lambda: self.flash_screen_2(duration, speed))
    def flash_screen_2(self, duration, speed):
            self.root.configure(bg="white")
            self.root.after(speed, lambda: self.flash_screen(duration - 1, speed))

    def next_round(self):
        self.round_index += 1
        self.time_remaining = rounds[self.round_index].time * 60
        self.time_display.set(value=self.format_time_remaining())
        self.round_num.set(f"Round: {rounds[self.round_index].num}")
        self.b_blind.set(f"Big Blind: {rounds[self.round_index].b_blind:,}")
        self.s_blind.set(f"Small Blind: {rounds[self.round_index].s_blind:,}")

    def game_editor(self):
        game_editor_window = tk.Toplevel(self.root)
        game_editor_window.title("Game Editor")
        game_editor_window.geometry("800x600")
        game_editor_window.configure(bg="green")

        game_editor_window.columnconfigure(0, weight=1)
        game_editor_window.columnconfigure(1, weight=1)
        game_editor_window.columnconfigure(2, weight=1)
        game_editor_window.columnconfigure(3, weight=1)
        game_editor_window.columnconfigure(4, weight=1)
        game_editor_window.columnconfigure(5, weight=1)

        round_column = tk.Frame(game_editor_window, bg="red", padx=10, pady=10)
        round_column.grid(row=0, column=1, sticky='NSWE')
        time_column = tk.Frame(game_editor_window, bg="black", padx=10, pady=10)
        time_column.grid(row=0, column=2, sticky='NSWE')
        b_blind_column = tk.Frame(game_editor_window, bg="red", padx=10, pady=10)
        b_blind_column.grid(row=0, column=3, sticky='NSWE')
        s_blind_column = tk.Frame(game_editor_window, bg="black", padx=10, pady=10)
        s_blind_column.grid(row=0, column=4, sticky='NSWE')

        round_column_label = tk.Label(round_column, text="Round", bg="red", fg="white").grid(row=0, column=1, padx=10, pady=10, sticky='NSWE')
        time_column_label = tk.Label(time_column, text="Time", bg="black", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky='NSWE')
        b_blind_column_label = tk.Label(b_blind_column, text="Big Blind", bg="red", fg="white").grid(row=0, column=3, padx=10, pady=10, sticky='NSWE')
        s_blind_column_label = tk.Label(s_blind_column, text="Small Blind", bg="black", fg="white").grid(row=0, column=4, padx=10, pady=10, sticky='NSWE')

        for (index, round) in enumerate(self.rounds):
            tk.Label(round_column, text=round.num, bg="red", fg="white").grid(row=index+1, column=1, padx=10, pady=10, sticky='NSWE')
            tk.Label(time_column, text=round.time, bg="black", fg="white").grid(row=index+1, column=2, padx=10, pady=10, sticky='NSWE')
            tk.Label(b_blind_column, text=round.b_blind, bg="red", fg="white").grid(row=index+1, column=3, padx=10, pady=10, sticky='NSWE')
            tk.Label(s_blind_column, text=round.s_blind, bg="black", fg="white").grid(row=index+1, column=4, padx=10, pady=10, sticky='NSWE')

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