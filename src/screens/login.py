import tkinter as tk

from PIL import Image, ImageTk

class LoginPage(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.base_style['bg'])
        self.styles = styles
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(3, weight=1) 
        self.grid_rowconfigure(0, weight=1)   
        self.grid_rowconfigure(6, weight=1)     

        # Load and resize the back button image
        back_image_path = "images/backtrack.png"
        back_image = Image.open(back_image_path).resize((48, 48))
        back_photo = ImageTk.PhotoImage(back_image)

        # Back button
        back_button = tk.Button(self, image=back_photo, command=lambda: self.controller.switch_frame('HomePage'), borderwidth=0)
        back_button.image = back_photo
        back_button.grid(row=0, column=0, sticky='nw')

        # Load and resize the logo image
        webtv_image_path = "images/WebTV.png"
        webtv_image = Image.open(webtv_image_path)
        webtv_photo = ImageTk.PhotoImage(webtv_image)

        # Logo label, aligned with the back button
        logo_label = tk.Label(self, image=webtv_photo, bg=self.styles.base_style['bg'])
        logo_label.image = webtv_photo
        logo_label.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        # Label for the title "Connexion", with consistent background color
        subtitle_label = tk.Label(self, text='Connexion', bg=self.styles.base_style['fg'])
        subtitle_label.grid(row=2, column=1, columnspan=2, pady=10)

        # Entry fields frame with background color from styles
        form_frame = tk.Frame(self, bg=self.styles.base_style['bg'])
        form_frame.grid(row=3, column=1, columnspan=2, pady=20)

        # Entry fields
        self.create_entry(form_frame, "Nom d'utilisateur", 0)
        self.create_entry(form_frame, "Mot de passe", 1, show='*')

        # Rounded button for "Login"
        login_button_canvas = self.styles.create_rounded_button(self, "Login", lambda: self.validate_login())
        login_button_canvas.grid(row=4, column=1, columnspan=2, pady=(0,20))

        # Label for "pas de compte ?" with consistent background color
        no_account_label = tk.Label(self, text="Vous n'avez pas de compte?", **self.styles.base_style)
        no_account_label.grid(row=5, column=1, columnspan=2, pady=(20, 0))

        # Rounded button for "S'inscrire"
        signup_button_canvas = self.styles.create_rounded_button(self, "S'inscrire", lambda: self.controller.switch_frame('SignupPage'))
        signup_button_canvas.grid(row=6, column=1, columnspan=2, pady=(0, 20))

    def create_entry(self, parent, label, row, show=None):
        frame = tk.Frame(parent, borderwidth=1.5, relief='sunken', bg='white')
        frame.grid(row=row, column=1, pady=5, padx=10, sticky='ew')
        label_widget = tk.Label(parent, text=label, **self.styles.base_style)
        label_widget.grid(row=row, column=0, sticky='w', padx=10)
        entry_widget = tk.Entry(frame, **self.styles.entry_style, show=show)
        entry_widget.pack(fill='both', expand=True)

        # Set the attributes for username and password entries
        if label == "Nom d'utilisateur":
            self.entry_username = entry_widget
        elif label == "Mot de passe":
            self.entry_password = entry_widget

    def validate_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "" and password == "":
            print("Login successful!")
            self.controller.set_login_state(True)  # This updates the login state
        else:
            print("Login failed.")
