import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from styles import Styles

class InfoProfile(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.bg_color)
        self.styles = styles
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)  # Center the form vertically
        self.grid_columnconfigure(1, weight=1)  # Center the form horizontally

        # Back button
        back_image_path = "images/backtrack.png"
        back_image = Image.open(back_image_path).resize((48, 48))
        back_photo = ImageTk.PhotoImage(back_image)
        back_button = tk.Button(self, image=back_photo, command=self.go_back, borderwidth=0)
        back_button.image = back_photo
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Title "Modification Profile"
        title_label = tk.Label(self, text='Modification Profile', font=self.styles.large_font, bg=self.styles.bg_color)
        title_label.grid(row=0, column=1, sticky='ew')

        # Entry fields frame
        entry_fields_frame = tk.Frame(self, bg=self.styles.bg_color)
        entry_fields_frame.grid(row=1, column=1, sticky='nsew')

        # Configure the column with entry fields to expand
        entry_fields_frame.grid_columnconfigure(1, weight=1)

        # Create labeled entries
        self.username_entry = self.create_labeled_entry(entry_fields_frame, 'Username', 'peter', 0)
        self.password_entry = self.create_labeled_entry(entry_fields_frame, 'Password', '********', 1, show='*')
        self.email_entry = self.create_labeled_entry(entry_fields_frame, 'Email', 'peter@example.com', 2)
        self.phone_entry = self.create_labeled_entry(entry_fields_frame, 'Telephone', '11111111111', 3)

        # Save and Cancel buttons
        save_button = ttk.Button(self, text="Sauvegarder", command=self.save_info, style='TButton')
        save_button.grid(row=4, column=0, columnspan=2, padx=50, pady=5, sticky='ew')

        cancel_button = ttk.Button(self, text="Annuler", command=self.cancel_info, style='TButton')
        cancel_button.grid(row=5, column=0, columnspan=2, padx=50, pady=5, sticky='ew')

        
    def create_labeled_entry(self, parent, label, default_value, row, show=None):
        label_widget = tk.Label(parent, text=label, anchor='w', bg=self.styles.bg_color, fg=self.styles.fg_color)
        label_widget.grid(row=row, column=0, padx=10, sticky='w')

        entry_widget = tk.Entry(parent, bg='white', fg='black', insertbackground='black', show=show)
        entry_widget.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        entry_widget.insert(0, default_value)
        return entry_widget

    def save_info(self):
        # Implement save functionality here
        print("Save functionality not implemented.")

    def cancel_info(self):
        # Implement cancel functionality here
        print("Cancel functionality not implemented.")

    def go_back(self):
        # Implement go back functionality here
        self.controller.switch_frame('MemberPage')


if __name__ == "__main__":
    root = tk.Tk()
    profile = InfoProfile(root, None)
    profile.pack(fill='both', expand=True)
    root.mainloop()
