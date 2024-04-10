import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from styles import Styles

class LikedCtgs(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.bg_color)
        self.styles = styles
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        # Back button
        back_image_path = "images/backtrack.png"
        back_image = Image.open(back_image_path).resize((48, 48))
        back_photo = ImageTk.PhotoImage(back_image)
        back_button = tk.Button(self, image=back_photo, command=self.go_back, borderwidth=0, bg=self.styles.bg_color)
        back_button.image = back_photo
        back_button.pack(side='top', anchor='nw', padx=10, pady=10)

        # Title
        title_label = tk.Label(self, text="Liked Categories", font=self.styles.large_font, bg=self.styles.bg_color)
        title_label.pack(pady=20)

        # Liked Categories Frame
        self.categories_frame = tk.Frame(self, bg=self.styles.bg_color)
        self.categories_frame.pack(fill='both', expand=True, padx=10)

        # Sample categories data
        self.liked_categories = [
            {"name": "Music", "image": "images/News1.png"},
            {"name": "Movies", "image": "images/News2.png"},
            {"name": "Sports", "image": "images/News3.png"}
        ]

        # Display liked categories
        self.display_liked_categories()

    def display_liked_categories(self):
        for category in self.liked_categories:
            self.create_category_widget(category)

    def create_category_widget(self, category):
        frame = tk.Frame(self.categories_frame, bg=self.styles.bg_color)
        frame.pack(pady=10, fill='x')

        # Category image
        img = Image.open(category["image"])
        img.thumbnail((100, 100))
        photo_img = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=photo_img, bg=self.styles.bg_color)
        img_label.image = photo_img  # Keep a reference
        img_label.pack(side='left', padx=10)

        # Category name
        name_label = tk.Label(frame, text=category["name"], font=self.styles.base_font, bg=self.styles.bg_color)
        name_label.pack(side='left', padx=10)

        # Remove button
        trash_img = Image.open("images/trash.png")
        trash_img.thumbnail((20, 20))
        trash_photo_img = ImageTk.PhotoImage(trash_img)
        remove_btn = tk.Button(frame, image=trash_photo_img, command=lambda: self.remove_category(category), bg=self.styles.bg_color, borderwidth=0)
        remove_btn.image = trash_photo_img  # Keep a reference
        remove_btn.pack(side='right', padx=10)

    def remove_category(self, category):
        # Confirm before removing the category
        if messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove {category['name']}?"):
            self.liked_categories.remove(category)
            self.refresh_categories()

    def refresh_categories(self):
        # Clear the categories frame and re-display the remaining categories
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        self.display_liked_categories()

    def go_back(self):
        self.controller.switch_frame('MemberPage')

if __name__ == "__main__":
    root = tk.Tk()
    styles = Styles()
    liked_ctgs = LikedCtgs(root, styles, None)
    liked_ctgs.pack(fill='both', expand=True)
    root.mainloop()
