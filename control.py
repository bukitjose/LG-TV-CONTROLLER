import pywebostv.discovery
from pywebostv.connection import WebOSClient
import tkinter as tk

class TVControlApp:
    def __init__(self, master):
        self.master = master
        master.title("TV Control App")
        self.tv_listbox = tk.Listbox(master, width=50)
        self.tv_listbox.grid(row=0, column=0)
        self.refresh_button = tk.Button(master, text="Refresh", command=self.update_tv_list)
        self.refresh_button.grid(row=1, column=0)
        self.connect_button = tk.Button(master, text="Connect", state="disabled", command=self.connect_to_tv)
        self.connect_button.grid(row=2, column=0)

    def update_tv_list(self):
        self.tv_listbox.delete(0, tk.END)
        tv_list = pywebostv.discovery.discover("lg")
        for tv in tv_list:
            self.tv_listbox.insert(tk.END, tv.name)

    def connect_to_tv(self):
        selected_tv = self.tv_listbox.get(tk.ACTIVE)
        tv_list = pywebostv.discovery.discover("lg")
        for tv in tv_list:
            if tv.name == selected_tv:
                conn = WebOSClient(tv.host)
                conn.connect()

                # Create a layout for the remote control
                layout = tk.Frame(self.master)
                layout.grid(row=0, column=1, rowspan=3)

                # Create the remote control buttons
                left_button = tk.Button(layout, text='◀', command=lambda: conn.click_button('LEFT'))
                left_button.grid(row=1, column=0)
                ok_button = tk.Button(layout, text='OK', command=lambda: conn.click_button('ENTER'))
                ok_button.grid(row=2, column=1)
                up_button = tk.Button(layout, text='▲', command=lambda: conn.click_button('UP'))
                up_button.grid(row=0, column=1)
                down_button = tk.Button(layout, text='▼', command=lambda: conn.click_button('DOWN'))
                down_button.grid(row=2, column=1)
                right_button = tk.Button(layout, text='▶', command=lambda: conn.click_button('RIGHT'))
                right_button.grid(row=1, column=2)
                mute_button = tk.Button(layout, text='Mute', command=lambda: conn.set_mute(True))
                mute_button.grid(row=1, column=1)

    def enable_connect_button(self, *args):
        if self.tv_listbox.curselection():
            self.connect_button['state'] = "normal"
        else:
            self.connect_button['state'] = "disabled"


root = tk.Tk()
app = TVControlApp(root)
root.bind('<<ListboxSelect>>', app.enable_connect_button)
root.mainloop()
