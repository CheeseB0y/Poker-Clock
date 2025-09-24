import tkinter as tk
import time
import math

class PokerClock:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Poker Clock")
        self.root.geometry("1200x900")
        self.timer_set = 10
        self.time_remaining = self.timer_set * 60
        self.time_display = tk.StringVar()
        self.timer_label = tk.Label(self.root, textvariable=self.time_display)
        self.timer_label.pack()
        self.button = tk.Button(self.root, text="Start timer", command=self.start_timer)
        self.button.pack()

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
            print(f"{math.floor(mins)}:{secs}")
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)
        else:
            self.time_display.set("0:00")

if __name__ == '__main__':
    PokerClock()