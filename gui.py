import PySimpleGUI as sg
import requests
import os
import random 
import json
import shutil
from bs4 import BeautifulSoup

# Tạo giao diện
layout = [
    [
        sg.Text("Nhập tài khoản muốn dowload", size=(15, 1)),
        sg.Input(key="-taikhoan-", size=(40, 1), default_text="@lanketoanne"),
    ],
    [
        sg.Text("Nhập Has Tag muốn tải", size=(15, 1)),
        sg.Input(key="-hastag-", size=(40, 1), default_text="#xuhuong"),
    ],
    [
        sg.Text("Nhập danh sách link tiktok cần tải", size=(15, 1)),
        sg.Multiline(key="-danhsachlink-", size=(40, 25), default_text="https://tiktok.com/"),
    ],
    [
        sg.Text("Thư mục lưu trữ", size=(15, 1)),
        sg.Input(key="-FOLDER-", size=(40, 1), default_text=r"Vui lòng chọn thư mục để lưu"),
        sg.FolderBrowse("Chọn", key="-FOLDER_BUTTON-"),
    ],
    [
        sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-',visible=False),
        
    ],
    [
         sg.Text('', size=(20, 1), key='-RESULT-')
    ],
    [
        sg.Button("TẢI VỀ", key="-DOWNLOAD_BUTTON-", size=(10, 1), button_color=("white", "green")),    
        sg.Text("Download video tiktok, douyin V1.0", size=(55, 1),text_color="#ddd", font=("Arial", 8, "normal")),
        #sg.Button("TẢI VỀ", key="-DOWNLOAD_BUTTON-"),
    ],
]

window = sg.Window("Tải video tiktok, douyin không logo V1 - Support Web3s.com.vn", layout)

def layvideotiktoktheouser(linkprofile, folder_dir_conf):
    url = "https://tiktok-api15.p.rapidapi.com/index/Tiktok/getUserVideos"

    querystring = {"unique_id":"@tiktok","user_id":linkprofile}

    headers = {
        "X-RapidAPI-Key": "b326c9ca28msh56b226d910fccb1p19c935jsn03094942ab45",
        "X-RapidAPI-Host": "tiktok-api15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    datalistvideo = response.json()
    #print("Video chi tiet: ", datalistvideo)
    videos = datalistvideo["data"]["videos"]
    for video in videos:
        # Generate random filename (optional)
        urlvideo = video["play"]
        videoid = video["video_id"]
        tenvideone = f"video_{videoid}.mp4"
        # Save video content to file
        if folder_dir_conf:
            filepath = os.path.join(folder_dir_conf, tenvideone)
        else:
            filepath = os.path.join(os.getcwd(), tenvideone)
        r = requests.get(urlvideo)  
        #with open (filepath,'wb') as f:
        #    f.write(r.content)
        with open (filepath,'wb') as f:
            for chunk in r.iter_content(1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print(f"Video downloaded successfully to: {filepath}") 


def layvideotheohastag(tukhoa, folder_dir_conf):
    url = "https://tiktok-all-in-one.p.rapidapi.com/search/hashtag"

    querystring = {"query":tukhoa,"offset":"20"}

    headers = {
        "X-RapidAPI-Key": "b326c9ca28msh56b226d910fccb1p19c935jsn03094942ab45",
        "X-RapidAPI-Host": "tiktok-all-in-one.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

def taitiktok(video_url,folder_dir_conf):
    # Lấy mô tả và videoid 
    url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/vid/index"
    
    querystring = {"url": video_url}

    headers = {
        "X-RapidAPI-Key": "b326c9ca28msh56b226d910fccb1p19c935jsn03094942ab45",
        "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
   #print("Chi tiet: ",response.json())
    urlvideo = response.json()["video"][0]
    videoid = response.json()["videoid"][0]
    mota = response.json()["description"][0]
    # description videoid
    #tenvideo = "videos/" + str(random.randrange(1,1000)) +".mp4"
    # Generate random filename (optional)
    tenvideone = f"video_{videoid}.mp4"
    # Save video content to file
    if folder_dir_conf:
        filepath = os.path.join(folder_dir_conf, tenvideone)
    else:
        filepath = os.path.join(os.getcwd(), tenvideone)
    r = requests.get(urlvideo)  
    #with open (filepath,'wb') as f:
    #    f.write(r.content)
    with open (filepath,'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print(f"Video downloaded successfully to: {filepath}")
    #return response.json()["video"][0]

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-FOLDER_BUTTON-":
            folder_path = sg.popup_get_folder("Chọn thư mục")
            if folder_path:
                window["-FOLDER-"].update(folder_path.replace("/", "\\"))
    if event == "-DOWNLOAD_BUTTON-":
        # Xử lý logic tải về ở đây
        taikhoan = values["-taikhoan-"]
        hastag = values["-hastag-"]
        danhsachlink = values["-danhsachlink-"]  
        folder_dir_conf = values["-FOLDER-"]
        # Xu ly download 
        # Chia chuỗi thành các dòng
        lines = danhsachlink.split("\n")
        # In ra từng dòng
        #print ("Lines: ", lines)
        for line in lines:
            if line == "https://tiktok.com/" : break        
            else :
                print("URL: ", line)
                jsonvideo = taitiktok(line,folder_dir_conf)                      

        if taikhoan !="@lanketoanne":
            layvideotiktoktheouser(taikhoan,folder_dir_conf)
        
        if hastag  !="#xuhuong" :
            layvideotheohastag(hastag,folder_dir_conf)

            #print("Data video: ", datavideo)
            #jsonvideo = taitiktok(taikhoan,folder_dir_conf)           
        
        """  
        Option = CfOtions(folder_dir_conf)
        # Khởi tạo trình duyệt với tùy chọn
        driver = webdriver.Chrome(options=Option)
        # Đặt thời gian chờ là 10 giây (có thể điều chỉnh theo nhu cầu của bạn)
        timeout = 60
        driver.set_page_load_timeout(timeout)
        # Tải theo tài khoản
        if taikhoan !="@lanketoanne":
            pyk.save_tiktok_multi_page(taikhoan,save_video=False,save_metadata=True,browser_name=driver)
            print("Tải video thành công!") """
window.close()          