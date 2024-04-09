import tkinter as tk

from styles import Styles
from screens.home import HomePage
from screens.login import LoginPage
from screens.signup import SignupPage
from screens.admin_page import AdminPage
from screens.membre import MemberPage
from screens.infoprofile import InfoProfile

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.styles = Styles()
        self.user_logged_in = False
        self.frames = {
            'HomePage': HomePage,
            'LoginPage': LoginPage,
            'SignupPage': SignupPage,
            'AdminPage': AdminPage,
            'MemberPage': MemberPage,
            'InfoProfile': InfoProfile
        }

        self.title("WebTV")
        self.configure(bg=self.styles.base_style['bg'])  # Set the background color

        self.center_window(800, 700)  # Set your desired window dimensions

        self.current_frame = None
        self.switch_frame('HomePage')

    # updating home page
    def set_login_state(self, state=True):
        self.user_logged_in = state
        self.switch_frame('HomePage')
        
    def switch_frame(self, frame_name):
        if frame_name not in self.frames:
            raise ValueError(f"Unknown frame: {frame_name}")

        if self.current_frame is not None:
            self.current_frame.destroy()
        frame_class = self.frames[frame_name]
        self.current_frame = frame_class(self, self.styles, self)
        self.current_frame.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def center_window(self, width, height):
        # Calculate position x, y
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
