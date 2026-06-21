import tkinter as tk
import random

ARRAY_SIZE = 30
DELAY_MS = 10

arr = []
generator = None
running = False
persistent_green = set()
comparisons = 0
accesses = 0

def bubble_sort():
    global comparisons, accesses
    n = len(arr)
    for i in range(n-1):
        for j in range(n-1-i):
            comparisons += 1; accesses += 2
            yield {"red": [], "green": [j, j+1]}
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                accesses += 2
                yield {"red": [j, j+1], "green": []}

def partition(low, high):
    global comparisons, accesses
    pivot = arr[high]; accesses += 1
    i = low - 1
    for j in range(low, high):
        comparisons += 1; accesses += 1
        yield {"red": [j], "green": [high, max(low, i+1)]}
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]; accesses += 2
            yield {"red": [i, j], "green": [high]}
    arr[i+1], arr[high] = arr[high], arr[i+1]; accesses += 2
    yield {"red": [i+1], "green": [i+1]}
    return i+1

def quick_sort(low, high):
    if low < high:
        pi = yield from partition(low, high)
        yield from quick_sort(low, pi-1)
        yield from quick_sort(pi+1, high)

def merge(left, mid, right):
    global comparisons, accesses
    L, R = arr[left:mid+1], arr[mid+1:right+1]
    i = j = 0; k = left
    while i < len(L) and j < len(R):
        comparisons += 1; accesses += 2
        if L[i] <= R[j]:
            arr[k] = L[i]; i += 1
        else:
            arr[k] = R[j]; j += 1
        accesses += 1
        yield {"red": [k], "green": [left, mid, right]}
        k += 1
    for val in L[i:]:
        arr[k] = val; accesses += 1; k += 1
        yield {"red": [k-1], "green": [left, mid, right]}
    for val in R[j:]:
        arr[k] = val; accesses += 1; k += 1
        yield {"red": [k-1], "green": [left, mid, right]}

def merge_sort(left, right):
    if left >= right: return
    mid = (left + right) // 2
    yield from merge_sort(left, mid)
    yield from merge_sort(mid+1, right)
    yield from merge(left, mid, right)

def draw(red_set=None, green_set=None):
    canvas.delete("all")
    red_set = red_set or set()
    green_set = green_set or set()
    c_width, c_height = 800, 400
    w = c_width / ARRAY_SIZE
    for i, val in enumerate(arr):
        h = (val / 100) * c_height
        color = "white"
        if i in red_set: color = "red"
        elif i in green_set: color = "green"
        canvas.create_rectangle(i*w, c_height-h, (i+1)*w, c_height, fill=color, outline="black")
    lbl_comp.config(text=f"Comparisons: {comparisons}")
    lbl_acc.config(text=f"Accesses: {accesses}")

def step():
    global running, persistent_green
    if not running: return
    try:
        state = next(generator)
        if state["green"]: persistent_green = set(state["green"])
        draw(set(state["red"]), persistent_green - set(state["red"]))
        root.after(DELAY_MS, step)
    except StopIteration:
        running = False
        persistent_green.clear()
        draw()
        btn_start.config(state=tk.NORMAL)

def start():
    global running, generator, persistent_green, comparisons, accesses
    if running: return
    running = True
    persistent_green.clear()
    comparisons = accesses = 0
    btn_start.config(state=tk.DISABLED)
    lbl_algo.config(text=f"Algorithm: {algo_var.get()}")
    if algo_var.get() == "Bubble Sort": generator = bubble_sort()
    elif algo_var.get() == "Quick Sort": generator = quick_sort(0, ARRAY_SIZE-1)
    else: generator = merge_sort(0, ARRAY_SIZE-1)
    step()

def reset():
    global arr, running, persistent_green, comparisons, accesses
    running = False
    persistent_green.clear()
    comparisons = accesses = 0
    arr = [random.randint(5, 100) for _ in range(ARRAY_SIZE)]
    btn_start.config(state=tk.NORMAL)
    draw()

root = tk.Tk()
root.title("Sorting Visualizer")
root.configure(bg="#2b2b2b")
f_stats = tk.Frame(root, bg="#2b2b2b")
f_stats.pack(pady=10)
lbl_algo = tk.Label(f_stats, text="Algorithm: Bubble Sort", fg="white", bg="#2b2b2b", font=("Consolas", 12))
lbl_algo.pack(side=tk.LEFT, padx=20)
lbl_comp = tk.Label(f_stats, text="Comparisons: 0", fg="white", bg="#2b2b2b", font=("Consolas", 12))
lbl_comp.pack(side=tk.LEFT, padx=20)
lbl_acc = tk.Label(f_stats, text="Accesses: 0", fg="white", bg="#2b2b2b", font=("Consolas", 12))
lbl_acc.pack(side=tk.LEFT, padx=20)
canvas = tk.Canvas(root, width=800, height=400, bg="black")
canvas.pack(padx=20)
f_ctrl = tk.Frame(root, bg="#2b2b2b")
f_ctrl.pack(pady=15)
algo_var = tk.StringVar(value="Bubble Sort")
tk.OptionMenu(f_ctrl, algo_var, "Bubble Sort", "Quick Sort", "Merge Sort").pack(side=tk.LEFT, padx=10)
btn_start = tk.Button(f_ctrl, text="Start", command=start, width=10, font=("Consolas", 10, "bold"))
btn_start.pack(side=tk.LEFT, padx=10)
tk.Button(f_ctrl, text="Reset", command=reset, width=10, font=("Consolas", 10)).pack(side=tk.LEFT, padx=10)
reset()
root.mainloop()