import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

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
        back_image = self.create_photo_image(self.styles.resource_path("images/backtrack.png"), (48, 48))
        back_button = tk.Button(self, image=back_image, command=self.go_back, borderwidth=0, bg=self.styles.bg_color)
        back_button.image = back_image
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
        self.username_entry = self.create_labeled_entry(entry_fields_frame, 'username', 'peter', 0)
        self.password_entry = self.create_labeled_entry(entry_fields_frame, 'password', '********', 1, show='*')
        self.confirm_password_entry = self.create_labeled_entry(entry_fields_frame, 'confirm password', '********', 2, show='*')
        self.email_entry = self.create_labeled_entry(entry_fields_frame, 'email', 'peter@example.com', 3)
        self.phone_entry = self.create_labeled_entry(entry_fields_frame, 'telephone', '11111111111', 4)

        # Save button
        save_button = tk.Button(self, text="Sauvegarder", command=self.save_info, bg=self.styles.button_bg_color)
        save_button.grid(row=2, column=1, pady=20, sticky='ew')

        # Cancel button
        cancel_button = tk.Button(self, text="Annuler", command=self.cancel_info, bg=self.styles.button_bg_color)
        cancel_button.grid(row=3, column=1, pady=10, sticky='ew')

    def create_labeled_entry(self, parent, label, default_value, row, show=None):
        # Label
        label_widget = tk.Label(parent, text=label, anchor='w', bg=self.styles.bg_color, fg=self.styles.fg_color)
        label_widget.grid(row=row, column=0, padx=10, sticky='w')
        
        # Entry
        entry_widget = tk.Entry(parent, bg='white', fg='black', insertbackground='black', show=show)
        entry_widget.grid(row=row, column=1, padx=10, pady=5, sticky='ew')
        entry_widget.insert(0, default_value)
        return entry_widget

    def save_info(self):
        # Implement save functionality here
        messagebox.showinfo("Info", "Save functionality not implemented.")

    def cancel_info(self):
        # Implement cancel functionality here
        messagebox.showinfo("Info", "Cancel functionality not implemented.")

    def go_back(self):
        if self.controller:
            self.controller.switch_frame('MemberPage')  # Replace 'MemberPage' with your actual frame name for back navigation
        else:
            messagebox.showinfo("Back", "No controller to handle the back operation.")

    def create_photo_image(self, path, size):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)



if __name__ == "__main__":
    root = tk.Tk()
    profile = InfoProfile(root)
    profile.pack(fill='both', expand=True)
    root.mainloop()

