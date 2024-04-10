import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import os

class DisplayVideo(tk.Frame):
    def __init__(self, parent, styles, controller):
        super().__init__(parent, bg=styles.base_style['bg'])
        self.styles = styles
        self.controller = controller
        self.thumbnail, self.video_path = self.load_video()
        self.build_ui()

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_header()
        self.create_content_area()
        self.display_video()


    def create_header(self):
        self.header = tk.Frame(self, bg=self.styles.bg_color)
        self.header.grid(row=0, column=0, sticky='ew')
        self.header.grid_columnconfigure(1, weight=1)

        self.create_menu_icon(self.header)
        self.create_logo(self.header)
        self.create_search_bar(self.header)
        self.create_buttons_frame(self.header)
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

    def home(self):
        self.controller.switch_frame('HomePage')
        
    def open_administrateur(self):
        print("Ouverture de la page d'administration.")
        self.controller.switch_frame('AdminPage')
        
    def logout(self):
        self.controller.set_login_state(False)

    def load_video(self):
        image_name = "Rihana.png"
        thumbnail_path = os.path.join("images", image_name)
        video_path = thumbnail_path.replace('.png', '.mp4')
        image = Image.open(thumbnail_path).resize((600, 300)) 
        thumbnail = ImageTk.PhotoImage(image)
        return thumbnail, video_path

    def display_video(self):
        thumb_frame = tk.Frame(self.content_frame, bg=self.styles.bg_color)
        thumb_frame.grid(row=0, column=0, padx=10, pady=(10,20))
        self.content_frame.grid_columnconfigure(0, weight=1)

        thumb_label = tk.Label(thumb_frame, image=self.thumbnail, bg=self.styles.bg_color)
        thumb_label.image = self.thumbnail  
        thumb_label.image_path = self.video_path.replace('.mp4', '.png')  
        thumb_label.grid(row=1, column=0)

        title_font = self.styles.large_font.copy()
        title_font.config(size=self.styles.large_font.cget("size") + 20, weight='bold')

        title_label = tk.Label(thumb_frame, text="Love on the Brain", font=title_font, bg=self.styles.bg_color, fg=self.styles.fg_color)
        title_label.grid(row=0, column=0, sticky='sw', pady=(20, 0))

        author_label = tk.Label(thumb_frame, text="Rihanna", font=self.styles.base_font, bg=self.styles.bg_color, fg=self.styles.fg_color)
        author_label.grid(row=2, column=0, pady=(0,10))
        description_label = tk.Label(
            thumb_frame,
            text="Rihanna's music video for \"Love on the Brain\" captures the emotional intensity of the song, which delves into the complexities of love and heartache. The video features a moody, vintage aesthetic with dark lighting, emphasizing the song's soulful vibe. Rihanna delivers a raw and passionate vocal performance, portraying a range of emotions from vulnerability to defiance. The simplicity of the video, with its focus on Rihanna's expressive performance, allows the powerful lyrics and melody to shine. \"Love on the Brain\" stands out as a visually and emotionally impactful piece, showcasing Rihanna's artistry and the depth of her music.",
            font=self.styles.small_font,
            bg=self.styles.bg_color,
            fg=self.styles.fg_color,
            wraplength=400,  
            justify="center"  
        )
        description_label.grid(row=3, column=0, pady=(0, 10))

        thumb_label.bind("<Button-1>", lambda e: self.open_video_page(self.video_path))
        thumb_label.bind("<Enter>", lambda e: self.show_overlay(thumb_label))
        thumb_label.bind("<Leave>", lambda e: self.hide_overlay(thumb_label))


    def show_overlay(self, thumb_label):
        thumbnail_image_path = thumb_label.image_path
        thumbnail = Image.open(thumbnail_image_path)
        blurred_thumbnail = thumbnail.filter(ImageFilter.GaussianBlur(radius=5))

        blurred_thumbnail = blurred_thumbnail.resize((600,300))
        blurred_photo = ImageTk.PhotoImage(blurred_thumbnail)

        thumb_label.configure(image=blurred_photo)
        thumb_label.blurred_image = blurred_photo  

        play_image_path = "images/play.png"
        play_image = Image.open(play_image_path).resize((48, 48))
        play_photo = ImageTk.PhotoImage(play_image)
        play_button = tk.Label(thumb_label, image=play_photo, borderwidth=0, bg='white')
        play_button.image = play_photo  # Keep a reference
        play_button.place(relx=0.5, rely=0.5, anchor='center')
        play_button.bind("<Button-1>", lambda e: self.open_video_page(self.video_path))

    def hide_overlay(self, thumb_label):
        thumb_label.configure(image=self.thumbnail)
        thumb_label.image = self.thumbnail

        for widget in thumb_label.winfo_children():
            widget.destroy()


    def open_video_page(self, video_path):
        video_path = os.path.abspath(video_path)
        applescript_command = f'''
        tell application "QuickTime Player"
            activate
            open "{video_path}"
            set screenSize to bounds of window of desktop
            set winWidth to 600
            set winHeight to 300
            set winX to (item 3 of screenSize) / 2 - winWidth / 2
            set winY to (item 4 of screenSize) / 2 - winHeight / 2
            set bounds of front window to {{winX, winY, winWidth, winHeight}}
        end tell
        '''
        os.system(f'osascript -e \'{applescript_command}\'')
