import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from styles import Styles

class MemberPage(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent)
        self.controller = controller
        self.styles = styles
        # Images must be kept in variables to maintain a reference
        self.images = {}
        self.create_widgets()

    def create_widgets(self):
        self.configure(bg=self.styles.bg_color)
        
        # Header Frame with logo and backtrack button
        self.header_frame = tk.Frame(self, bg=self.styles.bg_color)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

        # Backtrack button
        self.images['backtrack'] = self.create_photo_image('images/backtrack.png', (30, 30))
        back_button = tk.Button(self.header_frame, image=self.images['backtrack'], command=self.go_back, bg=self.styles.bg_color)
        back_button.grid(row=0, column=0, padx=10, pady=10)

        # Profile section
        self.profile_section_frame = tk.Frame(self, bg=self.styles.bg_color)
        self.profile_section_frame.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)

        # Categories section
        self.categories_section_frame = tk.Frame(self, bg=self.styles.bg_color)
        self.categories_section_frame.grid(row=2, column=1, sticky='nsew', padx=20, pady=(0,20))

        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add widgets to the profile section frame
        self.create_profile_section(self.profile_section_frame)

        # Add widgets to the categories section frame
        self.create_categories_section(self.categories_section_frame)

    def create_profile_section(self, frame):
        # Profile picture
        self.images['user'] = self.create_photo_image('images/user.png', (100, 100))
        profile_pic_label = tk.Label(frame, image=self.images['user'], bg=self.styles.bg_color)
        profile_pic_label.grid(row=0, column=0, rowspan=3, padx=(0, 20))

        # Username and info
        username_label = tk.Label(frame, text="CATINA.B", font=self.styles.large_font, bg=self.styles.bg_color)
        username_label.grid(row=0, column=1, sticky="w")

        username_info = tk.Label(frame, text="Username: Catina.b", bg=self.styles.bg_color)
        username_info.grid(row=1, column=1, sticky="w")

        # Edit profile button
        edit_profile_btn = tk.Button(frame, text="Modifier mon profile", bg="white", fg="black", command=self.go_infoprofile)
        edit_profile_btn.grid(row=2, column=1, sticky="w", pady=(10, 0))

        # Edit favorites button
        edit_favorites_btn = tk.Button(frame, text="Modifier mes categories favoris", bg="white", fg="black")
        edit_favorites_btn.grid(row=3, column=1, sticky="w", pady=10)

    def create_categories_section(self, frame):
        categories_label = tk.Label(frame, text="Categories Favoris", font=self.styles.large_font, bg=self.styles.bg_color)
        categories_label.grid(row=0, column=0, sticky="w")

        # Example category buttons (create as needed)
        for i in range(4):  # Assuming there are 4 categories
            btn = tk.Button(frame, text=f"Cat {i+1}", bg="white", fg="black")
            btn.grid(row=1, column=i, pady=10)

    def create_photo_image(self, file_path, size):
        img = Image.open(file_path).resize(size)
        photo = ImageTk.PhotoImage(img)
        return photo

    def go_back(self):
        if self.controller:
            self.controller.switch_frame("HomePage")
    def go_infoprofile(self):
        if self.controller:
            self.controller.switch_frame("InfoProfile")

# Usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Member Page")
    styles = Styles()
    member_page = MemberPage(root, styles, None)  # Assume 'None' is the controller for this example
    member_page.pack(fill='both', expand=True)
    root.geometry('800x600')  # Set the window size to be large enough
    root.mainloop()

