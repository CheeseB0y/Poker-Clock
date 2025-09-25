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

        self.root.title("Poker Clock")
        self.root.geometry("1200x900")

        self.round_index = 0
        self.round_num = tk.StringVar(value=f"Round: {rounds[self.round_index].num}")
        self.b_blind = tk.StringVar(value=f"Big Blind: {rounds[self.round_index].b_blind}")
        self.s_blind = tk.StringVar(value=f"Small Blind: {rounds[self.round_index].s_blind}")

        self.timer_set = rounds[self.round_index].time
        self.time_remaining = self.timer_set * 60
        self.time_display = tk.StringVar(value=f"{self.timer_set}:00")

        self.round_number_label = tk.Label(self.root, textvariable=self.round_num)
        self.round_number_label.pack(padx=10, pady=10)

        self.timer_label = tk.Label(self.root, textvariable=self.time_display)
        self.timer_label.pack(padx=10, pady=10)

        self.timer_button = tk.Button(self.root, text="Start timer", command=self.start_timer)
        self.timer_button.pack(padx=10, pady=10)

        self.s_blind_label = tk.Label(self.root, textvariable=self.s_blind)
        self.s_blind_label.pack(padx=10, pady=10)

        self.b_blind_label = tk.Label(self.root, textvariable=self.b_blind)
        self.b_blind_label.pack(padx=10, pady=10)

        self.next_button = tk.Button(self.root, text="Next round", command=self.next_round)
        self.next_button.pack(padx=10, pady=10)

        self.root.mainloop()

    def start_timer(self):
        self.countdown()

    def countdown(self):
        if self.time_remaining > 0:
            mins = self.time_remaining / 60
            secs = self.time_remaining % 60
            if secs < 10:
                secs = "0" + str(secs)
            self.time_display.set(f"{math.floor(mins)}:{secs}")
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)
        else:
            self.time_display.set("0:00")
            self.flash_screen()
    
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
        self.timer_set = rounds[self.round_index].time
        self.time_remaining = self.timer_set * 60
        self.time_display.set(value=f"{self.timer_set}:00")
        self.round_num.set(f"Round: {rounds[self.round_index].num}")
        self.b_blind.set(f"Big Blind: {rounds[self.round_index].b_blind}")
        self.s_blind.set(f"Small Blind: {rounds[self.round_index].s_blind}")

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