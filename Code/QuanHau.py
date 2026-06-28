import tkinter as tk
from tkinter import ttk

N = 8
board = [-1] * N  # board[i] = j: hàng i, quân hậu đặt ở cột j
generator = None
running = False
paused = False
step_count = 0
backtrack_count = 0

def is_safe(r, c):
    for i in range(r):
        if board[i] == c or abs(board[i] - c) == abs(i - r):
            """khoang cach hang giua 2 ô bằng với khoảng cách giữa các cột"""
            return False
    return True

def solve_n_queens(row):
    if row == N:
        return True 
    for col in range(N):
        yield {"r": row, "c": col, "status": "try"}
        if is_safe(row, col):
            board[row] = col
            yield {"r": row, "c": col, "status": "place"}
            if (yield from solve_n_queens(row + 1)):
                return True
            board[row] = -1
            yield {"r": row, "c": col, "status": "backtrack"}

# --- GIAO DIỆN & LOGIC ---
def draw_board(active_r=-1, active_c=-1, status=""):
    canvas.delete("all")
    w = 400 / N
    font_size = max(8, int(w * 0.55))  

    for r in range(N):
        for c in range(N):
            color = "white" if (r + c) % 2 == 0 else "#c8d8e8"
            if r == active_r and c == active_c:
                if status == "try":       color = "#ffe066"
                elif status == "backtrack": color = "#ff6b6b"
            x0, y0 = c * w, r * w
            canvas.create_rectangle(x0, y0, x0 + w, y0 + w, fill=color, outline="#888")
            if board[r] == c:
                fill_color = "#2ecc71" if status == "place" and r == active_r and c == active_c else "#1a1a2e"
                canvas.create_text(
                    x0 + w / 2, y0 + w / 2,
                    text="♕",
                    font=("Arial", font_size, "bold"),
                    fill=fill_color
                )

def update_stats_label(r=-1, c=-1, status=""):
    """Cập nhật nhãn trạng thái và bộ đếm"""
    if status == "try":
        msg = f"Đang thử đặt Hậu tại hàng {r+1}, cột {c+1}..."
    elif status == "place":
        msg = f"Đặt thành công Hậu tại hàng {r+1}, cột {c+1}."
    elif status == "backtrack":
        msg = f"Xung đột! Đang quay lui khỏi hàng {r+1}, cột {c+1}..."
    elif status == "done":
        msg = "Đã tìm thấy lời giải thành công!"
    else:
        msg = "Nhấn Start để bắt đầu."

    lbl_status.config(text=msg)
    lbl_steps.config(text=f"Số bước: {step_count}   |   Quay lui: {backtrack_count}")

def step():
    global running, step_count, backtrack_count
    if not running or paused:
        return
    try:
        state = next(generator)
        step_count += 1
        if state["status"] == "backtrack":
            backtrack_count += 1
        draw_board(state["r"], state["c"], state["status"])
        update_stats_label(state["r"], state["c"], state["status"])
        delay = speed_var.get()
        root.after(delay, step)
    except StopIteration:
        running = False
        draw_board(-1, -1, "done")
        update_stats_label(status="done")
        btn_start.config(state=tk.NORMAL)
        btn_pause.config(state=tk.DISABLED, text="Pause")
        combo_n.config(state="readonly")

def start():
    global running, generator, board, step_count, backtrack_count, paused
    if running:
        return
    N_val = int(n_var.get())
    global N
    N = N_val
    board = [-1] * N
    step_count = 0
    backtrack_count = 0
    paused = False
    running = True
    btn_start.config(state=tk.DISABLED)
    btn_pause.config(state=tk.NORMAL, text="Pause")
    combo_n.config(state="disabled")
    lbl_title.config(text=f"{N}-Queens Problem (Backtracking)")
    generator = solve_n_queens(0)
    update_stats_label()
    step()

def reset():
    global running, board, step_count, backtrack_count, paused, N
    running = False
    paused = False
    N = int(n_var.get())
    board = [-1] * N
    step_count = 0
    backtrack_count = 0
    btn_start.config(state=tk.NORMAL)
    btn_pause.config(state=tk.DISABLED, text="Pause")
    combo_n.config(state="readonly")
    lbl_title.config(text=f"{N}-Queens Problem (Backtracking)")
    draw_board()
    update_stats_label()

def toggle_pause():
    global paused
    if not running:
        return
    paused = not paused
    if paused:
        btn_pause.config(text="Resume")
    else:
        btn_pause.config(text="Pause")
        step()  # Tiếp tục chạy

# --- KHỞI TẠO CỬA SỔ ---
root = tk.Tk()
root.title("N-Queens Visualizer")
root.configure(bg="#1a1a2e")
root.geometry("480x640")
root.resizable(False, False)

# --- TIÊU ĐỀ ---
f_title = tk.Frame(root, bg="#1a1a2e")
f_title.pack(pady=(14, 4))
lbl_title = tk.Label(
    f_title, text="8-Queens Problem (Backtracking)",
    fg="#e0e0e0", bg="#1a1a2e", font=("Consolas", 13, "bold")
)
lbl_title.pack()

# --- THÔNG TIN TRẠNG THÁI ---
f_info = tk.Frame(root, bg="#1a1a2e")
f_info.pack(pady=(0, 4))

lbl_steps = tk.Label(
    f_info, text="Số bước: 0   |   Quay lui: 0",
    fg="#a0c4ff", bg="#1a1a2e", font=("Consolas", 10)
)
lbl_steps.pack()

lbl_status = tk.Label(
    f_info, text="Nhấn Start để bắt đầu.",
    fg="#ffd166", bg="#1a1a2e", font=("Consolas", 10, "italic"),
    wraplength=440, justify="center"
)
lbl_status.pack()

# --- BÀN CỜ ---
canvas = tk.Canvas(root, width=400, height=400, bg="white", highlightthickness=0)
canvas.pack(pady=8)

# --- VÙNG ĐIỀU KHIỂN ---
f_ctrl = tk.Frame(root, bg="#1a1a2e")
f_ctrl.pack(pady=6)

btn_start = tk.Button(
    f_ctrl, text="▶ Start", command=start,
    width=9, font=("Consolas", 10, "bold"),
    bg="#2ecc71", fg="white", activebackground="#27ae60",
    relief="flat", cursor="hand2"
)
btn_start.grid(row=0, column=0, padx=6)

btn_pause = tk.Button(
    f_ctrl, text="Pause", command=toggle_pause,
    width=9, font=("Consolas", 10, "bold"),
    bg="#f39c12", fg="white", activebackground="#d68910",
    relief="flat", cursor="hand2", state=tk.DISABLED
)
btn_pause.grid(row=0, column=1, padx=6)

btn_reset = tk.Button(
    f_ctrl, text="↺ Reset", command=reset,
    width=9, font=("Consolas", 10),
    bg="#e74c3c", fg="white", activebackground="#c0392b",
    relief="flat", cursor="hand2"
)
btn_reset.grid(row=0, column=2, padx=6)

# --- CHỌN KÍCH THƯỚC N ---
f_options = tk.Frame(root, bg="#1a1a2e")
f_options.pack(pady=4)

tk.Label(
    f_options, text="Kích thước bàn cờ (N):",
    fg="#e0e0e0", bg="#1a1a2e", font=("Consolas", 10)
).grid(row=0, column=0, padx=(0, 8), sticky="w")

n_var = tk.StringVar(value="8")
combo_n = ttk.Combobox(
    f_options, textvariable=n_var,
    values=[str(i) for i in range(4, 11)],
    state="readonly", width=5, font=("Consolas", 10)
)
combo_n.grid(row=0, column=1, sticky="w")

# --- THANH TRƯỢT TỐC ĐỘ ---
f_speed = tk.Frame(root, bg="#1a1a2e")
f_speed.pack(pady=(4, 12))

tk.Label(
    f_speed, text="Tốc độ (ms/bước):",
    fg="#e0e0e0", bg="#1a1a2e", font=("Consolas", 10)
).grid(row=0, column=0, padx=(0, 8))

speed_var = tk.IntVar(value=120)
tk.Scale(
    f_speed, variable=speed_var,
    from_=20, to=1000,
    orient=tk.HORIZONTAL, length=220,
    bg="#1a1a2e", fg="#e0e0e0", troughcolor="#3a3a5c",
    highlightthickness=0, font=("Consolas", 8),
    resolution=10
).grid(row=0, column=1)

lbl_speed_val = tk.Label(
    f_speed, textvariable=speed_var,
    fg="#a0c4ff", bg="#1a1a2e", font=("Consolas", 10), width=5
)
lbl_speed_val.grid(row=0, column=2, padx=(4, 0))

reset()
root.mainloop()
