import os
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

class Styles:
    def __init__(self):
        self.bg_color = '#ffffff'  # white background
        self.fg_color = '#000000'  # black foreground
        self.button_bg_color = '#a020f0'  # purple button background
        self.button_fg_color = '#ffffff'  # white button text
        self.font_family = 'Helvetica'
        self.base_font_size = 12

        self.base_font = tkfont.Font(family=self.font_family, size=self.base_font_size)
        self.bold_font = tkfont.Font(family=self.font_family, weight='bold', size=self.base_font_size)
        self.large_font = tkfont.Font(family=self.font_family, size=self.base_font_size + 4)
        self.small_font = tkfont.Font(family=self.font_family, size=self.base_font_size - 2)

        self.base_style = {'bg': self.bg_color, 'fg': self.fg_color, 'font': self.base_font}
        self.frame_style = {'bg': self.bg_color}
        self.button_style = {
            'bg': self.button_bg_color,
            'fg': self.button_fg_color,
            'font': self.base_font,
            'highlightthickness': 0,
            'width': 100,  # Default width
                'height': 30,  # Default height
                'corner_radius': 10  # Default corner radius
        }
        self.entry_style = {
            'bg': self.bg_color,
            'fg': self.fg_color,
            'font': self.base_font,
            'highlightthickness': 0,
            'insertbackground': self.fg_color
        }
        self.search_bar_style = {
            'bg': 'white',
              'fg': 'black',
                'font': self.base_font,
                'highlightthickness': 0, 'insertbackground': self.fg_color}

        # Initialize a style for ttk widgets
        self.ttk_style = ttk.Style()
        self.ttk_style.theme_use('classic')  # This theme does not depend on the system theme

        # Configure ttk styles
        self.ttk_style.configure('TButton', background=self.button_bg_color, foreground=self.button_fg_color)
        self.ttk_style.configure('TEntry', fieldbackground=self.bg_color, foreground=self.fg_color)

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def apply_style(self, widget, style_name):
        style = getattr(self, f"{style_name}_style", None)
        if style:
            widget.config(**style)
        else:
            raise ValueError(f"No style named {style_name}")

    def create_rounded_button(self, parent, text, command):
        # Access width, height, and corner_radius from button_style
        width = self.button_style['width']
        height = self.button_style['height']
        corner_radius = self.button_style['corner_radius']
        bg_color = self.button_style['bg']
        fg_color = self.button_style['fg']
        font = self.button_style['font']

        # Create a canvas to draw the button
        button_canvas = tk.Canvas(parent, width=width, height=height, bg=fg_color, highlightthickness=0)
        self.create_rounded_rectangle(button_canvas, 0, 0, width, height, corner_radius, fill=bg_color, outline=fg_color)

        # Add text to the button
        button_canvas.create_text(width / 2, height / 2, text=text, fill=fg_color, font=font)

        # Bind the click event to the button
        button_canvas.bind("<Button-1>", lambda event: command())

        return button_canvas
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [x1 + radius, y1,
                x1 + radius, y1,
                x2 - radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1 + radius,
                x1, y1]
        return canvas.create_polygon(points, smooth=True, **kwargs)

# In your Styles class:

    def create_rounded_entry(self, parent, **kwargs):
        # Ensure width and height are provided in kwargs
        width = kwargs.get('width', 150)
        height = kwargs.get('height', 30)

        # Create a frame to hold the canvas and entry
        frame = tk.Frame(parent, bg='white', highlightthickness=0)
        frame.grid(row=0, column=0, sticky="nsew") 

        # Create a canvas in the frame
        canvas = tk.Canvas(frame, width=width, height=height, bg='white', highlightthickness=0)
        canvas.grid(row=0, column=0)  # Use grid instead of pack

        # Draw a rounded rectangle on the canvas
        self.create_rounded_rectangle(canvas, 0, 0, width, height, 10, fill='white', outline='white')

        # Create a separate frame for the entry widget
        entry_frame = tk.Frame(frame, bg='white', highlightthickness=0)
        entry_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew") 

        # Now create an entry on the entry_frame
        entry = tk.Entry(entry_frame, **kwargs)
        entry.pack(fill=tk.BOTH, expand=True)  # Use pack to fill the entry_frame

        # Return both the frame and the entry widget
        return frame, entry


