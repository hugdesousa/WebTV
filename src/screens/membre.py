import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from styles import Styles
import os

class MemberPage(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.bg_color)
        self.styles = styles
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.create_header()
        separator = tk.Frame(self, height=40, bg=self.styles.bg_color)
        separator.pack(fill='x')
        self.create_body()

    def create_header(self):
        self.header = tk.Frame(self, bg=self.styles.bg_color)
        self.header.pack(fill='x')

        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_columnconfigure(4, weight=1)

        self.create_menu_icon(self.header)
        self.create_logo(self.header)
        self.create_search_bar(self.header)
        self.create_user_icon(self.header)

    def create_menu_icon(self, header):
        menu_icon_path = self.styles.resource_path("images/3features.png")
        menu_icon_img = Image.open(menu_icon_path).resize((48, 48))
        menu_icon = ImageTk.PhotoImage(menu_icon_img)
        menu_icon_label = tk.Label(header, image=menu_icon, bg=self.styles.bg_color)
        menu_icon_label.image = menu_icon
        menu_icon_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    def create_logo(self, header):
        logo_path = self.styles.resource_path("images/WebTV.png")
        logo_img = Image.open(logo_path).resize((100, 50))
        logo = ImageTk.PhotoImage(logo_img)
        logo_button = tk.Button(header, image=logo, bg=self.styles.bg_color, command=self.home)
        logo_button.image = logo
        logo_button.grid(row=0, column=1, sticky='nsew')

    def create_search_bar(self, header):
        search_frame, search_bar = self.styles.create_rounded_entry(header, **self.styles.search_bar_style)
        search_frame.grid(row=0, column=3, padx=(0, 10), pady=10, sticky='e')

        def on_focus_in(event):
            if search_bar.get() == "Rechercher":
                search_bar.delete(0, tk.END)

        def on_focus_out(event):
            if not search_bar.get():
                search_bar.insert(0, "Rechercher")

        search_bar.bind("<FocusIn>", on_focus_in)
        search_bar.bind("<FocusOut>", on_focus_out)

        search_icon_path = self.styles.resource_path("images/search.png")
        search_icon_img = Image.open(search_icon_path).resize((20, 20))
        search_icon = ImageTk.PhotoImage(search_icon_img)
        search_icon_button = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=lambda: print("Search:", search_bar.get()))
        search_icon_button.image = search_icon
        search_icon_button.grid(row=0, column=1, padx=5)

        clear_icon_path = self.styles.resource_path("images/largex.png")
        clear_icon_img = Image.open(clear_icon_path).resize((20, 20))
        clear_icon = ImageTk.PhotoImage(clear_icon_img)
        clear_button = tk.Button(search_frame, image=clear_icon, bg="white", bd=0, command=lambda: search_bar.delete(0, tk.END))
        clear_button.image = clear_icon
        clear_button.grid(row=0, column=2)

        search_bar.insert(0, "Rechercher")

    def create_user_icon(self, header):
        user_icon_path = os.path.join("images", "account.png")
        user_icon_img = Image.open(user_icon_path).resize((48, 48))
        user_icon = ImageTk.PhotoImage(user_icon_img)
        user_icon_label = tk.Label(header, image=user_icon, bg=self.styles.bg_color)
        user_icon_label.image = user_icon
        user_icon_label.grid(row=0, column=5, padx=10, pady=10, sticky='e')

        self.user_menu = tk.Menu(header, tearoff=0)
        self.user_menu.add_command(label="Logout", command=self.logout)

        user_icon_label.bind("<Button-1>", self.show_user_menu)

    def show_user_menu(self, event):
        self.user_menu.post(event.x_root, event.y_root)

    def home(self):
        self.controller.switch_frame('HomePage')

    def logout(self):
        self.controller.set_logging_state(False)
        self.controller.switch_frame('HomePage')

    def create_body(self):
        body_frame = tk.Frame(self, bg=self.styles.bg_color)
        body_frame.pack(fill='both', expand=True)

        member_label = tk.Label(body_frame, text="Membre", font=self.styles.large_font)
        member_label.pack(pady=(20, 10))

        self.create_profile_section(body_frame)
        self.create_management_buttons(body_frame)

    def create_profile_section(self, parent):
        profile_frame = tk.Frame(parent, bg=self.styles.bg_color)
        profile_frame.pack()

        image_path = self.styles.resource_path('images/account.png')
        img = Image.open(image_path)
        img.thumbnail((100, 100))
        photo_img = ImageTk.PhotoImage(img)
        profile_label = tk.Label(profile_frame, image=photo_img, bg=self.styles.bg_color)
        profile_label.image = photo_img
        profile_label.pack(pady=10)

    def create_management_buttons(self, parent):
        buttons_frame = tk.Frame(parent, bg=self.styles.bg_color)
        buttons_frame.pack()

        btn_gerer_membre = ttk.Button(buttons_frame, text="Modifier son profil", style='TButton', command=lambda: self.controller.switch_frame('InfoProfile'))
        btn_gerer_membre.pack(fill='x', padx=50, pady=5)

        btn_gerer_fichier = ttk.Button(buttons_frame, text="Modifier ses catégories", style='TButton',command=lambda: self.controller.switch_frame('LikedCtgs'))
        btn_gerer_fichier.pack(fill='x', padx=50, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Member Page")
    styles = Styles()
    member_page = MemberPage(root, styles, None)
    member_page.pack(fill='both', expand=True)
    root.geometry('800x600')
    root.mainloop()



