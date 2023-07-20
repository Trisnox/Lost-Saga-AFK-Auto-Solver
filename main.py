import ctypes
import cv2
import itertools
import json
import multiprocessing
import numpy as np
import os
import pydirectinput
import pynput
import pytesseract
import time
import random
import requests
import string
import tkinter as tk
import win32gui, win32com.client
from PIL import Image, ImageGrab, ImageTk
from tkinter import filedialog, ttk, messagebox

input_process = None
main_process = None
toggle = False
pup_up = None
pynput_keyboard = None

with open('config.json', 'r') as f:
    config: dict = json.load(f)

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in itertools.count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

current = set()

def on_press(key):
    combination = {pynput.keyboard.Key.ctrl, '\x03', 'c'}

    if key == pynput.keyboard.Key.f6:
        toggle_script()
    elif key in combination:
        current.add(key)
        if all(k in current for k in combination):
            listener.stop()
            raise KeyboardInterrupt

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def main():
    global config
    global pynput_keyboard
    print('Script has been started')
    pytesseract.pytesseract.tesseract_cmd = config['tesseract']
    u_input = config['input']

    pynput_keyboard = pynput.keyboard.Controller()

    while True:
        time.sleep(config['interval'])

        res = math_loop()
        
        if not res:
            continue
        
        ans = str(sum(tuple(map(int, res))))
        if u_input == 'directinput':
            pydirectinput.typewrite(ans, interval=0.025)
            time.sleep(.1)
            pydirectinput.press('enter')
        else:
            pynput_keyboard.type(ans)
            time.sleep(.1)
            pynput_keyboard.tap(pynput.keyboard.Key.enter)

def math_loop():
    img = get_win_ss()
    if not img:
        return False
    img = pre_crop(img)
    
    res = image_search(img, './img/afk1.png')
    if not res:
        res = image_search(img, './img/afk2.png')
    
    if not res:
        return False
    fn = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
    img.save(f'img/{fn}.png')
    img = math_crop(img)

    text = ocr(img)

    num = ocr_check(text)

    if not num:
        num = math_loop()
    
    return num

def get_win_ss():
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    lso = [(hwnd, title) for hwnd, title in winlist if 'lost saga in time' in title.lower()]
    try:
        lso = lso[0]
        hwnd = lso[0]
    except IndexError:
        return False
    
    # fix fullscreen problem... I think?
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    
    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    time.sleep(0.4)
    img = ImageGrab.grab(bbox)
    if img:
        return img
    else:
        return False

def pre_crop(img):
    global config
    if not config['window'] == 'full': # windowed mode
        w, h = img.size
        if config['resolution'] == '800x600':
            img = img.crop(((w - 255) // 2, 45, (w + 255) // 2, 171))
        elif config['resolution'] == '1024x768':
            img = img.crop(((w - 255) // 2, 50, (w + 255) // 2, 176))
        elif config['resolution'] == '1280x720':
            img = img.crop(((w - 255) // 2, 49, (w + 255) // 2, 151))
        elif config['resolution'] == '1280x1024':
            img = img.crop(((w - 255) // 2, 59, (w + 255) // 2, 185))
        elif config['resolution'] == '1600x900':
            img = img.crop(((w - 255) // 2, 55, (w + 255) // 2, 182))
        elif config['resolution'] == '1680x1050':
            img = img.crop(((w - 255) // 2, 60, (w + 255) // 2, 186))
        elif config['resolution'] == '1920x1080':
            img = img.crop(((w - 255) // 2, 61, (w + 255) // 2, 187))
        else:
            print('unknown resolution selected')
    else:
        w, h = img.size
        if config['resolution'] == '800x600':
            img = img.crop(((w - 255) // 2, 19, (w + 255) // 2, 145))
        elif config['resolution'] == '1024x768':
            img = img.crop(((w - 255) // 2, 24, (w + 255) // 2, 150))
        elif config['resolution'] == '1280x720':
            img = img.crop(((w - 255) // 2, 23, (w + 255) // 2, 149))
        elif config['resolution'] == '1280x1024':
            img = img.crop(((w - 255) // 2, 33, (w + 255) // 2, 159))
        elif config['resolution'] == '1600x900':
            img = img.crop(((w - 255) // 2, 29, (w + 255) // 2, 156))
        elif config['resolution'] == '1680x1050':
            img = img.crop(((w - 255) // 2, 34, (w + 255) // 2, 160))
        elif config['resolution'] == '1920x1080':
            img = img.crop(((w - 255) // 2, 35, (w + 255) // 2, 161))
        else:
            print('unknown resolution selected')
    
    return img

def math_crop(img):
    img = img.crop((29, 65, 53+29, 15+65))
    w, h = img.size
    img = img.resize((w*5, h*5), resample=Image.LANCZOS)
    file_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
    img.save(f'./img/{file_name}.png')
    return img

def image_search(ss, target):
    img_rgb = np.array(ss)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(target, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < 0.8:
        return None

    return max_loc

# turns out, ocr was much more simpler this way
def ocr(img):
    text = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=0123456789+- --psm 6 digits')
    print(text)
    return text


# def ocr():
#     global file_name
#     img = cv2.imread(f"img/{file_name}.png")

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

#     rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

#     dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

#     contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
#                                                      cv2.CHAIN_APPROX_NONE)

#     im2 = img.copy()

#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)

#         rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         cropped = im2[y:y + h, x:x + w]

#         text = pytesseract.image_to_string(cropped, config='-c tessedit_char_whitelist=0123456789+- --psm 6 digits')
#         print(text)

#     return text

def ocr_check(result):
    global config
    global pynput_keyboard
    # rewrite this later for - math operation
    filtered = result.split('+')
    try:
        num1 = filtered[0]
        int(num1)
        num2 = filtered[1]
        int(num2)
    except (ValueError, IndexError):
        print('OCR failed to identify numbers, retrying')
        u_input = config['input']
        if u_input == 'directinput':
            pydirectinput.press('1')
            time.sleep(.1)
            pydirectinput.press('enter')
        else:
            pynput_keyboard.tap('1')
            time.sleep(.1)
            pynput_keyboard.tap(pynput.keyboard.Key.enter)
        return False

    if len(num1) >= 3:
        num1 = num1[2]
        return (num1, num2)
    else:
        return (num1, num2)

def toggle_script():
    global main_process
    global toggle
    global tesseract_loc
    global interval_input
    global fix_input
    global input_input
    global window_input
    global resolution_input
    global toggle_button

    global config

    if not toggle:
        tesseract_loc.set(tesseract_entry.get())
        interval_input.set(interval_entry.get())
        
        if not tesseract_loc.get():
            tk.messagebox.showerror(title='Invalid', message='Tesseract location cannot be empty')
            return False
        
        try:
            float(interval_input.get())
        except ValueError:
            tk.messagebox.showerror(title='Invalid', message='Interval must be a number (integer or float)')
            return False
        
        config['tesseract'] = tesseract_loc.get().replace('/', '\\')
        config['fix'] = fix_input.get()
        config['input'] = input_input.get()
        config['interval'] = float(interval_input.get())
        config['window'] = window_input.get()
        config['resolution'] = resolution_input.get()

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        toggle = True
        toggle_button.config(text='Stop')
        main_process = multiprocessing.Process(target=main)
        main_process.start()
    else:
        main_process.terminate()
        toggle = False
        main_process = None
        print('Script has been stopped')
        toggle_button.config(text='Mulai')

def test_input_button():
    global pop_up
    global image_sequence
    global frames
    global count

    frames = 50
    count = 0

    pop_up = tk.Toplevel(window)
    pop_up.title('')

    
    pic_label = ttk.Label(pop_up, text='After pressing ok, focus your window to lost saga and wait a few seconds.\nIf chat box appear like this, it means the input is working fine')
    pic_label.grid(row=1, column=2)

    image = ImageLabel(pop_up)
    image.grid(row=2, column=2)
    image.load('./img/input.gif')

    oki = ttk.Button(pop_up, text='ok', command=lambda:test_input())
    oki.grid(row=3, column=2)

def test_input():
    global pop_up
    global input_process

    pop_up.destroy()

    input_process = multiprocessing.Process(target=the_actual_input)

    input_process.start()

def the_actual_input():
    # oversight
    # config in this context is never dumped again and not refreshed, this is because I can't access tkinter outside multiprocess
    global config
    time.sleep(5)
    u_input = config['input']
    if u_input == 'directinput':
        pydirectinput.press('enter')
        pydirectinput.typewrite('abc123', interval=0.05)
    else:
        controller = pynput.keyboard.Controller()
        controller.tap(pynput.keyboard.Key.enter)
        controller.type('abc123')

def test_screenshot():
    tk.messagebox.showinfo(message='After pressing ok, focus your window to lost saga then wait a few seconds. After more than 5/6 seconds, screenshot will appear at img folder')
    time.sleep(5)

    img = get_win_ss()

    if img:
        img.save('./img/ss.png')
    else:
        tk.messagebox.showwarning(title='Warning', message='Cannot take screenshot from Lost Saga because the process is not found')

def tesseract_set():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select A File",filetype = (("exe","*.exe"),("All Files","*.*")))
    if filename:
        tesseract_loc.set(filename)

if __name__ == '__main__': # stupid multiprocessing
    def version_check():
        version = "0.4.1"
        response = requests.get("https://api.github.com/repos/Trisnox/Lost-Saga-AFK-Auto-Solver/releases/latest").json()
        if version != response['tag_name']:
            tk.messagebox.showinfo("Newer Version Available", f"Latest version ({response['tag_name']}) have been released. Visit the repo for more info.\n\nRepo: https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver\n\nEnglish repo: https://github.com/Trisnox/Lost-Saga-AFK-Auto-Solver/tree/english")

    try:
        version_check()
    except requests.ConnectionError:
        print('Failed to check updates. Please check your connection.')


    def is_admin():
        try:
            is_admin = (os.getuid() == 0)
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin

    if not is_admin():
        tk.messagebox.showerror(title='Missing Perms', message='Program is not run with admin privileges. If program is not run with admin, it will unable to send input to the game. Please rerun script with admin privilege.')
        exit()

    window = tk.Tk()
    s = ttk.Style(window)

    s.configure('TFrame', background = '#0D1117')
    s.configure('TLabel', background = '#0D1117', foreground = '#E5E5E5')
    s.configure('TRadiobutton', background = '#0D1117', foreground = '#E5E5E5')
    s.configure('TEntry', background = '#0D1117', foreground = 'black')
    s.configure('TButton', background = '#0D1117')

    window.iconbitmap('img/sire icon.ico')
    window.title('AFK solver')
    tk.Grid.columnconfigure(window, 0, weight=1)
    tk.Grid.rowconfigure(window, 0, weight=1)

    mainframe = ttk.Frame(window)
    mainframe.grid(column=0, row=0, sticky=tk.N+tk.W+tk.E+tk.S)

    for row_index in range(10):
        tk.Grid.rowconfigure(mainframe, row_index, weight=1)
        for col_index in range(4):
            tk.Grid.columnconfigure(mainframe, col_index, weight=1)

    tesseract_label = ttk.Label(mainframe, compound=tk.RIGHT, text='Tesseract location')
    tesseract_label.grid(row=1, column=1, sticky=tk.E)

    tesseract_loc = tk.StringVar(value=config.get('tesseract', ''))

    tesseract_entry = ttk.Entry(mainframe, width=45, textvariable=tesseract_loc)
    tesseract_entry.grid(row=1, column=2, sticky=tk.W)

    browse = ttk.Button(mainframe, text='Browse',width=15, command=lambda:tesseract_set())
    browse.grid(row=1, column=3, sticky=tk.W)

    interval_input = tk.StringVar(value=config.get('interval', '5'))

    interval_label = ttk.Label(mainframe, text='Screenshot interval (in seconds)')
    interval_label.grid(row=2, column=1, sticky=tk.E)

    interval_entry = ttk.Entry(mainframe, width=5, textvariable=interval_input)
    interval_entry.grid(row=2, column=2, sticky=tk.W)

    interval_note = ttk.Label(mainframe, text='Enter 0 to screenshot\nimmediately but is not recommended', foreground='red', font=('', 7))
    interval_note.grid(row=2, column=3, sticky=tk.W+tk.S)

    ttk.Label(mainframe, text='').grid(row=3, column=1)

    fix_input = tk.StringVar(value=config.get('fix', 'n'))

    fix_label = ttk.Label(mainframe, text="Fix (for those input doesn't work\non this script but does work on jitbit macro recorder)")
    fix_label.configure(anchor='center')
    fix_label.grid(row=4, column=1)

    ttk.Radiobutton(mainframe, text='Keyboard', value='k', variable=fix_input).grid(row=5, column=1)
    ttk.Radiobutton(mainframe, text='None', value='n', variable=fix_input).grid(row=6, column=1)

    input_input = tk.StringVar(value=config.get('input', 'directinput'))

    input_label = ttk.Label(mainframe, text='Input type')
    input_label.grid(row=4, column=2)

    ttk.Radiobutton(mainframe, text='Default (Pynput)', value='default', variable=input_input).grid(row=5, column=2)
    ttk.Radiobutton(mainframe, text='DirectInput', value='directinput', variable=input_input).grid(row=6, column=2)

    window_input = tk.StringVar(value=config.get('window', 'window'))

    window_label = ttk.Label(mainframe, text='Window mode')
    window_label.grid(row=4, column=3)

    ttk.Radiobutton(mainframe, text='Fullscreen', value='full', variable=window_input).grid(row=5, column=3)
    ttk.Radiobutton(mainframe, text='Windowed', value='window', variable=window_input).grid(row=6, column=3)

    ttk.Label(mainframe, text='').grid(row=7, column=2)

    toggle_button = ttk.Button(mainframe, text='Start', width=15, command=lambda:toggle_script())
    toggle_button.grid(row=8, column=2)

    toggle_label = ttk.Label(mainframe, text='F6 shortcut to toggle start/stop', foreground='green')
    toggle_label.grid(row=8, column=3, sticky=tk.W)

    input_test_button = ttk.Button(mainframe, text='Input test', width=15, command=lambda:test_input_button())
    input_test_button.grid(row=8, column=1)

    ss_test_button = ttk.Button(mainframe, text='Screenshot test', width=15, command=lambda:test_screenshot())
    ss_test_button.grid(row=9, column=1)

    contact_info = ttk.Label(mainframe, text='Creator: trisnox (discord)\nFor assistance, you can ask through my support server https://discord.gg/GJ2P6u4edG')
    contact_info.grid(row=10, column=1, sticky=tk.W+tk.S)

    version_label = ttk.Label(mainframe, text='Version 0.4.1', foreground='blue', font=('', 7))
    version_label.grid(row=12, column=1, sticky=tk.W+tk.S)
    
    resolution_input = tk.StringVar(value=config.get('resolution', '1280x720'))

    reso_label = ttk.Label(mainframe, text='Window resolution')
    reso_label.grid(row=4, column=4)

    resolutions = ['800x600', '1024x768', '1280x720', '1280x1024', '1600x900', '1680x1050', '1920x1080']
    row_start = 4
    
    for x in resolutions:
        row_start += 1
        ttk.Radiobutton(mainframe, text=x, value=x, variable=resolution_input).grid(row=row_start, column=4)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=4, pady=10)

    listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    window.mainloop()
