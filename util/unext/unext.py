# util/unext/main.py
import os
import re
import requests

import util.unext.utils.main as util

import data.setting as setting

from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

def load_cookie():
    fTyp = [("クッキーファイル","*.txt")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir, title="U-NEXTのクッキー設定(Netscape)")
    if len(file_name) == 0:
        print('選択をキャンセルしました')
    else:
        
        check_cookie = util.parse_cookiefile(file_name)
        print(check_cookie)
        if check_cookie != None:
            status, id, message = util.check_cookie(check_cookie)
            if status == True:
                CTkMessagebox(title="成功", message=f"クッキーが有効です\nユーザーID: {id}", font=("BIZ UDゴシック", 13, "normal"))
                setting.global_cookie = check_cookie
            if status == False and message == None:
                CTkMessagebox(title="失敗", message="クッキーが無効です", icon="cancel", font=("BIZ UDゴシック", 13, "normal"))
            if status == False and message == "Expired":
                CTkMessagebox(title="失敗", message="クッキーの期限が切れています\n再度取得してください", icon="cancel", font=("BIZ UDゴシック", 13, "normal"))
        else:
            CTkMessagebox(title="失敗", message="クッキーを正常に読み込めませんでした", icon="cancel", font=("BIZ UDゴシック", 13, "normal"))

def get_metadata(url):
    if url != None:
        title_json = {"id": "", "title_list": []}
        if url not in setting.url_list:
            print("not duplicate")
            setting.url_list.append(url)
            #root.title(setting.title+"メタデータの取得中...")
        else:
            CTkMessagebox(title="エラー", message="すでにリストに存在します", icon="cancel", font=("BIZ UDゴシック", 13, "normal"))
            return

        # 正規表現パターンでSIDを取得
        match = re.search(r'SID(\d+)', url)
        if match:
            title_name = match.group(0)  # 'SID0063364'
            os.makedirs(os.path.join(setting.folders["temp"], title_name), exist_ok=True)
            title_json["id"] = title_name
        else:
            print("Unknown URL")
            return

        data = {
            "operationName": "cosmo_getVideoTitle",
            "variables": {"code": title_name},
            "query": "query cosmo_getVideoTitle($code: ID!) {\n  webfront_title_stage(id: $code) {\n    id\n    titleName\n    rate\n    userRate\n    productionYear\n    country\n    catchphrase\n    attractions\n    story\n    check\n    seriesCode\n    seriesName\n    publicStartDate\n    displayPublicEndDate\n    restrictedCode\n    copyright\n    mainGenreId\n    bookmarkStatus\n    thumbnail {\n      standard\n      secondary\n      __typename\n    }\n    mainGenreName\n    isNew\n    exclusive {\n      typeCode\n      isOnlyOn\n      __typename\n    }\n    isOriginal\n    lastEpisode\n    updateOfWeek\n    nextUpdateDateTime\n    productLineupCodeList\n    hasMultiprice\n    minimumPrice\n    country\n    productionYear\n    paymentBadgeList {\n      name\n      code\n      __typename\n    }\n    nfreeBadge\n    hasDub\n    hasSubtitle\n    saleText\n    currentEpisode {\n      id\n      interruption\n      duration\n      completeFlag\n      displayDurationText\n      existsRelatedEpisode\n      playButtonName\n      purchaseEpisodeLimitday\n      __typename\n    }\n    publicMainEpisodeCount\n    comingSoonMainEpisodeCount\n    missingAlertText\n    sakuhinNotices\n    hasPackRights\n    __typename\n  }\n}\n",
        }

        response = requests.post(setting.api_list["unext"], json=data, cookies=setting.global_cookie)
        response_data = response.json()["data"]["webfront_title_stage"]

        standard_thumbnail_url = response_data["thumbnail"]["standard"]
        standard_thumbnail_data = requests.get("https://" + standard_thumbnail_url).content
    
        #temp_image_path = os.path.join(folders["temp"], title_name, "standard_thumbnail.png")
        #with open(temp_image_path, mode="wb") as f:
        #    f.write(standard_thumbnail_data)
        #
        ## 画像のリサイズ
        #image = Image.open(temp_image_path)
        #image = image.resize((100, 70), Image.Resampling.LANCZOS)
        #
        ## Tkinter画像オブジェクトを生成
        #photo = ImageTk.PhotoImage(image)
    
        # Store reference to prevent garbage collection
        #setting.image_references.append(photo)
    
        # ツリービューに画像を追加
        title_name_jp = response_data["titleName"]
        episode_count = response_data["publicMainEpisodeCount"]
        #oya = tree.insert("", "end", text="", image=photo, values=(title_name_jp, episode_count, "0", "0"))
        
        data = {
            "operationName": "cosmo_getVideoTitleEpisodes",
            "variables": {"code": title_name, "pageSize": episode_count},
            "query": "query cosmo_getVideoTitleEpisodes($code: ID!, $page: Int, $pageSize: Int) {\n  webfront_title_titleEpisodes(id: $code, page: $page, pageSize: $pageSize) {\n    episodes {\n      id\n      episodeName\n      purchaseEpisodeLimitday\n      thumbnail {\n        standard\n        __typename\n      }\n      duration\n      displayNo\n      interruption\n      completeFlag\n      saleTypeCode\n      introduction\n      saleText\n      episodeNotices\n      isNew\n      hasPackRights\n      minimumPrice\n      hasMultiplePrices\n      productLineupCodeList\n      isPurchased\n      purchaseEpisodeLimitday\n      __typename\n    }\n    pageInfo {\n      results\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
        response = requests.post(setting.api_list["unext"], json=data, cookies=setting.global_cookie)
        # print(response.json()["data"]["webfront_title_titleEpisodes"])
        response.json()["data"]["webfront_title_titleEpisodes"]["episodes"]
        episode_num = 1
        #root.title(setting.title+f"メタデータの取得中... 0/{len(response.json()["data"]["webfront_title_titleEpisodes"]["episodes"])}")
        for i in response.json()["data"]["webfront_title_titleEpisodes"]["episodes"]:
            episode_thumbnail_url = i["thumbnail"]["standard"]
            episode_thumbnail_data = requests.get("https://" + episode_thumbnail_url).content
        
            episode_temp_image_path = os.path.join(setting.folders["temp"], title_name, f"episode_{episode_num}_thumbnail.png")
            #with open(episode_temp_image_path, mode="wb") as f:
            #    f.write(episode_thumbnail_data)
        
            ## 画像のリサイズ
            #episode_image = Image.open(episode_temp_image_path)
            #print(episode_temp_image_path)
            #episode_image = episode_image.resize((100, 70), Image.Resampling.LANCZOS)
            
            ## Tkinter画像オブジェクトを生成
            #episode_photo = ImageTk.PhotoImage(episode_image)
            
            
            #setting.image_references_episode.append(episode_photo)
            
            #title_name_jp_sub = ""
            #
            #if setting.output_type.get() == "original":
            #    title_name_jp_sub = i["displayNo"]+" "+i["episodeName"]
            #if setting.output_type.get() == "streamfab":
            title_name_jp_sub = title_name_jp+"_"+f"#{episode_num}"+"_"+i["episodeName"]
                
            print(title_name_jp_sub)
            title_json_temp = {
                "episode_num": episode_num,
                "title": title_name_jp_sub
            }
            title_json["title_list"].append(title_json_temp)
            
            ##tree.insert(oya, "end", image=photo, text=title_name_jp_sub)
            #tree.insert(oya, "end", text="", image=episode_photo, values=(title_name_jp_sub))
            #root.title(setting.title+f"メタデータの取得中... {episode_num}/{len(response.json()["data"]["webfront_title_titleEpisodes"]["episodes"])}")
            episode_num += 1
    
        print("Metadata loaded and image displayed")
        #root.title(setting.title+f"メタデータの取得完了 {len(response.json()["data"]["webfront_title_titleEpisodes"]["episodes"])}/{len(response.json()["data"]["webfront_title_titleEpisodes"]["episodes"])}")
        setting.title_list["title_ids"].append(title_json)