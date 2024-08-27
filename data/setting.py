import os
import customtkinter as ctk

title = "U-Next Downloader | "

output_type = ctk.StringVar()
output_type.set("streamfab")
fast_download = ctk.BooleanVar()
fast_download.set(True)
global_cookie = {}
image_references = []
image_references_episode = []

url_list = []
meta_list = {"title_ids":[]}
title_list = {"title_ids":[]}



# Define folders
cwd = os.getcwd()
folders = {
    "binaries": os.path.join(cwd, "binaries"),
    "output": os.path.join(cwd, "output"),
    "temp": os.path.join(cwd, "temp"),
}

api_list = {
    "unext": "https://cc.unext.jp",
}