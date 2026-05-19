import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import json
import os
from datetime import datetime

# ====================== 游戏配置 ======================
GRID_SIZE = 25
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_WIDTH = GRID_SIZE * GRID_WIDTH
GAME_HEIGHT = GRID_SIZE * GRID_HEIGHT

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# ====================== 用户管理 ======================
class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.init_user_file()

    def init_user_file(self):
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def register(self, username, password):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            for u in users:
                if u['username'] == username:
                    return False, "用户名已存在"
            users.append({"id": len(users) + 1, "username": username, "password": password})
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            return True, "注册成功"
        except Exception as e:
            print("注册错误:", e)
            return False, "注册失败"

    def login(self, username, password):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            for u in users:
                if u['username'] == username and u['password'] == password:
                    self.current_user = username
                    return True, "登录成功"
            return False, "账号或密码错误"
        except Exception as e:
            print("登录错误:", e)
            return False, "登录失败"


# ====================== 日志记录 ======================
class GameLogger:
    def __init__(self):
        self.log_file = "gamelog.json"
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save(self, user, score, duration):
        """保存游戏记录"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            logs = []

        # 获取下一个ID
        next_id = 1
        if logs:
            next_id = max(log.get('id', 0) for log in logs) + 1

        logs.append({
            "id": next_id,
            "username": user,
            "score": score,
            "duration": duration,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print("日志保存失败:", e)
            return False

    def get_logs(self, user):
        """获取用户的所有游戏记录"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            user_logs = [l for l in logs if l.get('username') == user]
            # 按ID倒序排列（最新的在前）
            user_logs.sort(key=lambda x: x.get('id', 0), reverse=True)
            return user_logs
        except Exception as e:
            print("读取日志失败:", e)
            return []


# ====================== 登录界面 ======================
class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("贪吃蛇 - 登录")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.um = UserManager()
        self.gl = GameLogger()
        self.center_window()
        self.ui()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f'400x300+{x}+{y}')

    def ui(self):
        tk.Label(self.root, text="🐍 贪吃蛇游戏", font=("黑体", 22, "bold")).pack(pady=20)
        f = tk.Frame(self.root)
        f.pack(pady=10)
        tk.Label(f, text="账号:", font=("黑体", 14)).grid(row=0, column=0, pady=8)
        self.user_entry = tk.Entry(f, font=("黑体", 14), width=15)
        self.user_entry.grid(row=0, column=1, padx=5)

        tk.Label(f, text="密码:", font=("黑体", 14)).grid(row=1, column=0, pady=8)
        self.pwd_entry = tk.Entry(f, font=("黑体", 14), show="*", width=15)
        self.pwd_entry.grid(row=1, column=1, padx=5)

        bf = tk.Frame(self.root)
        bf.pack(pady=20)
        tk.Button(bf, text="登录", font=("黑体", 13), width=10,
                  bg="#3498db", fg="white", command=self.login).grid(row=0, column=0, padx=10)
        tk.Button(bf, text="注册", font=("黑体", 13), width=10,
                  bg="#2ecc71", fg="white", command=self.register).grid(row=0, column=1, padx=10)

        # 绑定回车键
        self.user_entry.bind('<Return>', lambda e: self.login())
        self.pwd_entry.bind('<Return>', lambda e: self.login())

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pwd_entry.get().strip()
        if not u or not p:
            messagebox.showwarning("提示", "请输入账号和密码")
            return
        ok, msg = self.um.login(u, p)
        if ok:
            self.root.destroy()
            GameMain(u, self.um, self.gl)
        else:
            messagebox.showerror("错误", msg)

    def register(self):
        u = self.user_entry.get().strip()
        p = self.pwd_entry.get().strip()
        if not u or not p:
            messagebox.showwarning("提示", "请输入账号和密码")
            return
        if len(u) < 3:
            messagebox.showwarning("提示", "用户名长度不能少于3个字符")
            return
        if len(p) < 3:
            messagebox.showwarning("提示", "密码长度不能少于3个字符")
            return
        ok, msg = self.um.register(u, p)
        if ok:
            messagebox.showinfo("成功", msg)
            self.user_entry.delete(0, tk.END)
            self.pwd_entry.delete(0, tk.END)
        else:
            messagebox.showerror("失败", msg)

    def run(self):
        self.root.mainloop()


# ====================== 游戏主类 ======================
class GameMain:
    def __init__(self, username, um, gl):
        self.username = username
        self.um = um
        self.gl = gl

        self.win = tk.Tk()
        self.win.title(f"🐍 贪吃蛇 - {username}")
        self.win.resizable(False, False)

        PANEL_W = 260
        total_w = GAME_WIDTH + PANEL_W
        total_h = GAME_HEIGHT

        # 窗口居中
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f"{total_w}x{total_h}+{(sw - total_w) // 2}+{(sh - total_h) // 2}")

        # 游戏画布
        self.canvas = tk.Canvas(self.win, bg="#111", width=GAME_WIDTH, height=GAME_HEIGHT)
        self.canvas.pack(side="left")

        # 右侧面板
        self.panel = tk.Frame(self.win, width=PANEL_W, height=GAME_HEIGHT, bg="#2c3e50")
        self.panel.pack(side="right", fill="y")
        self.panel.pack_propagate(False)

        # 游戏变量
        self.snake = []
        self.food = []
        self.dir = RIGHT
        self.next_dir = RIGHT
        self.score = 0
        self.running = True
        self.paused = False
        self.speed = 150
        self.timer = None
        self.start_time = time.time()

        self.build_ui()
        self.bind_keys()
        self.init_snake()
        self.create_food()
        self.draw()
        self.game_loop()

        # 让画布获得焦点
        self.canvas.focus_set()

        # 窗口关闭时的处理
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.win.mainloop()

    def build_ui(self):
        # 标题
        tk.Label(self.panel, text="🐍 贪吃蛇", font=("黑体", 20, "bold"),
                 fg="#f1c40f", bg="#2c3e50").pack(pady=10)

        # 玩家信息
        tk.Label(self.panel, text=f"玩家：{self.username}",
                 font=("黑体", 14), fg="white", bg="#2c3e50").pack(pady=5)

        # 分隔线
        tk.Frame(self.panel, height=2, bg="#f1c40f").pack(fill="x", padx=30, pady=8)

        # 游戏数据
        self.score_label = tk.Label(self.panel, text="得分：0",
                                    font=("黑体", 18, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.score_label.pack(pady=8)

        self.speed_label = tk.Label(self.panel, text="速度：5/10",
                                    font=("黑体", 14), fg="#3498db", bg="#2c3e50")
        self.speed_label.pack(pady=5)

        self.state_label = tk.Label(self.panel, text="✅ 运行中",
                                    font=("黑体", 13, "bold"), fg="#2ecc71", bg="#2c3e50")
        self.state_label.pack(pady=10)

        # 分隔线
        tk.Frame(self.panel, height=2, bg="#f1c40f").pack(fill="x", padx=30, pady=8)

        # 操作说明
        tk.Label(self.panel, text="🎮 操作说明", font=("黑体", 15, "bold"),
                 fg="white", bg="#2c3e50").pack(pady=8)

        tips = [
            "↑ ↓ ← → : 移动",
            "空格 : 暂停/继续",
            "A : 加速",
            "D : 减速",
            "R : 重新开始",
            "L : 查看记录",
            "ESC : 退出游戏"
        ]
        for t in tips:
            tk.Label(self.panel, text=t, font=("黑体", 11),
                     fg="#bdc3c7", bg="#2c3e50", anchor="w").pack(pady=2, padx=20)

    def init_snake(self):
        cx = GAME_WIDTH // 2
        cy = GAME_HEIGHT // 2
        self.snake = [
            [cx, cy],
            [cx - GRID_SIZE, cy],
            [cx - GRID_SIZE * 2, cy],
            [cx - GRID_SIZE * 3, cy]
        ]
        self.dir = RIGHT
        self.next_dir = RIGHT
        self.score = 0
        self.speed = 150
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.update_ui()

    def create_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if [x, y] not in self.snake:
                self.food = [x, y]
                break

    def move(self):
        if not self.running or self.paused:
            return

        self.dir = self.next_dir
        head = self.snake[0]
        nx = head[0] + self.dir[0] * GRID_SIZE
        ny = head[1] + self.dir[1] * GRID_SIZE
        new_head = [nx, ny]

        # 吃到食物
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 10
            self.create_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        # 碰撞检测
        if self.check_dead():
            self.game_over()
            return

        self.draw()
        self.update_ui()

    def check_dead(self):
        h = self.snake[0]
        # 边界碰撞
        if h[0] < 0 or h[0] >= GAME_WIDTH or h[1] < 0 or h[1] >= GAME_HEIGHT:
            return True
        # 自身碰撞
        if h in self.snake[1:]:
            return True
        return False

    def draw(self):
        self.canvas.delete("all")

        # 绘制网格
        for i in range(GRID_WIDTH):
            self.canvas.create_line(i * GRID_SIZE, 0, i * GRID_SIZE, GAME_HEIGHT, fill="#222")
        for i in range(GRID_HEIGHT):
            self.canvas.create_line(0, i * GRID_SIZE, GAME_WIDTH, i * GRID_SIZE, fill="#222")

        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            color = "#2ecc71" if i == 0 else "#27ae60"
            self.canvas.create_rectangle(x, y, x + GRID_SIZE - 1, y + GRID_SIZE - 1,
                                         fill=color, outline=color)

        # 绘制食物
        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx + GRID_SIZE - 1, fy + GRID_SIZE - 1,
                                    fill="#e74c3c", outline="#e74c3c")

    def update_ui(self):
        self.score_label.config(text=f"得分：{self.score}")
        # 速度等级：speed 50~250，对应等级10~1
        level = max(1, min(10, 11 - (self.speed - 50) // 20))
        self.speed_label.config(text=f"速度：{level}/10")

    def bind_keys(self):
        # 方向键
        self.win.bind("<Up>", lambda e: self.change_dir(UP))
        self.win.bind("<Down>", lambda e: self.change_dir(DOWN))
        self.win.bind("<Left>", lambda e: self.change_dir(LEFT))
        self.win.bind("<Right>", lambda e: self.change_dir(RIGHT))
        # 功能键
        self.win.bind("<space>", lambda e: self.toggle_pause())
        self.win.bind("<Escape>", lambda e: self.quit_game())
        self.win.bind("a", lambda e: self.change_speed(-20))
        self.win.bind("A", lambda e: self.change_speed(-20))
        self.win.bind("d", lambda e: self.change_speed(20))
        self.win.bind("D", lambda e: self.change_speed(20))
        self.win.bind("r", lambda e: self.restart())
        self.win.bind("R", lambda e: self.restart())
        self.win.bind("l", lambda e: self.show_log())
        self.win.bind("L", lambda e: self.show_log())

    def change_dir(self, d):
        if (d == UP and self.dir != DOWN) or \
                (d == DOWN and self.dir != UP) or \
                (d == LEFT and self.dir != RIGHT) or \
                (d == RIGHT and self.dir != LEFT):
            self.next_dir = d

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.state_label.config(text="⏸ 已暂停", fg="#f39c12")
        else:
            self.state_label.config(text="✅ 运行中", fg="#2ecc71")
            self.game_loop()

    def change_speed(self, v):
        new_speed = self.speed + v
        if 50 <= new_speed <= 250:
            self.speed = new_speed
            self.update_ui()

    def restart(self):
        if self.timer:
            self.win.after_cancel(self.timer)
        self.init_snake()
        self.create_food()
        self.draw()
        self.running = True
        self.paused = False
        self.state_label.config(text="✅ 运行中", fg="#2ecc71")
        self.game_loop()

    def show_log(self):
        """显示游戏记录窗口"""
        logs = self.gl.get_logs(self.username)

        if not logs:
            messagebox.showinfo("游戏记录", "暂无游戏记录")
            return

        # 创建日志窗口
        top = tk.Toplevel(self.win)
        top.title(f"{self.username} 的游戏记录")
        top.geometry("600x450")
        top.resizable(False, False)

        # 窗口居中
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (600 // 2)
        y = (top.winfo_screenheight() // 2) - (450 // 2)
        top.geometry(f'600x450+{x}+{y}')

        # 标题
        tk.Label(top, text=f"📊 {self.username} 的游戏记录",
                 font=("黑体", 16, "bold"), fg="#2c3e50").pack(pady=10)

        # 创建表格
        frame = tk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(frame, columns=("id", "time", "score", "duration"),
                            show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        # 设置列标题
        tree.heading("id", text="序号")
        tree.heading("time", text="游戏时间")
        tree.heading("score", text="得分")
        tree.heading("duration", text="游戏时长(秒)")

        # 设置列宽和居中
        tree.column("id", width=60, anchor="center")
        tree.column("time", width=180, anchor="center")
        tree.column("score", width=100, anchor="center")
        tree.column("duration", width=100, anchor="center")

        # 插入数据
        for log in logs:
            tree.insert("", "end", values=(
                log.get("id", ""),
                log.get("time", ""),
                log.get("score", 0),
                log.get("duration", 0)
            ))

        tree.pack(fill=tk.BOTH, expand=True)

        # 底部统计信息
        total_games = len(logs)
        total_score = sum(log.get("score", 0) for log in logs)
        avg_score = total_score // total_games if total_games > 0 else 0
        max_score = max((log.get("score", 0) for log in logs), default=0)

        info_frame = tk.Frame(top, bg="#ecf0f1")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(info_frame, text=f"总局数：{total_games}",
                 font=("黑体", 12), bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text=f"总分：{total_score}",
                 font=("黑体", 12), bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text=f"平均分：{avg_score}",
                 font=("黑体", 12), bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, text=f"最高分：{max_score}",
                 font=("黑体", 12), bg="#ecf0f1", fg="#e74c3c").pack(side=tk.LEFT, padx=20)

        # 按钮框架
        btn_frame = tk.Frame(top)
        btn_frame.pack(pady=10)

        close_btn = tk.Button(btn_frame, text="关闭", font=("黑体", 12),
                              command=top.destroy, bg="#3498db", fg="white", width=10)
        close_btn.pack(side=tk.LEFT, padx=10)

        # 如果游戏已结束，添加一个"返回游戏"按钮（但游戏已结束，实际是重新开始）
        if not self.running:
            restart_btn = tk.Button(btn_frame, text="重新开始", font=("黑体", 12),
                                    command=lambda: [top.destroy(), self.restart()],
                                    bg="#2ecc71", fg="white", width=10)
            restart_btn.pack(side=tk.LEFT, padx=10)

    def show_game_over_dialog(self):
        """显示游戏结束对话框，包含更多选项"""
        # 创建一个自定义对话框
        dialog = tk.Toplevel(self.win)
        dialog.title("游戏结束")
        dialog.geometry("350x250")
        dialog.resizable(False, False)
        dialog.transient(self.win)
        dialog.grab_set()

        # 居中
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f'350x250+{x}+{y}')

        # 内容
        tk.Label(dialog, text="🎮 游戏结束", font=("黑体", 18, "bold"),
                 fg="#e74c3c").pack(pady=15)

        tk.Label(dialog, text=f"🐍 得分：{self.score}",
                 font=("黑体", 14), fg="#2c3e50").pack(pady=5)

        cost = int(time.time() - self.start_time)
        tk.Label(dialog, text=f"⏱️ 游戏时长：{cost} 秒",
                 font=("黑体", 14), fg="#2c3e50").pack(pady=5)

        tk.Label(dialog, text="", font=("黑体", 10)).pack(pady=5)

        # 按钮
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=15)

        # 重新开始按钮
        restart_btn = tk.Button(btn_frame, text="重新开始", font=("黑体", 12),
                                command=lambda: [dialog.destroy(), self.restart()],
                                bg="#2ecc71", fg="white", width=10)
        restart_btn.pack(side=tk.LEFT, padx=8)

        # 查看日志按钮
        log_btn = tk.Button(btn_frame, text="查看日志", font=("黑体", 12),
                            command=lambda: [dialog.destroy(), self.show_log()],
                            bg="#3498db", fg="white", width=10)
        log_btn.pack(side=tk.LEFT, padx=8)

        # 退出游戏按钮
        exit_btn = tk.Button(btn_frame, text="退出游戏", font=("黑体", 12),
                             command=lambda: [dialog.destroy(), self.quit_game()],
                             bg="#e74c3c", fg="white", width=10)
        exit_btn.pack(side=tk.LEFT, padx=8)

    def game_over(self):
        """游戏结束处理"""
        if self.timer:
            self.win.after_cancel(self.timer)
        self.running = False

        # 保存游戏记录
        cost = int(time.time() - self.start_time)
        self.gl.save(self.username, self.score, cost)

        # 更新状态标签
        self.state_label.config(text="💀 游戏结束", fg="#e74c3c")

        # 显示自定义游戏结束对话框
        self.show_game_over_dialog()

    def on_closing(self):
        """窗口关闭时的处理"""
        if messagebox.askokcancel("退出", "确定要退出游戏吗？"):
            if self.timer:
                self.win.after_cancel(self.timer)
            self.win.destroy()

    def quit_game(self):
        """退出游戏"""
        if self.timer:
            self.win.after_cancel(self.timer)
        self.win.destroy()

    def game_loop(self):
        if self.running and not self.paused:
            self.move()
            self.timer = self.win.after(self.speed, self.game_loop)


if __name__ == "__main__":
    app = LoginWindow()
    app.run()