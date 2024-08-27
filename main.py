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

import util.abema as downloader_abema
import util.unext as downloader_unext

module_frame = None
prev_frame = None

def clear_frame(frame):
  for widget in frame.winfo_children():
    widget.destroy()
  frame.pack_forget()

def setup_cotent_sidebar(num1, num2, num3):
  global module_frame, prev_frame
  
  # 初期化
  frame = None
  
  frame_scroll = module_frame = ctk.CTkFrame(root, fg_color="#3f5673", bg_color="#3f5673", width=1100, height=768)
  # tk.Label(root, bg="#3f5673", width=1024, height=720).place(x=0,y=0)
  module_frame.place(x=230, y=0)
  clear_frame(frame_scroll)
  # 以前のフレームがある場合はクリアする
  if prev_frame is not None:
      clear_frame(prev_frame)
  if num1 == 1:
    if num2 == 1:
      if num3 == 1:
        frame = downloader_abema.gui.init_gui(frame_scroll)
        
        printl("info", "Open Abema Downloader")
      if num3 == 2:
        frame = downloader_unext.gui.init_gui(frame_scroll)
        
        printl("info", "Open U-next Downloader")
      if num3 == None:
        # Load images and add them to the scrollable frame
        # You should replace the image paths with your own image paths
        image_paths = ["data/service_image/abema.jpg","data/service_image/unext.jpg"]  # Add all your image paths here
        
        def on_image_click(index):
          setup_cotent_sidebar(1, 1, index)
          #print(f"Image {index} clicked!")
        
        for i, path in enumerate(image_paths):
          img = Image.open(path)
          img = ctk.CTkImage(img, size=(175, 100))  # Adjust the size as needed
          label = ctk.CTkLabel(master=frame_scroll, image=img, text="")
          # Set the cursor to hand when hovering over the image
          label.configure(cursor="hand2")
      
          # Bind the click event to the label
          label.bind("<Button-1>", lambda event, idx=i: on_image_click(idx+1))
          label.grid(row=i // 5, column=i % 5, padx=10, pady=10)  # 5 images per row
        printl("info", "Open All Downloader")
    if num2 == 2:
      if num3 == 1:
        printl("info", "Open Download List")
      if num3 == 2:
        printl("info", "Open Already Download List")
  if num1 == 2:
    if num2 == 1:
      printl("info", "Open About Tab")
  prev_frame = frame

def setup_sidebar():
  # 画像をRGBAモードで開く
  original_image = Image.open("./data/icon.png").convert("RGBA")
  
  # 画像のサイズを指定
  size = (50, 50)
  
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
  
  tk.Label(root, bg="#688fbf", width=32, height=720).place(x=0,y=0)
  
  ctk.CTkLabel(master=root,image=logo_image,text="").place(x=15,y=5)
  tk.Label(root, bg="#688fbf", text="Hotaru-WV", fg="#fff", font=("Dubai Medium", 13, "normal")).place(x=70,y=0)
  tk.Label(root, bg="#688fbf", text=version, fg="#505b5e", font=("Dubai Medium", 13, "normal")).place(x=70,y=25)
  
  modulelist = ctk.CTkFrame(master=root, width=230, height=720, corner_radius=0, fg_color="#688fbf")
  modulelist.place(x=0,y=100)
  
  
  def on_enter_home(event):
    button_home.configure(image=ctk.CTkImage(Image.open("data/icon_home_activate.png"),size=(20, 20)))
  
  def on_leave_home(event):
    button_home.configure(image=ctk.CTkImage(Image.open("data/icon_home_disable.png"),size=(20, 20)))
  
  def on_enter_library(event):
    button_library.configure(image=ctk.CTkImage(Image.open("data/icon_library_activate.png"),size=(20, 20)))
  
  def on_leave_library(event):
    button_library.configure(image=ctk.CTkImage(Image.open("data/icon_library_disable.png"),size=(20, 20)))
    
  def on_enter_library_already(event):
    button_library_already.configure(image=ctk.CTkImage(Image.open("data/icon_library_activate.png"),size=(20, 20)))
  
  def on_leave_library_already(event):
    button_library_already.configure(image=ctk.CTkImage(Image.open("data/icon_library_disable.png"),size=(20, 20)))
  
  button_home = ctk.CTkButton(master=modulelist, command=lambda: setup_cotent_sidebar(1, 1, None), image=ctk.CTkImage(Image.open("data/icon_home_disable.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#2b373a", corner_radius=15, text="ホーム", width=215, height=40, font=("BIZ UDゴシック", 16, "normal"), anchor="w")
  button_home.bind('<Enter>', on_enter_home, add='+')
  button_home.bind("<Leave>", on_leave_home, add='+')
  button_home.place(x=5,y=12)
  
  librarylist = ctk.CTkFrame(master=root, width=230, height=384, corner_radius=0, fg_color="#688fbf")
  librarylist.place(x=0,y=384)
  
  tk.Label(librarylist, bg="#688fbf", text="ライブラリー", fg="#fff", font=("BIZ UDゴシック", 13, "normal")).place(x=15,y=0)
  
  button_library = ctk.CTkButton(master=librarylist, command=lambda: setup_cotent_sidebar(1, 2, 1), image=ctk.CTkImage(Image.open("data/icon_library_disable.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#2b373a", corner_radius=15, text="ダウンロードリスト", width=215, height=40, font=("BIZ UDゴシック", 14, "normal"), anchor="w")
  button_library.bind('<Enter>', on_enter_library, add='+')
  button_library.bind("<Leave>", on_leave_library, add='+')
  button_library.place(x=5,y=24)
  
  button_library_already = ctk.CTkButton(master=librarylist, command=lambda: setup_cotent_sidebar(1, 2, 2), image=ctk.CTkImage(Image.open("data/icon_library_disable.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#2b373a", corner_radius=15, text="ダウンロード済みリスト", width=215, height=40, font=("BIZ UDゴシック", 14, "normal"), anchor="w")
  button_library_already.bind('<Enter>', on_enter_library_already, add='+')
  button_library_already.bind("<Leave>", on_leave_library_already, add='+')
  button_library_already.place(x=5,y=69)
  #tk.Canvas(bg="#0a111e", highlightthickness=0, height=2080, width=4).place(x=230, y=0)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Joiner / Leaver", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 1)).place(x=20,y=12)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/spammer.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Spammer", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 2)).place(x=20,y=57)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/setting.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="Settings", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 1)).place(x=20,y=516)
  #ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/info.png"),size=(20, 20)), compound="left", fg_color="#0f1314", hover_color="#ade3f7", corner_radius=0, text="About", width=195, height=40, font=("Roboto", 16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 2)).place(x=20,y=562)
  
def setup_content():
  print("coming soon lol")

printl("info", "Loading GUI")

setup_sidebar()
setup_cotent_sidebar(2, 1, None)
setup_content()


root.mainloop()