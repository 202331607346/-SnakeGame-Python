import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import json
import os
from datetime import datetime

# 游戏配置 - 增大游戏区域
GRID_SIZE = 25  # 增大网格大小（像素）从20改为25
GRID_WIDTH = 30  # 网格宽度（30列）
GRID_HEIGHT = 20  # 网格高度（20行）
GAME_WIDTH = GRID_SIZE * GRID_WIDTH  # 750像素
GAME_HEIGHT = GRID_SIZE * GRID_HEIGHT  # 500像素

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.init_user_file()

    def init_user_file(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        else:
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        with open(self.users_file, 'w', encoding='utf-8') as f2:
                            json.dump([], f2)
            except:
                with open(self.users_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def register(self, username, password):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

            for user in users:
                if user.get('username') == username:
                    return False, "用户名已存在！"

            user_id = len(users) + 1
            users.append({
                'id': user_id,
                'username': username,
                'password': password
            })

            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)

            return True, "注册成功！"
        except Exception as e:
            print(f"注册错误: {e}")
            return False, f"注册失败：{str(e)}"

    def login(self, username, password):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

            for user in users:
                if isinstance(user, dict):
                    if user.get('username') == username and user.get('password') == password:
                        self.current_user = username
                        return True, f"登录成功！欢迎 {username}"

            return False, "用户名或密码错误！"
        except Exception as e:
            print(f"登录错误: {e}")
            return False, f"登录失败：{str(e)}"


class GameLogger:
    def __init__(self):
        self.log_file = "gamelog.json"
        self.init_log_file()

    def init_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        else:
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if not isinstance(data, list):
                        with open(self.log_file, 'w', encoding='utf-8') as f2:
                            json.dump([], f2)
            except:
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)

    def save_log(self, username, score, duration):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

            if not isinstance(logs, list):
                logs = []

            log_id = len(logs) + 1
            logs.append({
                'id': log_id,
                'username': username,
                'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'duration': duration,
                'score': score
            })

            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存日志错误: {e}")

    def get_user_logs(self, username=None):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)

            if not isinstance(logs, list):
                return []

            if username:
                logs = [log for log in logs if log.get('username') == username]

            return logs
        except:
            return []


class LoginRegisterWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("贪吃蛇游戏 - 登录/注册")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self.user_manager = UserManager()
        self.logger = GameLogger()

        self.center_window(self.window)
        self.create_widgets()

    def center_window(self, window):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (400 // 2)
        y = (window.winfo_screenheight() // 2) - (350 // 2)
        window.geometry(f'400x350+{x}+{y}')

    def create_widgets(self):
        title = tk.Label(self.window, text="贪吃蛇游戏", font=("Arial", 24, "bold"))
        title.pack(pady=30)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=40)

        login_btn = tk.Button(button_frame, text="登录", font=("Arial", 14),
                              width=15, height=2, command=self.show_login,
                              bg="#3498db", fg="white")
        login_btn.pack(pady=10)

        register_btn = tk.Button(button_frame, text="注册", font=("Arial", 14),
                                 width=15, height=2, command=self.show_register,
                                 bg="#2ecc71", fg="white")
        register_btn.pack(pady=10)

        exit_btn = tk.Button(button_frame, text="退出", font=("Arial", 14),
                             width=15, height=2, command=self.window.quit,
                             bg="#e74c3c", fg="white")
        exit_btn.pack(pady=10)

    def show_login(self):
        login_window = tk.Toplevel(self.window)
        login_window.title("登录")
        login_window.geometry("350x250")
        login_window.resizable(False, False)
        login_window.transient(self.window)
        login_window.grab_set()

        self.center_window(login_window)

        frame = tk.Frame(login_window, padx=30, pady=30)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="用户名:", font=("Arial", 12)).grid(row=0, column=0, pady=10, sticky="e")
        username_entry = tk.Entry(frame, font=("Arial", 12), width=18)
        username_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="密码:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="e")
        password_entry = tk.Entry(frame, font=("Arial", 12), width=18, show="*")
        password_entry.grid(row=1, column=1, pady=10)

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showerror("登录失败", "用户名和密码不能为空！")
                return

            success, msg = self.user_manager.login(username, password)
            if success:
                messagebox.showinfo("登录成功", msg)
                login_window.destroy()
                self.window.withdraw()
                self.start_game()
            else:
                messagebox.showerror("登录失败", msg)
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                username_entry.focus()

        def on_enter(event):
            do_login()

        username_entry.bind('<Return>', on_enter)
        password_entry.bind('<Return>', on_enter)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        login_btn = tk.Button(btn_frame, text="登录", font=("Arial", 12),
                              command=do_login, width=10, bg="#3498db", fg="white")
        login_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(btn_frame, text="取消", font=("Arial", 12),
                               command=login_window.destroy, width=10, bg="#95a5a6", fg="white")
        cancel_btn.pack(side=tk.LEFT, padx=10)

        username_entry.focus()

    def show_register(self):
        register_window = tk.Toplevel(self.window)
        register_window.title("注册")
        register_window.geometry("350x300")
        register_window.resizable(False, False)
        register_window.transient(self.window)
        register_window.grab_set()

        self.center_window(register_window)

        frame = tk.Frame(register_window, padx=30, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="用户名:", font=("Arial", 12)).grid(row=0, column=0, pady=8, sticky="e")
        username_entry = tk.Entry(frame, font=("Arial", 12), width=18)
        username_entry.grid(row=0, column=1, pady=8)

        tk.Label(frame, text="密码:", font=("Arial", 12)).grid(row=1, column=0, pady=8, sticky="e")
        password_entry = tk.Entry(frame, font=("Arial", 12), width=18, show="*")
        password_entry.grid(row=1, column=1, pady=8)

        tk.Label(frame, text="确认密码:", font=("Arial", 12)).grid(row=2, column=0, pady=8, sticky="e")
        confirm_entry = tk.Entry(frame, font=("Arial", 12), width=18, show="*")
        confirm_entry.grid(row=2, column=1, pady=8)

        def do_register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()

            if not username or not password:
                messagebox.showerror("注册失败", "用户名和密码不能为空！")
                return

            if len(username) < 3:
                messagebox.showerror("注册失败", "用户名长度不能少于3个字符！")
                return

            if len(password) < 3:
                messagebox.showerror("注册失败", "密码长度不能少于3个字符！")
                return

            if password != confirm:
                messagebox.showerror("注册失败", "两次输入的密码不一致！")
                password_entry.delete(0, tk.END)
                confirm_entry.delete(0, tk.END)
                password_entry.focus()
                return

            success, msg = self.user_manager.register(username, password)
            if success:
                messagebox.showinfo("注册成功", msg + "\n请返回登录")
                register_window.destroy()
            else:
                messagebox.showerror("注册失败", msg)
                username_entry.delete(0, tk.END)
                username_entry.focus()

        def on_enter(event):
            do_register()

        username_entry.bind('<Return>', on_enter)
        password_entry.bind('<Return>', on_enter)
        confirm_entry.bind('<Return>', on_enter)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        register_btn = tk.Button(btn_frame, text="注册", font=("Arial", 12),
                                 command=do_register, width=10, bg="#2ecc71", fg="white")
        register_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(btn_frame, text="取消", font=("Arial", 12),
                               command=register_window.destroy, width=10, bg="#95a5a6", fg="white")
        cancel_btn.pack(side=tk.LEFT, padx=10)

        username_entry.focus()

    def start_game(self):
        game = SnakeGame(self.user_manager.current_user, self.user_manager, self.logger)
        game.run()

    def run(self):
        self.window.mainloop()


class SnakeGame:
    def __init__(self, username, user_manager, logger):
        self.username = username
        self.user_manager = user_manager
        self.logger = logger

        self.window = tk.Tk()
        self.window.title(f"贪吃蛇游戏 - 玩家: {username}")
        self.window.resizable(False, False)

        # 设置窗口大小 - 增大右侧面板宽度
        right_panel_width = 280  # 从200增加到280
        window_width = GAME_WIDTH + right_panel_width
        window_height = GAME_HEIGHT + 20  # 增加一点高度

        # 设置窗口居中
        self.center_window(self.window, window_width, window_height)

        # 创建画布
        self.canvas = tk.Canvas(self.window, width=GAME_WIDTH, height=GAME_HEIGHT, bg='black')
        self.canvas.pack(side=tk.LEFT)

        # 让画布获得焦点
        self.canvas.focus_set()

        # 右侧信息面板 - 增大宽度
        self.info_frame = tk.Frame(self.window, width=right_panel_width, height=GAME_HEIGHT, bg='#2c3e50')
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_frame.pack_propagate(False)

        self.create_info_panel()

        # 游戏变量
        self.snake = []
        self.food = None
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.add_score = 10
        self.game_running = True
        self.game_paused = False
        self.game_start_time = None
        self.speed = 100
        self.after_id = None

        # 绑定键盘事件
        self.canvas.bind('<Up>', self.on_up)
        self.canvas.bind('<Down>', self.on_down)
        self.canvas.bind('<Left>', self.on_left)
        self.canvas.bind('<Right>', self.on_right)
        self.canvas.bind('<space>', self.on_space)
        self.canvas.bind('<Escape>', self.on_escape)

        # 使用字母键
        self.canvas.bind('a', self.on_speed_up)
        self.canvas.bind('d', self.on_speed_down)
        self.canvas.bind('l', self.on_show_logs)
        self.canvas.bind('r', self.on_restart)

        # 大写字母也绑定
        self.canvas.bind('A', self.on_speed_up)
        self.canvas.bind('D', self.on_speed_down)
        self.canvas.bind('L', self.on_show_logs)
        self.canvas.bind('R', self.on_restart)

        # 同时绑定到窗口作为备用
        self.window.bind('<Up>', self.on_up)
        self.window.bind('<Down>', self.on_down)
        self.window.bind('<Left>', self.on_left)
        self.window.bind('<Right>', self.on_right)
        self.window.bind('<space>', self.on_space)
        self.window.bind('<Escape>', self.on_escape)
        self.window.bind('a', self.on_speed_up)
        self.window.bind('d', self.on_speed_down)
        self.window.bind('l', self.on_show_logs)
        self.window.bind('r', self.on_restart)
        self.window.bind('A', self.on_speed_up)
        self.window.bind('D', self.on_speed_down)
        self.window.bind('L', self.on_show_logs)
        self.window.bind('R', self.on_restart)

        # 窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.init_game()

    def create_hint_labels(self):
        """创建提示标签"""
        hint_frame = tk.Frame(self.info_frame, bg='#2c3e50')
        hint_frame.pack(pady=10, fill=tk.X)

        tk.Label(hint_frame, text="=" * 20, font=("Arial", 8),
                 fg='#f39c12', bg='#2c3e50').pack()
        tk.Label(hint_frame, text="快捷键",
                 font=("Arial", 11, "bold"), fg='#f39c12', bg='#2c3e50').pack()

        hints = [
            "↑ ↓ ← → : 移动",
            "A 键 : 加速",
            "D 键 : 减速",
            "L 键 : 查看日志",
            "R 键 : 重新开始",
            "空格 : 暂停/继续",
            "ESC : 退出游戏"
        ]

        for hint in hints:
            tk.Label(hint_frame, text=hint, font=("Arial", 10),
                     fg='#bdc3c7', bg='#2c3e50').pack(anchor='w', padx=15, pady=3)

        tk.Label(hint_frame, text="=" * 20, font=("Arial", 8),
                 fg='#f39c12', bg='#2c3e50').pack(pady=5)

        tk.Label(hint_frame, text="提示：点击游戏区域",
                 font=("Arial", 9), fg='#e74c3c', bg='#2c3e50').pack()
        tk.Label(hint_frame, text="后使用键盘",
                 font=("Arial", 9), fg='#e74c3c', bg='#2c3e50').pack()

    def on_up(self, event):
        if self.game_running and not self.game_paused:
            if self.direction != DOWN:
                self.next_direction = UP
                return "break"

    def on_down(self, event):
        if self.game_running and not self.game_paused:
            if self.direction != UP:
                self.next_direction = DOWN
                return "break"

    def on_left(self, event):
        if self.game_running and not self.game_paused:
            if self.direction != RIGHT:
                self.next_direction = LEFT
                return "break"

    def on_right(self, event):
        if self.game_running and not self.game_paused:
            if self.direction != LEFT:
                self.next_direction = RIGHT
                return "break"

    def on_space(self, event):
        self.toggle_pause()
        return "break"

    def on_escape(self, event):
        self.end_game()
        return "break"

    def on_speed_up(self, event):
        if self.game_running:
            if self.speed > 50:
                self.speed -= 20
                self.add_score += 2
                self.update_score_display()
                self.show_temp_message(f"加速！速度: {(350 - self.speed) // 30 + 1}/10")
        return "break"

    def on_speed_down(self, event):
        if self.game_running:
            if self.speed < 350:
                self.speed += 20
                self.add_score -= 2
                if self.add_score < 1:
                    self.add_score = 1
                self.update_score_display()
                self.show_temp_message(f"减速！速度: {(350 - self.speed) // 30 + 1}/10")
        return "break"

    def on_show_logs(self, event):
        self.show_game_logs()
        return "break"

    def on_restart(self, event):
        if messagebox.askyesno("重新开始", "确定要重新开始游戏吗？"):
            self.restart_game()
        return "break"

    def show_temp_message(self, message):
        """显示临时消息"""
        # 移除之前的临时消息
        for widget in self.info_frame.winfo_children():
            if isinstance(widget, tk.Label) and hasattr(widget, 'temp_message'):
                widget.destroy()

        temp_label = tk.Label(self.info_frame, text=message, font=("Arial", 10),
                              fg='#2ecc71', bg='#2c3e50')
        temp_label.temp_message = True
        temp_label.pack(pady=5)
        self.window.after(1000, temp_label.destroy)

    def center_window(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def create_info_panel(self):
        # 玩家信息 - 加大字体
        tk.Label(self.info_frame, text=f"玩家: {self.username}",
                 font=("Arial", 16, "bold"), fg='white', bg='#2c3e50').pack(pady=15)

        # 分隔线
        tk.Frame(self.info_frame, height=2, bg='white').pack(fill=tk.X, padx=20)

        # 得分信息
        self.score_label = tk.Label(self.info_frame, text="得分: 0",
                                    font=("Arial", 18), fg='#f1c40f', bg='#2c3e50')
        self.score_label.pack(pady=15)

        self.add_score_label = tk.Label(self.info_frame, text="每食物得分: 10",
                                        font=("Arial", 12), fg='#3498db', bg='#2c3e50')
        self.add_score_label.pack(pady=5)

        self.speed_label = tk.Label(self.info_frame, text="速度: 5/10",
                                    font=("Arial", 12), fg='#e74c3c', bg='#2c3e50')
        self.speed_label.pack(pady=5)

        self.status_label = tk.Label(self.info_frame, text="游戏状态: 运行中",
                                     font=("Arial", 12), fg='#2ecc71', bg='#2c3e50')
        self.status_label.pack(pady=15)

        # 操作说明标题
        tk.Label(self.info_frame, text="操作说明", font=("Arial", 14, "bold"),
                 fg='white', bg='#2c3e50').pack(pady=10)

        # 操作说明列表
        instructions_frame = tk.Frame(self.info_frame, bg='#2c3e50')
        instructions_frame.pack(fill=tk.X, padx=15)

        instructions = [
            ("↑ ↓ ← →", "移动"),
            ("A / D", "加速/减速"),
            ("L", "查看日志"),
            ("R", "重新开始"),
            ("Space", "暂停/继续"),
            ("ESC", "退出游戏")
        ]

        for key, func in instructions:
            frame = tk.Frame(instructions_frame, bg='#2c3e50')
            frame.pack(fill=tk.X, pady=3)
            tk.Label(frame, text=key, font=("Arial", 10, "bold"),
                     fg='#f1c40f', bg='#2c3e50', width=12, anchor='w').pack(side=tk.LEFT)
            tk.Label(frame, text=func, font=("Arial", 10),
                     fg='#bdc3c7', bg='#2c3e50', anchor='w').pack(side=tk.LEFT)

        # 快捷键提示
        self.create_hint_labels()

    def update_speed_display(self):
        speed_level = int((350 - self.speed) / 30) + 1
        if speed_level < 1:
            speed_level = 1
        if speed_level > 10:
            speed_level = 10
        self.speed_label.config(text=f"速度: {speed_level}/10")

    def init_game(self):
        # 初始化蛇（5个节点）
        start_x = GAME_WIDTH // 2 // GRID_SIZE * GRID_SIZE
        start_y = GAME_HEIGHT // 2 // GRID_SIZE * GRID_SIZE

        self.snake = [
            [start_x, start_y],
            [start_x - GRID_SIZE, start_y],
            [start_x - 2 * GRID_SIZE, start_y],
            [start_x - 3 * GRID_SIZE, start_y],
            [start_x - 4 * GRID_SIZE, start_y]
        ]

        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.add_score = 10
        self.speed = 200
        self.game_running = True
        self.game_paused = False
        self.game_start_time = time.time()

        self.update_score_display()
        self.update_speed_display()
        self.create_food()
        self.draw()

        # 开始游戏循环
        if self.after_id:
            self.window.after_cancel(self.after_id)
        self.game_loop()

    def create_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE

            if [x, y] not in self.snake:
                self.food = [x, y]
                break

    def draw(self):
        self.canvas.delete("all")

        # 绘制网格线
        for i in range(GRID_WIDTH):
            self.canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, GAME_HEIGHT, fill='#333333')
        for i in range(GRID_HEIGHT):
            self.canvas.create_line(0, i * GRID_SIZE, GAME_WIDTH, i * GRID_SIZE, fill='#333333')

        # 绘制食物
        if self.food:
            self.canvas.create_rectangle(self.food[0], self.food[1],
                                         self.food[0] + GRID_SIZE - 1,
                                         self.food[1] + GRID_SIZE - 1,
                                         fill='red', outline='red')

        # 绘制蛇
        for i, segment in enumerate(self.snake):
            color = '#2ecc71' if i == 0 else '#27ae60'
            self.canvas.create_rectangle(segment[0], segment[1],
                                         segment[0] + GRID_SIZE - 1,
                                         segment[1] + GRID_SIZE - 1,
                                         fill=color, outline=color)

        # 绘制眼睛
        if len(self.snake) > 0:
            head = self.snake[0]
            eye_offset = GRID_SIZE // 4
            if self.direction == RIGHT:
                self.canvas.create_oval(head[0] + GRID_SIZE - eye_offset - 2, head[1] + eye_offset,
                                        head[0] + GRID_SIZE - eye_offset + 2, head[1] + eye_offset + 4, fill='white')
                self.canvas.create_oval(head[0] + GRID_SIZE - eye_offset - 2, head[1] + GRID_SIZE - eye_offset - 4,
                                        head[0] + GRID_SIZE - eye_offset + 2, head[1] + GRID_SIZE - eye_offset,
                                        fill='white')
            elif self.direction == LEFT:
                self.canvas.create_oval(head[0] + eye_offset - 2, head[1] + eye_offset,
                                        head[0] + eye_offset + 2, head[1] + eye_offset + 4, fill='white')
                self.canvas.create_oval(head[0] + eye_offset - 2, head[1] + GRID_SIZE - eye_offset - 4,
                                        head[0] + eye_offset + 2, head[1] + GRID_SIZE - eye_offset, fill='white')
            elif self.direction == UP:
                self.canvas.create_oval(head[0] + eye_offset, head[1] + eye_offset - 2,
                                        head[0] + eye_offset + 4, head[1] + eye_offset + 2, fill='white')
                self.canvas.create_oval(head[0] + GRID_SIZE - eye_offset - 4, head[1] + eye_offset - 2,
                                        head[0] + GRID_SIZE - eye_offset, head[1] + eye_offset + 2, fill='white')
            else:  # DOWN
                self.canvas.create_oval(head[0] + eye_offset, head[1] + GRID_SIZE - eye_offset - 2,
                                        head[0] + eye_offset + 4, head[1] + GRID_SIZE - eye_offset + 2, fill='white')
                self.canvas.create_oval(head[0] + GRID_SIZE - eye_offset - 4, head[1] + GRID_SIZE - eye_offset - 2,
                                        head[0] + GRID_SIZE - eye_offset, head[1] + GRID_SIZE - eye_offset + 2,
                                        fill='white')

    def update_score_display(self):
        self.score_label.config(text=f"得分: {self.score}")
        self.add_score_label.config(text=f"每食物得分: {self.add_score}")
        self.update_speed_display()

    def move(self):
        if not self.game_running or self.game_paused:
            return

        self.direction = self.next_direction

        head = self.snake[0]
        new_head = [head[0] + self.direction[0] * GRID_SIZE,
                    head[1] + self.direction[1] * GRID_SIZE]

        # 检查是否吃到食物
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += self.add_score
            self.update_score_display()
            self.create_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        # 检查碰撞
        if self.check_collision():
            self.end_game()

    def check_collision(self):
        head = self.snake[0]

        if (head[0] < 0 or head[0] >= GAME_WIDTH or
                head[1] < 0 or head[1] >= GAME_HEIGHT):
            self.status_label.config(text="游戏状态: 撞墙了", fg='#e74c3c')
            return True

        if head in self.snake[1:]:
            self.status_label.config(text="游戏状态: 咬到自己了", fg='#e74c3c')
            return True

        return False

    def toggle_pause(self):
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.status_label.config(text="游戏状态: 已暂停", fg='#f39c12')
            else:
                self.status_label.config(text="游戏状态: 运行中", fg='#2ecc71')
                self.game_loop()

    def show_game_logs(self):
        logs = self.logger.get_user_logs(self.username)

        if not logs:
            messagebox.showinfo("游戏日志", "暂无游戏记录")
            return

        log_window = tk.Toplevel(self.window)
        log_window.title(f"{self.username} 的游戏日志")
        log_window.geometry("700x450")

        self.center_window(log_window, 700, 450)

        tree_frame = tk.Frame(log_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ('ID', '用户名', '开始时间', '时长(秒)', '得分')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                            yscrollcommand=scrollbar.set)

        column_widths = {'ID': 50, '用户名': 100, '开始时间': 150, '时长(秒)': 80, '得分': 80}
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths.get(col, 100))

        scrollbar.config(command=tree.yview)

        for log in logs:
            tree.insert('', 'end', values=(log.get('id', ''), log.get('username', ''),
                                           log.get('start_time', ''), log.get('duration', ''),
                                           log.get('score', '')))

        tree.pack(fill=tk.BOTH, expand=True)

        close_btn = tk.Button(log_window, text="关闭", command=log_window.destroy)
        close_btn.pack(pady=10)

    def end_game(self):
        if self.game_running:
            self.game_running = False
            if self.after_id:
                self.window.after_cancel(self.after_id)

            duration = int(time.time() - self.game_start_time)
            self.logger.save_log(self.username, self.score, duration)

            result = messagebox.askyesno("游戏结束",
                                         f"游戏结束！\n得分: {self.score}\n游戏时长: {duration}秒\n\n日志已保存！\n\n是否重新开始？")

            if result:
                self.restart_game()
            else:
                self.on_closing()

    def restart_game(self):
        # 重置游戏变量
        self.init_game()

    def on_closing(self):
        if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
            if self.after_id:
                self.window.after_cancel(self.after_id)
            self.window.quit()
            self.window.destroy()

    def game_loop(self):
        if self.game_running and not self.game_paused:
            self.move()
            self.draw()
            self.after_id = self.window.after(self.speed, self.game_loop)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = LoginRegisterWindow()
    app.run()