import os
import tkinter as tk
import customtkinter as ctk
from pystyle import Colorate, Colors
from xml.etree import ElementTree as ET
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

version = "0.0.1"

def printl(num, data):
  filename = os.path.basename(__file__)
  if num == "error":
    print(f"["+Colorate.Horizontal(Colors.red_to_blue, "Error")+"]"+f"[{filename}] " + data)
  if num == "debug":
    print(f"["+Colorate.Horizontal(Colors.cyan_to_blue, "Debug")+"]"+f"[{filename}] " + data)
  if num == "info":
    print(f"["+Colorate.Horizontal(Colors.white_to_blue, "Info")+"]"+f"[{filename}] " + data)

root = ctk.CTk()
root.title("Hotaru-WV | v0.0.1")
root.geometry("1366x768")
root.resizable(0, 0)

def setup_sidebar():
  # 画像をRGBAモードで開く
  original_image = Image.open("./data/icon.png").convert("RGBA")
  
  # 画像のサイズを指定
  size = (65, 65)
  
  # 画像をリサイズ
  image_resized = original_image.resize(size, Image.LANCZOS)
  
  # 円形マスクを作成
  mask = Image.new("L", size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0, size[0], size[1]), fill=255)
  
  # 画像を円形に切り抜く
  image_circular = ImageOps.fit(image_resized, mask.size, centering=(0.5, 0.5))
  image_circular.putalpha(mask)
  
  # 背景色を設定 (RGB値で指定)
  background_color = (104, 143, 191)  # 例えば白色
  background = Image.new("RGBA", size, background_color)
  
  # 背景色の上に円形画像を貼り付け
  background.paste(image_circular, (0, 0), image_circular)
  
  # ラベルに背景付きの円形画像を設定
  logo_image = ctk.CTkImage(background, size=size)
  
  tk.Label(root, bg="#3f5673", width=1024, height=720).place(x=0,y=0)
  tk.Label(root, bg="#688fbf", width=32, height=720).place(x=0,y=0)
  
  ctk.CTkLabel(master=root,image=logo_image,text="").place(x=5,y=5)
  tk.Label(root, bg="#688fbf", text="Hotaru-WV", fg="#fff", font=("Dubai Medium", 13, "normal")).place(x=85,y=0)
  tk.Label(root, bg="#688fbf", text=version, fg="#505b5e", font=("Dubai Medium", 13, "normal")).place(x=85,y=25)
  
  modulelist = ctk.CTkFrame(master=root, width=230, height=720, corner_radius=0, fg_color="#688fbf")
  modulelist.place(x=0,y=100)
  #tk.Canvas(bg="#0a111e", highlightthickness=0, height=2080, width=4).place(x=230, y=0)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Joiner / Leaver", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 1)).place(x=20,y=12)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/spammer.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Spammer", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 2)).place(x=20,y=57)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/setting.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Settings", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 1)).place(x=20,y=516)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/info.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="About", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 2)).place(x=20,y=562)
  
def setup_content():
  print("coming soon lol")

printl("info", "Loading GUI")
setup_sidebar()
setup_content()


root.mainloop()