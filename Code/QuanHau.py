import tkinter as tk

N = 8
DELAY_MS = 120
board = [-1] * N  # board[i] = j nghĩa là hàng i, quân hậu đặt ở cột j
generator = None
running = False

def is_safe(r, c):
    """Kiểm tra xem đặt Hậu ở hàng r, cột c có bị ăn không"""
    for i in range(r):
        # Cùng cột hoặc cùng đường chéo
        if board[i] == c or abs(board[i] - c) == abs(i - r):
            return False
    return True

def solve_n_queens(row):
    if row == N:
        return True # Xếp xong 8 quân
        
    for col in range(N):
        # Thử vị trí
        yield {"r": row, "c": col, "status": "try"} 
        if is_safe(row, col):
            # Đặt quân hậu
            board[row] = col
            yield {"r": row, "c": col, "status": "place"}
            # Đệ quy đi tiếp hàng dưới
            if (yield from solve_n_queens(row + 1)):
                return True   
            # Quay lui nếu đường đi dưới bị chặn
            board[row] = -1
            yield {"r": row, "c": col, "status": "backtrack"}

# --- XỬ LÝ GIAO DIỆN & LOGIC ---
def draw_board(active_r=-1, active_c=-1, status=""):
    canvas.delete("all")
    w = 400 / N
    for r in range(N):
        for c in range(N):
            # Vẽ nền bàn cờ caro
            color = "white" if (r + c) % 2 == 0 else "lightgray"
            # Đổi màu nền nếu đang thử nghiệm hoặc quay lui
            if r == active_r and c == active_c:
                if status == "try": color = "yellow"
                elif status == "backtrack": color = "red"
            x0, y0 = c * w, r * w
            canvas.create_rectangle(x0, y0, x0 + w, y0 + w, fill=color, outline="black")
            # Vẽ quân hậu nếu trên bảng ghi nhận
            if board[r] == c:
                canvas.create_text(x0 + w/2, y0 + w/2, text="♕", font=("Arial", 24, "bold"), fill="black")

def step():
    global running
    if not running: return
    try:
        state = next(generator)
        draw_board(state["r"], state["c"], state["status"])
        root.after(DELAY_MS, step)
    except StopIteration:
        running = False
        draw_board(-1, -1, "done") # Trả về bàn cờ tĩnh khi xong
        btn_start.config(state=tk.NORMAL)

def start():
    global running, generator, board
    if running: return
    running = True
    board = [-1] * N
    btn_start.config(state=tk.DISABLED)
    generator = solve_n_queens(0)
    step()

def reset():
    global running, board
    running = False
    board = [-1] * N
    btn_start.config(state=tk.NORMAL)
    draw_board()

# --- KHỞI TẠO CỬA SỔ TKINTER ---
root = tk.Tk()
root.title("N-Queens Visualizer")
root.configure(bg="#2b2b2b")
root.geometry("450x550")

# Vùng thống kê / Tiêu đề
f_stats = tk.Frame(root, bg="#2b2b2b")
f_stats.pack(pady=10)
tk.Label(f_stats, text="8-Queens Problem (Backtracking)", fg="white", bg="#2b2b2b", font=("Consolas", 14, "bold")).pack()

# Vùng vẽ bàn cờ
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack(pady=10)

# Vùng điều khiển
f_ctrl = tk.Frame(root, bg="#2b2b2b")
f_ctrl.pack(pady=10)
btn_start = tk.Button(f_ctrl, text="Start", command=start, width=10, font=("Consolas", 10, "bold"))
btn_start.pack(side=tk.LEFT, padx=10)
tk.Button(f_ctrl, text="Reset", command=reset, width=10, font=("Consolas", 10)).pack(side=tk.LEFT, padx=10)

reset()
root.mainloop()