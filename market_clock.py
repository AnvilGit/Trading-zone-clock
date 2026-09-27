import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo


class MarketClock:
    MARKETS = (
        ("TOKYO", "JAPAN", "Asia/Tokyo", "#F2B84B"),
        ("LONDON", "UNITED KINGDOM", "Europe/London", "#61D6B2"),
        ("NEW YORK", "UNITED STATES", "America/New_York", "#F08070"),
    )
    BACKGROUND = "#111815"
    PANEL = "#19231F"
    MUTED = "#91A098"
    TEXT = "#F3F5F2"

    def __init__(self, root):
        self.root = root
        self.root.title("World Trading Clocks")
        self.root.geometry("1240x560")
        self.root.minsize(860, 440)
        self.root.configure(bg=self.BACKGROUND)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        container = tk.Frame(root, bg=self.BACKGROUND, padx=32, pady=28)
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        header = tk.Frame(container, bg=self.BACKGROUND)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 26))
        tk.Label(
            header,
            text="WORLD CLOCKS",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="TRADING DESK  /  LOCAL MARKET TIMES",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="right", pady=(6, 0))

        clocks = tk.Frame(container, bg=self.BACKGROUND)
        clocks.grid(row=1, column=0, sticky="nsew")
        for column in range(len(self.MARKETS)):
            clocks.grid_columnconfigure(column, weight=1, uniform="market")

        self.clock_labels = []
        self.date_labels = []
        self.zone_labels = []
        for column, (city, country, zone_name, accent) in enumerate(self.MARKETS):
            panel = tk.Frame(
                clocks,
                bg=self.PANEL,
                highlightbackground="#2B3932",
                highlightthickness=1,
            )
            panel.grid(row=0, column=column, sticky="nsew", padx=7)
            panel.grid_columnconfigure(0, weight=1)
            panel.grid_rowconfigure(3, weight=1)

            tk.Frame(panel, bg=accent, height=4).grid(
                row=0, column=0, sticky="ew"
            )
            tk.Label(
                panel,
                text=city,
                bg=self.PANEL,
                fg=accent,
                font=("Segoe UI", 12, "bold"),
                anchor="w",
            ).grid(row=1, column=0, sticky="ew", padx=22, pady=(25, 3))
            zone_label = tk.Label(
                panel,
                text=country,
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            )
            zone_label.grid(row=2, column=0, sticky="ew", padx=22)
            self.zone_labels.append((zone_label, ZoneInfo(zone_name)))

            clock_label = tk.Label(
                panel,
                text="00:00:00",
                bg=self.PANEL,
                fg=self.TEXT,
                font=("Segoe UI", 52, "bold"),
                anchor="center",
            )
            clock_label.grid(row=3, column=0, sticky="nsew", padx=8)
            panel.bind(
                "<Configure>",
                lambda event, label=clock_label: self.resize_clock(event, label),
            )
            self.clock_labels.append(clock_label)

            date_label = tk.Label(
                panel,
                text="",
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 11),
                anchor="center",
            )
            date_label.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 27))
            self.date_labels.append(date_label)

        footer = tk.Label(
            container,
            text="24-HOUR TIME     F11 FULLSCREEN     ESC EXIT FULLSCREEN",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
        )
        footer.grid(row=2, column=0, sticky="ew", pady=(20, 0))

        self.update_clocks()

    @staticmethod
    def resize_clock(event, label):
        if event.width > 1:
            size = max(32, min(68, int((event.width - 36) / 6.1)))
            label.configure(font=("Segoe UI", size, "bold"))

    def update_clocks(self):
        for (zone_label, zone), clock_label, date_label in zip(
            self.zone_labels, self.clock_labels, self.date_labels
        ):
            local_time = datetime.now(zone)
            clock_label.configure(text=local_time.strftime("%H:%M:%S"))
            date_label.configure(
                text=f"{local_time.strftime('%A, %B')} {local_time.day}"
                f"    {local_time.tzname()}"
            )
        self.root.after(250, self.update_clocks)

    def toggle_fullscreen(self, _event=None):
        is_fullscreen = bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", not is_fullscreen)

    def exit_fullscreen(self, _event=None):
        self.root.attributes("-fullscreen", False)


def main():
    root = tk.Tk()
    MarketClock(root)
    root.mainloop()


if __name__ == "__main__":
    main()
