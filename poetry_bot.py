import re
import pyperclip
import keyboard
import time
import win32gui
import win32con
import win32clipboard
import tkinter as tk
from threading import Thread
import traceback
import os

class PoetryBot:
    def __init__(self):
        try:
            print("初始化诗词机器人...")
            self.poems = {}
            self.is_active = False
            self.last_text = ""
            self.create_gui()
            print("初始化完成")
        except Exception as e:
            print(f"初始化失败: {str(e)}")
            print(traceback.format_exc())
        
    def create_gui(self):
        """创建GUI界面"""
        try:
            print("创建GUI界面...")
            self.window = tk.Tk()
            self.window.title("诗词接龙助手")
            self.window.geometry("300x150")
            
            # 状态标签
            self.status_label = tk.Label(
                self.window, 
                text="当前状态：已关闭", 
                font=("微软雅黑", 12)
            )
            self.status_label.pack(pady=20)
            
            # 开关按钮
            self.toggle_button = tk.Button(
                self.window,
                text="开启",
                command=self.toggle,
                width=20,
                height=2,
                font=("微软雅黑", 10)
            )
            self.toggle_button.pack()
            print("GUI界面创建完成")
        except Exception as e:
            print(f"创建GUI失败: {str(e)}")
            print(traceback.format_exc())

    def load_poems(self):
        """从poems.js加载诗词数据"""
        try:
            print("开始加载诗词数据...")
            with open('static/poems.js', 'r', encoding='utf-8') as f:
                content = f.read()
                print("文件读取成功")
                start = content.find('{')
                end = content.rfind('}')
                if start != -1 and end != -1:
                    poems_str = content[start:end+1]
                    exec(f"self.poems = {poems_str}")
                    print(f"成功加载 {len(self.poems)} 首诗词")
                else:
                    print("未找到有效的诗词数据")
            print("诗词数据加载成功！")
        except FileNotFoundError:
            print("找不到 poems.js 文件，请检查文件路径")
            print(f"当前工作目录: {os.getcwd()}")
        except Exception as e:
            print(f"加载诗词数据失败: {str(e)}")
            print(traceback.format_exc())

    def detect_poetry(self, text):
        """检测文本中的诗句"""
        for first_line in self.poems.keys():
            if first_line in text:
                return first_line
        return None

    def get_next_line(self, first_line):
        """获取下一句"""
        return self.poems.get(first_line, "抱歉，没有找到下一句")

    def get_active_window_text(self):
        """获取当前活动窗口的文本"""
        keyboard.press_and_release('ctrl+a')
        time.sleep(0.1)
        keyboard.press_and_release('ctrl+c')
        time.sleep(0.1)
        try:
            return pyperclip.paste()
        except:
            return ""

    def send_response(self, text):
        """发送回复"""
        pyperclip.copy(text)
        time.sleep(0.1)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)
        keyboard.press_and_release('enter')

    def toggle(self):
        """切换机器人状态"""
        self.is_active = not self.is_active
        if self.is_active:
            self.status_label.config(text="当前状态：运行中")
            self.toggle_button.config(text="关闭")
            print("诗词机器人已启动")
        else:
            self.status_label.config(text="当前状态：已关闭")
            self.toggle_button.config(text="开启")
            print("诗词机器人已关闭")

    def monitor(self):
        """监控线程"""
        while True:
            try:
                if self.is_active:
                    current_text = self.get_active_window_text()
                    if current_text and current_text != self.last_text:
                        poetry_line = self.detect_poetry(current_text)
                        if poetry_line:
                            next_line = self.get_next_line(poetry_line)
                            self.send_response(next_line)
                            print(f"检测到诗句：{poetry_line}")
                            print(f"回复：{next_line}")
                        self.last_text = current_text
                time.sleep(0.5)
            except Exception as e:
                print(f"发生错误: {str(e)}")
                time.sleep(1)

    def run(self):
        """运行机器人"""
        try:
            print("启动监控线程...")
            monitor_thread = Thread(target=self.monitor, daemon=True)
            monitor_thread.start()
            print("监控线程启动成功")
            
            print("启动GUI主循环...")
            self.window.mainloop()
        except Exception as e:
            print(f"运行失败: {str(e)}")
            print(traceback.format_exc())

if __name__ == "__main__":
    try:
        print("程序开始运行...")
        bot = PoetryBot()
        print("加载诗词数据...")
        bot.load_poems()
        print("启动机器人...")
        bot.run()
    except Exception as e:
        print(f"程序运行失败: {str(e)}")
        print(traceback.format_exc())
        input("按回车键退出...")