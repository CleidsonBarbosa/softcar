import customtkinter as ctk
from PIL import Image, ImageTk
import os

COR_FUNDO = "#1e2d3d"
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


class BaseScreen(ctk.CTkFrame):
    def __init__(self, parent, app, bg_image="tela_fundo.png"):
        super().__init__(parent, fg_color=COR_FUNDO, corner_radius=15)
        self.app = app

        bg_path = os.path.join(ASSETS_DIR, bg_image)
        self._bg_original = None
        if os.path.exists(bg_path):
            self._bg_original = Image.open(bg_path)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        self._bg_tk = None

        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        if event.widget == self:
            w = self.winfo_width()
            h = self.winfo_height()
            if w > 20 and h > 20:
                max_w = min(1100, int(w * 0.85))
                self.center_frame.configure(width=max_w)
                self.center_frame.place_configure(relx=0.5, rely=0.5, anchor="center", width=max_w)
            self._redraw_bg()

    def _redraw_bg(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 10 or h < 10 or not self._bg_original:
            return
        resized = self._bg_original.resize((w, h), Image.Resampling.LANCZOS)
        self._bg_tk = ImageTk.PhotoImage(resized)
        self.canvas.delete("bg")
        self.canvas.create_image(0, 0, image=self._bg_tk, anchor="nw", tags="bg")
        self.canvas.tag_lower("bg")

    def on_show(self):
        self.after(30, self._redraw_bg)
