import tkinter as tk
from tkinter import messagebox

import pyodbc
from PIL import Image, ImageTk, ImageFilter
from styles import Styles
import os

class HomePage(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.base_style['bg'])
        self.styles = styles
        self.controller = controller
        self.categories = ["Music", "Funny videos", "News"]
        self.thumbnails = self.load_thumbnails()
        self.build_ui()

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_header()
        self.create_content_area()
        self.populate_categories()

    def create_header(self):
        self.header = tk.Frame(self, bg=self.styles.bg_color)
        self.header.grid(row=0, column=0, sticky='ew')
        self.header.grid_columnconfigure(1, weight=1)

        self.create_menu_icon(self.header)
        self.create_logo(self.header)
        self.create_search_bar(self.header)
        self.create_buttons_frame(self.header)
        # Conditionally create the user icon based on login state
        if self.controller.user_logged_in:
            self.create_user_icon(self.header)

    def update_user_icon(self):
        if self.controller.user_logged_in:
            if not hasattr(self, 'user_icon_label'):
                self.create_user_icon(self.header)
                self.header.grid_columnconfigure(len(self.header.grid_slaves(row=0)), weight=1)
                self.header.grid(row=0, column=len(self.header.grid_slaves(row=0)) - 1, sticky='e')
        else:
            if hasattr(self, 'user_icon_label'):
                self.user_icon_label.destroy()
                delattr(self, 'user_icon_label')

    def create_content_area(self):
        self.main_content = tk.Canvas(self, bg=self.styles.bg_color, highlightthickness=0)
        self.main_content.grid(row=1, column=0, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.main_content.yview)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.main_content.configure(yscrollcommand=self.scrollbar.set)

        self.content_frame = tk.Frame(self.main_content, bg=self.styles.bg_color)
        self.canvas_frame = self.main_content.create_window((0, 0), window=self.content_frame, anchor='nw')

        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.main_content.bind('<Configure>', self.on_canvas_resize)

    def on_frame_configure(self, event):
        self.main_content.configure(scrollregion=self.main_content.bbox('all'))

    def on_canvas_resize(self, event):
        self.main_content.itemconfig(self.canvas_frame, width=event.width)
        self.main_content.itemconfig(self.canvas_frame, width=self.main_content.winfo_width())

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
        logo_label = tk.Label(header, image=logo, bg=self.styles.bg_color)
        logo_label.image = logo
        logo_label.grid(row=0, column=1)

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
        search_icon_button = tk.Button(search_frame, image=search_icon, bg="white", bd=0, command=self.execute_search)
        self.search_bar = search_bar
        search_icon_button.image = search_icon
        search_icon_button.grid(row=0, column=1, padx=5)

        clear_icon_path = self.styles.resource_path("images/largex.png")
        clear_icon_img = Image.open(clear_icon_path).resize((20, 20))
        clear_icon = ImageTk.PhotoImage(clear_icon_img)
        clear_button = tk.Button(search_frame, image=clear_icon, bg="white", bd=0, command=lambda: search_bar.delete(0, tk.END))
        clear_button.image = clear_icon
        clear_button.grid(row=0, column=2)

        search_bar.insert(0, "Rechercher")

    def execute_search(self):
        search_query = self.search_bar.get().strip()
        server = 'localhost'
        database = 'LDDProject'
        username = 'SA'
        password = 'Password123'

        # Create connection string
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        if not search_query:
            messagebox.showinfo("Search", "Veuillez entrer un terme de recherche.")
            return

        # Connect to the database and execute search query
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            # Utilisation de la nouvelle requête pour rechercher par mot-clé
            cursor.execute("""
                SELECT F.Chemin,F.Description FROM Fichier F
                JOIN MotsIndexFichier MIF ON F.Fichier_ID = MIF.Fichier_ID
                JOIN MOTCLE MK ON MIF.MotCleID = MK.MotCleID
                WHERE MK.MotCle LIKE ?
            """, ('%' + search_query + '%',))
            results = cursor.fetchall()
            self.display_search_results(results)
        except pyodbc.Error as e:
            messagebox.showerror("Erreur de base de données", str(e))
        finally:
            if conn:
                conn.close()

    def display_search_results(self, results):
        # First, clear the existing content in the content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not results:
            # If no results, display a message saying so
            no_results_label = tk.Label(self.content_frame, text="No results found.", bg=self.styles.bg_color)
            no_results_label.pack(pady=20)
            return

        # Loop through the results, which are expected to contain file paths and descriptions
        for idx, (chemin, video_description) in enumerate(results):
            # Create a frame for each result to organize its display
            result_frame = tk.Frame(self.content_frame, bg=self.styles.bg_color)
            result_frame.pack(fill='x', padx=10, pady=5)

            if os.path.isfile(chemin):
                # Load the image, resizing as needed
                image = Image.open(chemin)
                image = image.resize((150, 100))  # Resize as per your UI needs
                photo = ImageTk.PhotoImage(image)

                # Display the image in a label
                image_label = tk.Label(result_frame, image=photo, bg=self.styles.bg_color)
                image_label.image = photo  # Keep a reference
                image_label.pack(side='left', padx=10)  # Adjust layout as needed

            # Display the video description
            description_label = tk.Label(result_frame, text=f"{idx + 1}. {video_description}", bg=self.styles.bg_color,
                                         font=self.styles.small_font)
            description_label.pack(side='left', anchor='n', padx=10)  # Adjust layout as needed

            # This ensures each frame containing the result is visually separated
            tk.Frame(self.content_frame, height=2, bg="grey", bd=1).pack(fill='x', padx=5, pady=5)

    def create_buttons_frame(self, header):
        buttons_frame = tk.Frame(header, bg=self.styles.bg_color)
        buttons_frame.grid(row=0, column=4, padx=(0, 10), pady=10, sticky='e')

        if not self.controller.user_logged_in:
            btn_signup = self.styles.create_rounded_button(buttons_frame, "S'inscrire", lambda: self.controller.switch_frame('SignupPage'))
            btn_signup.grid(row=0, column=0, padx=(0, 10))

            btn_login = self.styles.create_rounded_button(buttons_frame, "Se connecter", lambda: self.controller.switch_frame('LoginPage'))
            btn_login.grid(row=0, column=1, padx=(0, 10))


    def create_user_icon(self, header):
        user_icon_path = os.path.join("images", "account.png")
        user_icon_img = Image.open(user_icon_path).resize((48, 48))
        user_icon = ImageTk.PhotoImage(user_icon_img)
        user_icon_label = tk.Label(header, image=user_icon, bg=self.styles.bg_color)
        user_icon_label.image = user_icon
        user_icon_label.grid(row=0, column=5, padx=10, pady=10,sticky='e')

        self.user_menu = tk.Menu(header, tearoff=0)
        self.user_menu.add_command(label="Profile", command=self.open_profile)
        self.user_menu.add_command(label="Administrateur", command=self.open_administrateur)
        self.user_menu.add_command(label="Logout", command=self.logout)

        user_icon_label.bind("<Button-1>", self.show_user_menu)

    def show_user_menu(self, event):
        self.user_menu.post(event.x_root, event.y_root)

    def open_profile(self):
        self.controller.switch_frame('MemberPage')
        
    def open_administrateur(self):
        print("Ouverture de la page d'administration.")
        self.controller.switch_frame('AdminPage')
        
    def logout(self):
        print("Logout user")

    def load_thumbnails(self):
        thumbnails = []
        thumbnail_paths = []

        image_names = ["KattyPerry.png", "Rihana.png", "Beyonce.png", "JustinBieber.png",
                    "Chien.png", "Bebe.png", "Laugh.png", "fails1.png",
                    "News1.png", "News2.png", "News3.png", "News4.png"]
        for name in image_names:
            path = os.path.join("images", name)
            
            image = Image.open(path).resize((150, 100))
            photo = ImageTk.PhotoImage(image)
            thumbnails.append(photo)
            thumbnail_paths.append(path)

        return thumbnails, thumbnail_paths

    def show_side_menu(self, event):
        self.side_menu.post(event.x_root, event.y_root)

    def feature1(self):
        print("Feature 1")

    def feature2(self):
        print("Feature 2")

    def feature3(self):
        print("Feature 3")

    def add_category(self, content_frame, category_name, thumbnails, thumbnail_paths, start_row):
        category_frame = tk.Frame(content_frame, bg="white")
        category_frame.grid(row=start_row, column=0, sticky='nsew', padx=10, pady=10)
        category_frame.grid_columnconfigure(0, weight=0)

        tk.Label(category_frame, text=category_name, **self.styles.base_style).grid(row=0, column=1, sticky='w', padx=10)

        thumbnails_per_row = 4
        thumb_row = 1  
        for i, (thumb, image_path) in enumerate(zip(thumbnails, thumbnail_paths)):
            col = i % thumbnails_per_row
            if col == 0 and i != 0:
                thumb_row += 2

            video_frame = tk.Frame(category_frame, bg="white")
            video_frame.grid(row=thumb_row, column=col + 1, sticky='nsew', padx=10, pady=2)
            category_frame.grid_columnconfigure(col + 1, weight=1)

            thumb_label = tk.Label(video_frame, image=thumb, bg='white', width=150, height=100)
            thumb_label.image = thumb
            thumb_label.image_path = image_path
            thumb_label.pack()

            video_path = image_path.replace('.png', '.mp4')
            thumb_label.bind("<Button-1>", lambda e, video=video_path: self.open_video_page(video))

            thumb_label.bind("<Enter>", lambda e, label=thumb_label: self.show_overlay(label))
            thumb_label.bind("<Leave>", lambda e, label=thumb_label: self.hide_overlay(label))

            video_title = f"Video {i+1}"
            title_label = tk.Label(video_frame, text=video_title, **self.styles.base_style)
            title_label.pack()

            video_creator = f"Artiste {i+1}"
            video_label = tk.Label(video_frame, text=video_creator, **self.styles.base_style)
            video_label.pack()

    def show_overlay(self, thumb_label):
        thumbnail_image_path = thumb_label.image_path
        thumbnail = Image.open(thumbnail_image_path)

        blurred_thumbnail = thumbnail.filter(ImageFilter.GaussianBlur(radius=5))
        blurred_thumbnail = blurred_thumbnail.resize((150, 100))

        blurred_photo = ImageTk.PhotoImage(blurred_thumbnail)

        thumb_label.configure(image=blurred_photo)
        thumb_label.image = blurred_photo  # Keep a reference!

        play_image_path = "images/play.png"
        play_image = Image.open(play_image_path).resize((48, 48))
        play_photo = ImageTk.PhotoImage(play_image)

        play_button = tk.Label(thumb_label, image=play_photo, borderwidth=0, bg=self.styles.bg_color)
        play_button.image = play_photo  # Keep a reference!
        play_button.place(relx=0.5, rely=0.5, anchor='center')
        
        video_path = thumbnail_image_path.replace('.png', '.mp4')
        play_button.bind("<Button-1>", lambda e, video=video_path: self.open_video_page(video))

    def hide_overlay(self, thumb_label):
        original_thumbnail_path = thumb_label.image_path
        original_thumbnail = Image.open(original_thumbnail_path)
        original_photo = ImageTk.PhotoImage(original_thumbnail)
        thumb_label.configure(image=original_photo)
        thumb_label.image = original_photo  
        thumb_label.update_idletasks() 

        for widget in thumb_label.winfo_children():
            widget.destroy()

    def open_video_page(self, video_path):
        self.controller.switch_frame('DisplayVideo')

    def populate_categories(self):
        thumbnails, thumbnail_paths = self.load_thumbnails()  
        for i, category in enumerate(self.categories):
            start_index = i * 4
            end_index = start_index + 4
            self.add_category(self.content_frame, category, thumbnails[start_index:end_index], thumbnail_paths[start_index:end_index], i * 2)
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("WebTV")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = screen_width // 2  
    window_height = screen_height // 2  

    root.geometry(f'{window_width}x{window_height}')
    
    app = HomePage(root, controller=None)
    app.pack(fill='both', expand=True)
    root.mainloop()


