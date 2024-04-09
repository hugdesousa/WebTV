import tkinter as tk
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
            # If logged in, create the user icon if it doesn't already exist
            if not hasattr(self, 'user_icon_label'):
                self.create_user_icon(self.header)
                self.header.grid_columnconfigure(len(self.header.grid_slaves(row=0)), weight=1)
                self.header.grid(row=0, column=len(self.header.grid_slaves(row=0)) - 1, sticky='e')
        else:
            # If not logged in, destroy the user icon if it exists
            if hasattr(self, 'user_icon_label'):
                self.user_icon_label.destroy()
                delattr(self, 'user_icon_label')

    def create_content_area(self):
        # Create the Canvas and add the Scrollbar
        self.main_content = tk.Canvas(self, bg=self.styles.bg_color, highlightthickness=0)
        self.main_content.grid(row=1, column=0, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a Scrollbar and attach it to the Canvas
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.main_content.yview)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.main_content.configure(yscrollcommand=self.scrollbar.set)

        # Create a Frame inside the Canvas which will be scrolled with it
        self.content_frame = tk.Frame(self.main_content, bg=self.styles.bg_color)
        self.canvas_frame = self.main_content.create_window((0, 0), window=self.content_frame, anchor='nw')

        # Configure the Canvas to update the scrolling region when the size of the Frame changes
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.main_content.bind('<Configure>', self.on_canvas_resize)

    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.main_content.configure(scrollregion=self.main_content.bbox('all'))

    def on_canvas_resize(self, event):
        # Resize the inner frame's width to the canvas width
        self.main_content.itemconfig(self.canvas_frame, width=event.width)
        # Adjust the canvas window to the new width
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
        # Create the rounded entry and add it to the header
        search_frame, search_bar = self.styles.create_rounded_entry(header, **self.styles.search_bar_style)
        search_frame.grid(row=0, column=3, padx=(0, 10), pady=10, sticky='e')

        # Bind focus in and focus out for placeholder functionality
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


    def create_buttons_frame(self, header):
        buttons_frame = tk.Frame(header, bg=self.styles.bg_color)
        buttons_frame.grid(row=0, column=4, padx=(0, 10), pady=10, sticky='e')

        # Only show the buttons if the user is not logged in
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

        # Create a dropdown menu for the user icon
        self.user_menu = tk.Menu(header, tearoff=0)
        self.user_menu.add_command(label="Profile", command=self.open_profile)
        self.user_menu.add_command(label="Logout", command=self.logout)

        # Bind the click event to show the menu
        user_icon_label.bind("<Button-1>", self.show_user_menu)

    def show_user_menu(self, event):
        self.user_menu.post(event.x_root, event.y_root)

    def open_profile(self):
        print("Open user profile")

    def logout(self):
        print("Logout user")

    def load_thumbnails(self):
        thumbnails = []
        image_names = ["KattyPerry.png", "Rihana.png", "Beyonce.png", "JustinBieber.png",
                    "Chien.png", "Bebe.png", "Laugh.png", "fails1.png",
                    "News1.png", "News2.png", "News3.png", "News4.png"]
        for name in image_names:
            path = os.path.join("images", name)
            # Modify the resize dimensions to make thumbnails bigger
            image = Image.open(path).resize((150, 100))  # Example size; adjust as needed
            photo = ImageTk.PhotoImage(image)
            thumbnails.append(photo)
        return thumbnails

    def show_side_menu(self, event):
        self.side_menu.post(event.x_root, event.y_root)

    def feature1(self):
        print("Feature 1")

    def feature2(self):
        print("Feature 2")

    def feature3(self):
        print("Feature 3")

    def add_category(self, content_frame, category_name, thumbnails, start_row):
        category_frame = tk.Frame(content_frame, bg="white")
        category_frame.grid(row=start_row, column=0, sticky='nsew', padx=10, pady=10)
        category_frame.grid_columnconfigure(0, weight=0)

        # Add the category title label.
        tk.Label(category_frame, text=category_name, **self.styles.base_style).grid(row=0, column=1, sticky='w', padx=10)

        # Define the number of thumbnails per row.
        thumbnails_per_row = 4
        thumb_row = 1  # Initialize the thumbnail row.
        for i, thumb in enumerate(thumbnails):
            col = i % thumbnails_per_row
            if col == 0 and i != 0:  # Start a new row after 'thumbnails_per_row' thumbnails.
                thumb_row += 2

            # Container frame for each thumbnail and its title.
            video_frame = tk.Frame(category_frame, bg="white")
            video_frame.grid(row=thumb_row, column=col + 1, sticky='nsew', padx=10, pady=2)
            category_frame.grid_columnconfigure(col + 1, weight=1)

            # Thumnail
            thumb_label = tk.Label(video_frame, image=thumb, bg='white')
            thumb_label.image = thumb  # Keep a reference.
            thumb_label.pack()

            # Bind the enter event to show the overlay and play button
            thumb_label.bind("<Enter>", lambda e, thumb_label=thumb_label: self.show_overlay(thumb_label))

            # Bind the leave event to remove the overlay and play button
            thumb_label.bind("<Leave>", lambda e, thumb_label=thumb_label: self.hide_overlay(thumb_label))

            # Title
            video_title = f"Video {i+1}"  # Example title.
            title_label = tk.Label(video_frame, text=video_title, **self.styles.base_style)
            title_label.pack()

            # Creator
            video_creator = f"Artiste {i+1}"  # Example creator.
            video_label = tk.Label(video_frame, text=video_creator, **self.styles.base_style)
            video_label.pack()

    def show_overlay(self, thumb_label, thumbnail_image_path):
        # Open the original thumbnail image
        thumbnail = Image.open(thumbnail_image_path)
        
        # Apply a blur filter to the image
        blurred_thumbnail = thumbnail.filter(ImageFilter.GaussianBlur(radius=5))

        # Convert the blurred image to a format that Tkinter can use
        blurred_photo = ImageTk.PhotoImage(blurred_thumbnail)

        # Set the blurred image on the thumbnail label
        thumb_label.configure(image=blurred_photo)
        thumb_label.image = blurred_photo  # Keep a reference!

        # Assuming 'play.png' is a 48x48 icon with a transparent background
        play_image_path = "images/play.png"
        play_image = Image.open(play_image_path).resize((48, 48))
        play_photo = ImageTk.PhotoImage(play_image)

        # Create a label with the play image and a transparent background
        play_button = tk.Label(thumb_label, image=play_photo, borderwidth=0, bg='')
        play_button.image = play_photo  # Keep a reference!
        play_button.place(relx=0.5, rely=0.5, anchor='center')

        # Bind the click event to the function that will open the video page
        play_button.bind("<Button-1>", lambda e: self.open_video_page())

    def hide_overlay(self, thumb_label, original_thumbnail_path):
        # Restore the original thumbnail image when the mouse leaves
        original_thumbnail = Image.open(original_thumbnail_path)
        original_photo = ImageTk.PhotoImage(original_thumbnail)
        thumb_label.configure(image=original_photo)
        thumb_label.image = original_photo  # Keep a reference!
        # Remove the play button
        for widget in thumb_label.winfo_children():
            widget.destroy()

    def open_video_page(self):
    # Implement the function that redirects to the video page
        print("This will redirect to the video page")

    def populate_categories(self):
        # Set the weight for each category row to be expandable
        for i in range(len(self.categories) * 2):
            self.content_frame.grid_rowconfigure(i, weight=1)
        for i, category in enumerate(self.categories):
            start_index = i * 4
            end_index = start_index + 4
            self.add_category(self.content_frame, category, self.thumbnails[start_index:end_index], i * 2)

    def on_resize(self, event):
        # Call the on_canvas_resize method to update canvas and scrollbar
        self.on_canvas_resize(event)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("WebTV")
    styles = Styles()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Calculate window size
    window_width = screen_width // 2  # Half the screen width
    window_height = screen_height // 2  # Half the screen height

    # Set the initial size of the window to be half the size of the screen
    root.geometry(f'{window_width}x{window_height}')
    
    app = HomePage(root, styles, controller=None)
    app.pack(fill='both', expand=True)
    root.mainloop()
