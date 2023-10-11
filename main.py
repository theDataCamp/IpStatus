import socket
import requests
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
import threading


class NetworkInfo:
    @staticmethod
    def get_ip_address():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except Exception as e:
            return "Error getting IP: {}".format(str(e))

    @staticmethod
    def is_internet_connected():
        try:
            response = requests.get('https://www.google.com/', timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    @staticmethod
    def update_info(gui_instance, interval=10):
        while True:
            gui_instance.update_ip_address()
            gui_instance.update_internet_status()
            time.sleep(interval)  # Update every `interval` seconds


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('IP Status')

        # Set window size to display the app title
        self.root.geometry('230x75')

        self.network_info = NetworkInfo()

        # Set configurable dot size ratio (dot size in relation to the font size)
        # e.g. 0.5 means the dot size is half of the font size
        self.dot_size_ratio = 1.0

        self.build_gui()

        # Kick off the update thread
        self.update_thread = threading.Thread(target=NetworkInfo.update_info, args=(self,))
        self.update_thread.setDaemon(True)
        self.update_thread.start()

    def build_gui(self):
        frame = ttk.Frame(self.root, padding='10')
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set default font
        self.font = font.nametofont("TkDefaultFont")
        self.font.config(size=12)
        self.font.config(weight="bold")

        ip_label = ttk.Label(frame, text="IP Address:", font=self.font)
        ip_label.grid(column=0, row=1, sticky=tk.W)

        ip_value = ttk.Label(frame, text=self.network_info.get_ip_address(), font=self.font)
        ip_value.grid(column=1, row=1, sticky=tk.W)

        status_label = ttk.Label(frame, text="Internet Status:", font=self.font)
        status_label.grid(column=0, row=2, sticky=tk.W)

        self.canvas_size = 20
        self.status_canvas = tk.Canvas(frame, width=self.canvas_size, height=self.canvas_size)
        self.update_internet_status()
        self.status_canvas.grid(column=1, row=2, sticky=tk.W)

        self.ip_label = ip_label
        self.ip_value = ip_value
        self.status_label = status_label

    def update_ip_address(self):
        new_ip_address = self.network_info.get_ip_address()
        self.ip_value.config(text=new_ip_address)

    def update_internet_status(self):
        status_color = 'green' if self.network_info.is_internet_connected() else 'red'
        self.status_canvas.delete("all")

        # Calculate the new status dot size based on the current font size and dot_size_ratio
        dot_size = int(self.font.actual()['size'] * self.dot_size_ratio)
        padding = (self.canvas_size - dot_size) // 2
        self.status_canvas.create_oval(padding, padding, padding + dot_size, padding + dot_size, fill=status_color, outline=status_color)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()