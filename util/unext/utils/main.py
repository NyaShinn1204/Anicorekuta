# util/unext/utils/main.py
import requests

def parse_cookiefile(file_path):
    '''クッキーを辞書形式に変換するコード'''
    
    cookies = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                
                parts = line.strip().split('\t')
                if len(parts) < 6:
                    continue
                name = parts[5]
                value = parts[6] if len(parts) > 6 else ''
                
                if name == '_flog':
                    continue
                
                cookies[name] = value

    except FileNotFoundError:
        return None
    except Exception as e:
        return None

    return cookies

def check_cookie(load_cookie):
    import data.setting as setting
    '''クッキーをテストするコード'''
    check_json = {
        "operationName":"cosmo_userInfo",
        "variables":{},
        "query":"query cosmo_userInfo {\n  userInfo {\n    id\n    multiAccountId\n    userPlatformId\n    userPlatformCode\n    superUser\n    age\n    otherFunctionId\n    points\n    hasRegisteredEmail\n    billingCaution {\n      title\n      description\n      suggestion\n      linkUrl\n      __typename\n    }\n    blockInfo {\n      isBlocked\n      score\n      __typename\n    }\n    siteCode\n    accountTypeCode\n    linkedAccountIssuer\n    isAdultPermitted\n    needsAdultViewingRights\n    __typename\n  }\n}\n"
    }
    #print(load_cookie)
    try:    
        test_cookie = requests.post(setting.api_list["unext"], json=check_json, cookies=load_cookie)
        return_json = test_cookie.json()
        #print(return_json)
        if return_json["data"]["userInfo"]["hasRegisteredEmail"] == True:
            return True, return_json["data"]["userInfo"]["id"], None
        else:
            if return_json["errors"][1]["message"] == "Token Expired":
                return False, None, "Expired"
            return False, None, None
    except:
        return False, None, None