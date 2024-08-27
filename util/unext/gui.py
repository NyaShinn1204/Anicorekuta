# util/unext/gui.py
import customtkinter as ctk

from util.unext.unext import *

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()

def init_gui(frame_scroll):
    module_frame = ctk.CTkFrame(frame_scroll, fg_color="#3f5673", bg_color="#3f5673", width=1100, height=768)
    module_frame.place(x=0, y=0)
    
    #ctk.CTkLabel(module_frame, text="U-Next ダウンローダー", text_color="#fff", font=("BIZ UDゴシック", 16, "normal")).place(x=10,y=10)
    
    ctk.CTkButton(module_frame, text="クッキーの読み込み", font=("BIZ UDゴシック", 13, "normal"), command=load_cookie).place(x=10,y=10)

    url_or_path_entry = ctk.CTkEntry(module_frame, placeholder_text="URL or PATH", width=300)
    url_or_path_entry.place(x=160,y=10)
    
    ctk.CTkButton(module_frame, text="メタデータの取得", font=("BIZ UDゴシック", 13, "normal"), command=lambda: get_metadata(url_or_path_entry.get()), width=70).place(x=340,y=45)
    
    #ctk.CTkButton(module_frame, text="開始", font=("BIZ UDゴシック", 13, "normal"), command=start_download, width=70).place(x=390,y=45)
    #ctk.CTkButton(module_frame, text="強制停止", font=("BIZ UDゴシック", 13, "normal"), command=stop_download, width=70).place(x=390,y=80)
    
    
    ctk.CTkCheckBox(master=module_frame, text_color="#fff", text="高速ダウンロード", variable=setting.fast_download, corner_radius=4, border_width=3, checkbox_width=20, checkbox_height=20, font=("BIZ UDゴシック", 13, "normal")).place(x=10,y=50)
    #ctk.CTkCheckBox(master=module_frame, text_color="#fff", text="高速ダウンロード", variable=setting.fast_download, corner_radius=4, border_width=3, checkbox_width=20, checkbox_height=20, font=("BIZ UDゴシック", 13, "normal")).place(x=10,y=75)
    
    return module_frame
