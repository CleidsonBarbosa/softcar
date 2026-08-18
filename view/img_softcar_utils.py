import os
from PIL import Image, ImageTk


def carregar_img_softcar():
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img_softcar.png")
    if os.path.exists(img_path):
        return Image.open(img_path)
    return None


def criar_img_softcar(canvas, img_softcar_original):
    if not img_softcar_original:
        return None, None
    img_tk = ImageTk.PhotoImage(img_softcar_original.resize((350, 137), Image.Resampling.LANCZOS))
    btn_id = canvas.create_image(160, 63, image=img_tk, anchor="center", tags="dashboard_img")
    canvas.image_softcar = img_tk
    return btn_id, img_tk


def redimensionar_img_softcar(canvas, btn_dashboard_id, img_softcar_original, w, h):
    if not btn_dashboard_id or not img_softcar_original:
        return
    img_w = max(1, int(w * 0.20) - 80)
    img_h = max(1, int(h * 0.12) + 10)
    img_resized = img_softcar_original.resize((img_w, img_h), Image.Resampling.LANCZOS)
    img_tk_new = ImageTk.PhotoImage(img_resized)
    canvas.image_softcar = img_tk_new
    canvas.itemconfig(btn_dashboard_id, image=img_tk_new)
    canvas.tag_raise(btn_dashboard_id)
    img_x = max(img_w // 2, w * 0.10 - 50)
    img_y = max(img_h // 2, h * 0.05)
    canvas.coords(btn_dashboard_id, img_x, img_y)
