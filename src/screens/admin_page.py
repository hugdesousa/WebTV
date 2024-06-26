import tkinter as tk
from tkinter import ttk, scrolledtext

import pyodbc
from PIL import Image, ImageTk
from styles import Styles
import os


class AdminPage(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.base_style['bg'])
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
        logo_button.grid(row=0, column=1)


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

        # Icons
        search_icon_path = self.styles.resource_path("images/search.png")
        search_icon_img = Image.open(search_icon_path).resize((20, 20))
        search_icon = ImageTk.PhotoImage(search_icon_img)
        search_icon_button = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=lambda: print("Search:", search_bar.get()))
        search_icon_button.image = search_icon
        search_icon_button.grid(row=0, column=1, padx=5)

        # Clear button
        clear_icon_path = self.styles.resource_path("images/largex.png")
        clear_icon_img = Image.open(clear_icon_path).resize((20, 20))
        clear_icon = ImageTk.PhotoImage(clear_icon_img)
        clear_button = tk.Button(search_frame, image=clear_icon, bg="white", bd=0, command=lambda: search_bar.delete(0, tk.END))
        clear_button.image = clear_icon
        clear_button.grid(row=0, column=2)

        # Initialize with placeholder text
        search_bar.insert(0, "Rechercher")

    def create_user_icon(self, header):
        user_icon_path = os.path.join("images", "account.png")
        user_icon_img = Image.open(user_icon_path).resize((48, 48))
        user_icon = ImageTk.PhotoImage(user_icon_img)
        user_icon_label = tk.Label(header, image=user_icon, bg=self.styles.bg_color)
        user_icon_label.image = user_icon
        user_icon_label.grid(row=0, column=5, padx=10, pady=10,sticky='e')

        # Create a dropdown menu for the user icon
        self.user_menu = tk.Menu(header, tearoff=0)
        self.user_menu.add_command(label="Profile", command=self.open_profile)
        self.user_menu.add_command(label="Logout", command=self.logout)

        # Bind the click event to show the menu
        user_icon_label.bind("<Button-1>", self.show_user_menu)

    def show_user_menu(self, event):
        # Post the menu at the position of the event (click position)
        self.user_menu.post(event.x_root, event.y_root)

    def open_profile(self):
        self.controller.switch_frame('MemberPage')    # You can add more functionality as needed to open the profile page

    def logout(self):
        self.controller.set_logging_state(False)
        self.controller.switch_frame('HomePage')

    def home(self):
        self.controller.switch_frame('HomePage')    # You can add more functionality as needed to open the profile page

    def create_body(self):
        # Main body frame
        body_frame = tk.Frame(self, bg=self.styles.bg_color)
        body_frame.pack(fill='both', expand=True)

        # Admin Label
        admin_label = tk.Label(body_frame, text="Administrateur",
                               font=(self.styles.font_family, 18, 'bold'),
                               bg='white', fg='black')

        admin_label.pack(pady=(20, 10))

        # Profile Section
        self.create_profile_section(body_frame)

        # Management Buttons
        self.create_management_buttons(body_frame)

    def create_profile_section(self, parent):
        # Profile picture and Admin label
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
        # Buttons for managing the admin tasks
        buttons_frame = tk.Frame(parent, bg=self.styles.bg_color)
        buttons_frame.pack()

        # Button Gérer Membre
        btn_gerer_membre = ttk.Button(buttons_frame, text="Gérer Membre", style='TButton', command=self.show_member_query_results)
        btn_gerer_membre.pack(fill='x', padx=50, pady=5)

        # Button Gérer Thème
        btn_gerer_theme = ttk.Button(buttons_frame, text="Gérer Thème", style='TButton',  command=self.show_file_query_results)
        btn_gerer_theme.pack(fill='x', padx=50, pady=5)

    def show_member_query_results(self):
        self._results_window("SELECT * FROM Membre")

    def show_file_query_results(self):
        self._results_window("""
            SELECT 
            T.Nom AS Nom_Theme,
            COUNT(F.ThemeID) AS Nombre_Fichiers_Associés
            FROM 
            Theme T
            LEFT JOIN 
            Fichier F ON T.ThemeID = F.ThemeID
            GROUP BY 
             T.Nom
            ORDER BY 
            Nombre_Fichiers_Associés DESC;
            """)

    def _results_window(self, query):
         # Create a new window for displaying query results
        results_window = tk.Toplevel(self)
        results_window.title("Résultats de la requête")

            # Define a scrolled text widget to display the results
        text_area = scrolledtext.ScrolledText(results_window, width=60, height=20, wrap=tk.WORD)
        text_area.pack(padx=10, pady=10)

        try:
            server = 'localhost'
            database = 'LDDProject'
            username = 'SA'
            password = 'Password123'

            # Create connection string with Windows Authentication
            conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

            # Establish connection
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # Execute the SQL query
            cursor.execute(query)

            # Fetch the query results
            results = cursor.fetchall()

            # Close the database connection
            conn.close()

            # Display the results in the text area
            for row in results:
                text_area.insert(tk.END, f"{row}\n")

        except Exception as e:
            print("Erreur lors de l'exécution de la requête:", e)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Administration")
    styles = Styles()
    admin_page = AdminPage(root, styles, controller=None)
    admin_page.pack(fill='both', expand=True)
    root.mainloop()
