import os
import shutil
import tkinter as tk
from tkinter import filedialog

import cv2
import rawpy
import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Image Processing Tool Ver. 1")
        # self.iconbitmap('Images/SU_AutoSoftwareUpgradeTool.ico')
        self.geometry(f"{1024}x{768}")
        self.minsize(1024, 768)

        # 設定3維框架排序
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_appearance_mode("System")
        
        # Themes: "blue" (standard), "green", "dark-blue"
        customtkinter.set_default_color_theme("blue")
        
        ##############################
        # Sidebar frame
        ##############################
        # Create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Title
        self.sidebar_LogoLabel = customtkinter.CTkLabel(self.sidebar_frame, text="Menu bar", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.sidebar_LogoLabel.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="new")

        # 切換頁面按鈕
        self.sidebar_home_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.home_button_event)
        self.sidebar_home_button.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        self.sidebar_frame_2_button = customtkinter.CTkButton(self.sidebar_frame, text="Menu", command=self.frame_2_button_event)
        self.sidebar_frame_2_button.grid(row=3, column=0, padx=20, pady=10, sticky="new")
        self.sidebar_frame_3_button = customtkinter.CTkButton(self.sidebar_frame, text="Setting",command=self.frame_3_button_event)
        self.sidebar_frame_3_button.grid(row=4, column=0, padx=20, pady=10, sticky="new")
        
        # 顏色設定
        self.sidebar_appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Color Mode:", anchor="w")
        self.sidebar_appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.sidebar_appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.sidebar_appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # 介面縮放率
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["70%", "80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))

        # 視窗透明度
        self.sidebar_window_transparency_label = customtkinter.CTkLabel(self.sidebar_frame, text="WT Scaling:", anchor="w")
        self.sidebar_window_transparency_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.sidebar_window_transparency_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["60%", "70%", "80%", "90%", "100%"], command=self.change_window_transparency_event)
        self.sidebar_window_transparency_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 30))
        
        ##############################
        # home frame
        ##############################
        # Create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_rowconfigure(1, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        # 處理資訊
        self.ProcessTextbox = customtkinter.CTkTextbox(self.home_frame, height=300, font=customtkinter.CTkFont(size=12))
        self.ProcessTextbox.grid(row=0, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")

        # create main frame
        self.main_frame = customtkinter.CTkFrame(self.home_frame)
        self.main_frame.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="nsew")
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        
        # 選取資料夾
        self.ImportLabel = customtkinter.CTkLabel(self.main_frame, text="Image Folder", height=30, font=customtkinter.CTkFont(weight="bold"))
        self.ImportLabel.grid(row=1, column=0, padx=(20, 0), pady=(10, 0), sticky="wn")
        self.ImportEntry = customtkinter.CTkEntry(self.main_frame, width=500)
        self.ImportEntry.grid(row=1, column=1, padx=(20, 0), pady=(10, 0), sticky="wn")
        self.ImportButton = customtkinter.CTkButton(self.main_frame, text="Select", width=30, height=30, font=customtkinter.CTkFont(weight="bold"), command=lambda: self.main_button_event(self.ImportEntry))
        self.ImportButton.grid(row=1, column=2, padx=(20, 0), pady=(10, 0), sticky="wn")
        
        self.ExportLabel = customtkinter.CTkLabel(self.main_frame, text="Export Folder", height=30, font=customtkinter.CTkFont(weight="bold"))
        self.ExportLabel.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="wn")
        self.ExportEntry = customtkinter.CTkEntry(self.main_frame, width=500)
        self.ExportEntry.grid(row=2, column=1, padx=(20, 0), pady=(10, 0), sticky="wn")
        self.ExportButton = customtkinter.CTkButton(self.main_frame, text="Select", width=30, height=30, font=customtkinter.CTkFont(weight="bold"), command=lambda: self.main_button_event(self.ExportEntry))
        self.ExportButton.grid(row=2, column=2, padx=(20, 0), pady=(10, 0), sticky="wn")
        
        # 清晰度設定
        self.VagueThresholdLabel = customtkinter.CTkLabel(self.main_frame, text="清晰度閾值", height=30, font=customtkinter.CTkFont(weight="bold"))
        self.VagueThresholdLabel.grid(row=3, column=0, padx=(20, 0), pady=(10, 0), sticky="wn")
        self.VagueThresholdEntry = customtkinter.CTkEntry(self.main_frame, placeholder_text="0.0 ~ 100.0")
        self.VagueThresholdEntry.grid(row=3, column=1, padx=(20, 0), pady=(10, 0), sticky="wn")
        
        # Create operation frame
        self.operation_frame = customtkinter.CTkFrame(self.home_frame)
        self.operation_frame.grid(row=2, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

        # Laplacian 算子
        self.Laplacian_Button = customtkinter.CTkButton(self.operation_frame, text="Laplacian算子", width=100, height=30, font=customtkinter.CTkFont(weight="bold"), command=lambda: self.Laplacian_event())
        self.Laplacian_Button.grid(row=0, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")
        
        # 方差方法
        self.VarianceMethod_Button = customtkinter.CTkButton(self.operation_frame, text="方差方法計算", width=100, height=30, font=customtkinter.CTkFont(weight="bold"), command=lambda: self.VarianceMethod_event())
        self.VarianceMethod_Button.grid(row=0, column=1, padx=(20, 20), pady=(10, 10), sticky="nsew")
        
        ##############################
        # second frame
        ##############################
        # Create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_rowconfigure(1, weight=1)
        self.second_frame.grid_columnconfigure(0, weight=1)
        
        self.second_frame_label = customtkinter.CTkLabel(self.second_frame, text="Tool Manual", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.second_frame_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.second_frame_textbox = customtkinter.CTkTextbox(self.second_frame)
        self.second_frame_textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.second_frame_textbox.insert("0.0", 'by Lucas 20221204')
        self.second_frame_textbox.configure(state="disabled")
        
        ##############################
        # third frame
        ##############################
        # Create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.button = customtkinter.CTkButton(self.third_frame, text="3")
        self.button.grid(row=1, column=0, padx=20, pady=10)

        ##############################
        # set default values
        ##############################
        # Default color
        self.sidebar_appearance_mode_optionemenu.set("System")
        
        # Default UI size
        self.scaling_optionemenu.set("100%")
        customtkinter.set_widget_scaling(1)
        
        # Default window transparency
        self.sidebar_window_transparency_optionemenu.set("100%")
        
        # Show the home frame.
        self.select_frame_by_name("home")
        
    ##############################
    # Function
    ##############################
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_window_transparency_event(self, new_window_transparency: str):
        new_window_transparency = float(new_window_transparency.replace("%", "")) / 100
        self.attributes("-alpha", new_window_transparency)

    def select_frame_by_name(self, name):
        # Change button weight
        if name == "home":
            self.sidebar_home_button.configure(font=customtkinter.CTkFont(weight="bold"))
        else:
            self.sidebar_home_button.configure(font=customtkinter.CTkFont(weight="normal"))
        if name == "frame_2":
            self.sidebar_frame_2_button.configure(font=customtkinter.CTkFont(weight="bold"))
        else:
            self.sidebar_frame_2_button.configure(font=customtkinter.CTkFont(weight="normal"))
        if name == "frame_3":
            self.sidebar_frame_3_button.configure(font=customtkinter.CTkFont(weight="bold"))
        else:
            self.sidebar_frame_3_button.configure(font=customtkinter.CTkFont(weight="normal"))

        # Show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
            
    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
        
    def main_button_event(self, value1):
        filename =  filedialog.askdirectory(title = "Select file")
        value1.delete(0, "end")
        value1.insert(0, filename)
    
    # 拉普拉斯算子 (Laplace operator)
    def Laplacian_event(self):
        RunningSwitch = True
        
        ImportFolderPath = self.ImportEntry.get()
        if len(ImportFolderPath) < 3:
            tk.messagebox.showerror("Error", "錯誤訊息: 請選擇Import Folder!")
            RunningSwitch = False
        
        ExportFolderPath = self.ExportEntry.get()
        if len(ExportFolderPath) < 3:
            tk.messagebox.showerror("Error", "錯誤訊息: 請選擇Export Folder!")
            RunningSwitch = False

        VagueThreshold = self.VagueThresholdEntry.get()
        if len(VagueThreshold) < 1:
            tk.messagebox.showerror("Error", "錯誤訊息: 請填寫清晰度!")
            RunningSwitch = False
        else:
            VagueThreshold = float(VagueThreshold)

        if RunningSwitch:
            ProcessCount = 0
            for filename in os.listdir(ImportFolderPath):
                # Path Setting
                image_path = ImportFolderPath + "/" + filename
                image_path = image_path.replace("/", "\\\\")
                
                # Change RWA image for RGB
                raw = rawpy.imread(image_path)
                rgb = raw.postprocess()

                # 轉會為灰階圖像
                gray_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

                # 計算 Laplacian 算子
                laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
                abs_laplacian = cv2.convertScaleAbs(laplacian)

                # 計算平均灰度值和平均拉普拉斯值
                mean = cv2.mean(gray_image)[0]
                mean_laplacian = cv2.mean(abs_laplacian)[0]

                # 計算清晰率
                blur = mean_laplacian / mean
                blur = blur * 1000
                if blur > VagueThreshold:
                    shutil.copy(image_path, ExportFolderPath)
                    
                ProcessCount = ProcessCount + 1
                self.ProcessTextbox.insert("0.0", ("已處理張數: " + str(ProcessCount) + "\t\t檔案名稱: " + filename + "\t\t\t清晰率: " + str(blur)[0:6] + "\n"))
                self.update()

    # Variance(變異數計算)
    def VarianceMethod_event(self):
        RunningSwitch = True
        
        ImportFolderPath = self.ImportEntry.get()
        if len(ImportFolderPath) < 3:
            tk.messagebox.showerror("Error", "錯誤訊息: 請選擇Import Folder!")
            RunningSwitch = False
        
        ExportFolderPath = self.ExportEntry.get()
        if len(ExportFolderPath) < 3:
            tk.messagebox.showerror("Error", "錯誤訊息: 請選擇Export Folder!")
            RunningSwitch = False

        VagueThreshold = self.VagueThresholdEntry.get()
        if len(VagueThreshold) < 1:
            tk.messagebox.showerror("Error", "錯誤訊息: 請填寫清晰度!")
            RunningSwitch = False
        else:
            VagueThreshold = float(VagueThreshold)

        if RunningSwitch:
            ProcessCount = 0
            for filename in os.listdir(ImportFolderPath):
                # Path Setting
                image_path = ImportFolderPath + "/" + filename
                image_path = image_path.replace("/", "\\\\")
                
                # Change RWA image for RGB
                raw = rawpy.imread(image_path)
                rgb = raw.postprocess()

                # 轉換為灰階圖像
                gray_image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

                # Variance(變異數計算)
                laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
                lap_var = laplacian.var()

                if lap_var > VagueThreshold:
                    shutil.copy(image_path, ExportFolderPath)
                    
                ProcessCount = ProcessCount + 1
                self.ProcessTextbox.insert("0.0", ("已處理張數: " + str(ProcessCount) + "\t\t檔案名稱: " + filename + "\t\t\t清晰率: " + str(lap_var)[0:6] + "\n"))
                self.update()

if __name__ == "__main__":
    app = App()
    app.mainloop()

