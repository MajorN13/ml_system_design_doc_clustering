"""Дерево причин рисков: ровная сетка, ортогональные связи, группы причин в контейнерах.

Запуск: python risk_tree.py <папка для png> [папка со шрифтами CMU Sans Serif]
"""
import sys, dataclasses
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
FONT_DIR = sys.argv[2] if len(sys.argv) > 2 else "fonts"
for f in ["cmu-sans-serif-500-roman.ttf", "cmu-sans-serif-700-roman.ttf"]:
    font_manager.fontManager.addfont(f"{FONT_DIR}/{f}")
font_manager.fontManager.ttflist = [dataclasses.replace(e, stretch="normal") if e.name == "CMU Sans Serif" else e
                                    for e in font_manager.fontManager.ttflist]
plt.rcParams["font.family"] = "CMU Sans Serif"

BLUE, GRAY, RED, AMBER = "#003366", "#555555", "#B00000", "#AA6400"
LINE = "#4A4A4A"

R = {  # id: (подпись, P, I)
    "R1": ("Витрина не обновилась", 3, 3), "R2": ("Нет файла от бизнеса", 4, 3),
    "R3": ("Ошибки в данных", 3, 4), "R4": ("Кластеры «прыгают»", 4, 4),
    "R5": ("Мало ТК", 4, 3), "R6": ("Недоверие пользователей", 3, 5),
    "R7": ("Не интерпретируемы", 3, 4), "R8": ("Эффект ниже затрат", 3, 3),
    "R9": ("Утечка данных", 2, 5), "R10": ("Не держим SLA", 2, 2),
    "R11": ("Уход сотрудника", 2, 3), "R12": ("Расширение скоупа", 3, 3),
    "R13": ("Изменилась схема", 3, 3), "R14": ("Задержка доступов, ИБ", 4, 3),
    "R15": ("Смена или уход ЛПР", 2, 4), "R16": ("Неверная гипотеза", 2, 5),
}


def fill(s):
    if s >= 15: return "#F2A0A0", "#960000"
    if s >= 10: return "#FFC98F", "#A04A00"
    if s >= 5: return "#FFE9A6", "#7A5A00"
    return "#CFE8C4", "#006400"


W, H = 8.4, 3.85
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
BW, BH = 1.15, 0.40
C = [0.7, 2.15, 3.6, 5.05, 6.45]   # центры колонок


def box(x, y, w, h):
    return dict(l=x - w / 2, r=x + w / 2, t=y + h / 2, b=y - h / 2, x=x, y=y)


def risk(rid, x, y, w=BW, h=BH):
    lab, p, i = R[rid]
    fc, tc = fill(p * i)
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec="none"))
    ax.text(x - w / 2 + 0.06, y + 0.085, rid, fontsize=7.6, fontweight="bold", va="center")
    ax.text(x + w / 2 - 0.06, y + 0.085, str(p * i), fontsize=7.6, fontweight="bold", va="center", ha="right",
            color=tc)
    ax.text(x - w / 2 + 0.06, y - 0.09, lab, fontsize=6.6, va="center")
    return box(x, y, w, h)


def event(text, x, y, w=1.2, h=0.5):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#E3EAF2", ec=BLUE, lw=0.9))
    ax.text(x, y, text, fontsize=7.2, fontweight="bold", ha="center", va="center", color=BLUE, linespacing=1.1)
    return box(x, y, w, h)


def group(title, x, y, w, h):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                fc="#F7F7F7", ec="#8A9BB0", lw=0.7, ls=(0, (3, 2))))
    ax.text(x - w / 2 + 0.06, y + h / 2 - 0.05, title, fontsize=6.4, fontweight="bold", color=BLUE, va="top")
    return box(x, y, w, h)


def path(pts, color=LINE, lw=0.8, head=True):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", solid_joinstyle="miter")
    if head:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        dx, dy = x1 - x0, y1 - y0
        n = (dx ** 2 + dy ** 2) ** 0.5
        ux, uy = dx / n, dy / n
        s = 0.075
        ax.add_patch(Polygon([(x1, y1), (x1 - ux * s - uy * s * 0.5, y1 - uy * s + ux * s * 0.5),
                              (x1 - ux * s + uy * s * 0.5, y1 - uy * s - ux * s * 0.5)], fc=color, ec=color))


# ---------------- верхний ряд: организационные причины -> E1
ax.text(0.13, 3.77, "Организация и ИБ", fontsize=6.6, fontweight="bold", color=BLUE, va="center")
top_ids = ["R14", "R15", "R12", "R11", "R9"]
chips_x = [0.7, 1.95, 3.2, 4.45, 5.7]
yc, ybus = 3.45, 2.98
for rid, x in zip(top_ids, chips_x):
    b = risk(rid, x, yc, w=1.12)
    ax.plot([x, x], [b["b"], ybus], color=LINE, lw=0.8)
E1 = event("Запуск сорван или\nсервис остановлен", C[4], ybus, h=0.42)
path([(chips_x[0], ybus), (E1["l"], ybus)])

# разделитель
ax.plot([0.12, 5.6], [2.8, 2.8], color="#D5DCE4", lw=0.6)
ax.text(0.13, 2.7, "Данные, модель и пользователи", fontsize=6.6, fontweight="bold", color=BLUE, va="center")

# ---------------- данные и модель
gS = group("Источники данных", C[0], 2.06, 1.3, 1.14)
risk("R2", C[0], 2.2, w=1.15)
risk("R13", C[0], 1.74, w=1.15)
r3 = risk("R3", C[1], 2.2)
r5 = risk("R5", C[1], 1.74)
r1 = risk("R1", C[1], 1.08)
gM = group("Модель", C[2], 2.06, 1.3, 1.14)
risk("R4", C[2], 2.2)
risk("R7", C[2], 1.74)
r16 = risk("R16", C[3], 2.0)
r6 = risk("R6", C[3], 1.08)
E2 = event("Разбиение\nнепригодно для CVP", C[4], 2.36)
E3 = event("Сервисом\nне пользуются", C[4], 1.08)
r8 = risk("R8", C[4], 0.42, w=1.2)
r10 = risk("R10", C[0], 0.42)

xe = (r6["r"] + E2["l"]) / 2   # колонка изломов между R6/R16 и событиями
path([(gS["r"], 2.2), (r3["l"], 2.2)])                                   # источники -> R3
path([(gS["r"], 1.74), (1.46, 1.74), (1.46, 1.08), (r1["l"], 1.08)])         # источники -> R1
path([(r3["r"], 2.2), (gM["l"], 2.2)], color=RED, lw=1.3)                # R3 -> модель
path([(r5["r"], 1.74), (gM["l"], 1.74)], color=RED, lw=1.3)                # R5 -> модель
path([(gM["r"], 2.45), (E2["l"], 2.45)])                                   # модель -> E2
path([(r16["r"], 2.0), (xe, 2.0), (xe, 2.25), (E2["l"], 2.25)])            # R16 -> E2
path([(gM["x"], gM["b"]), (gM["x"], 1.17), (r6["l"], 1.17)], color=RED, lw=1.3)   # модель -> R6
path([(r1["r"], 0.98), (r6["l"], 0.98)])                                   # R1 -> R6
path([(r10["r"], 0.42), (C[3], 0.42), (C[3], r6["b"])])                    # R10 -> R6
path([(r6["r"], 1.08), (E3["l"], 1.08)], color=RED, lw=1.3)                # R6 -> E3
path([(r6["r"], 0.98), (xe, 0.98), (xe, 0.42), (r8["l"], 0.42)])           # R6 -> R8

# ---------------- шина ИЛИ и вершина
xb = 7.2
TY = 1.75
for e in [E1, E2, r8]:
    ax.plot([e["r"], xb], [e["y"], e["y"]], color=LINE, lw=0.8)
ax.plot([E3["r"], xb], [E3["y"], E3["y"]], color=RED, lw=1.3)
ax.plot([xb, xb], [r8["y"], E1["y"]], color=LINE, lw=0.8)
ax.plot([xb, xb], [E3["y"], TY], color=RED, lw=1.3)
ax.add_patch(FancyBboxPatch((xb + 0.06, TY - 0.13), 0.3, 0.26, boxstyle="round,pad=0,rounding_size=0.12",
                            fc="white", ec=AMBER, lw=1.0))
ax.plot([xb, xb + 0.06], [TY, TY], color=RED, lw=1.3)
ax.text(xb + 0.21, TY, "ИЛИ", fontsize=5.6, fontweight="bold", color=AMBER, ha="center", va="center")
path([(xb + 0.36, TY), (7.62, TY)], color=RED, lw=1.3)
ax.add_patch(Rectangle((7.62, TY - 0.5), 0.76, 1.0, fc=BLUE, ec=BLUE))
ax.text(8.0, TY, "Сервис\nне дал\nбизнес-\nэффекта", fontsize=7.3, fontweight="bold", color="white",
        ha="center", va="center", linespacing=1.05)

# легенда
ax.text(0.13, 0.06, "A → B: A повышает вероятность B.  Число — P × I до мер.", fontsize=5.8, color=GRAY,
        va="center")
ax.plot([3.0, 3.3], [0.06, 0.06], color=RED, lw=1.3)
ax.text(3.36, 0.06, "критическая цепочка", fontsize=5.8, color=RED, va="center")

fig.savefig(f"{OUT}/risk_tree.png", dpi=300, facecolor="white")
print("ok")
