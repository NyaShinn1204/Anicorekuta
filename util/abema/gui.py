# util/abema/gui.py
import customtkinter as ctk

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()

def init_gui(frame_scroll):
    module_frame = ctk.CTkFrame(frame_scroll, fg_color="#3f5673", bg_color="#3f5673", width=1100, height=768)
    module_frame.place(x=0, y=0)
    ctk.CTkLabel(master=module_frame, text="aaa").place(x=50,y=150)
    return module_frame
