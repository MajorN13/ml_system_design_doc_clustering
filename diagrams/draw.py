"""Диаграммы для ML System Design Doc: этапы, план-график, матрица и дерево рисков."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

for f in ["cmu-sans-serif-500-roman.ttf", "cmu-sans-serif-700-roman.ttf", "cmu-sans-serif-500-italic.ttf"]:
    font_manager.fontManager.addfont(f"fonts/{f}")
import dataclasses
font_manager.fontManager.ttflist = [dataclasses.replace(_e, stretch="normal") if _e.name == "CMU Sans Serif" else _e
                                    for _e in font_manager.fontManager.ttflist]
plt.rcParams["font.family"] = ["CMU Sans Serif", "DejaVu Sans"]  # DejaVu — запасной для символов, которых нет в CMU (стрелки)

BLUE = "#003366"
LIGHT = "#F0F0F0"
GREEN = "#006400"
AMBER = "#AA6400"
RED = "#960000"
GRAY = "#555555"
DPI = 300

# ---------------------------------------------------------------- этапы
ROW1 = [
    ("0", "Требования и\nкритерии успеха", "PO · DS · MLE", "нед. 1–2", "пользователи, ЛПР,\nпороги пилота"),
    ("1", "Доступы, EDA,\nкачество данных", "DS · DE", "нед. 2–4", "отчёт EDA,\nDQ-правила"),
    ("2", "ETL и витрина\nпризнаков v0", "DE · MLE", "нед. 3–5", "DAG Airflow,\nвитрина в DVC"),
    ("3", "Бейзлайн:\nправила бизнеса", "DS", "нед. 4–5", "rule-based\nразбиение"),
    ("4", "MVP: PCA + Ward,\nвыбор k", "DS", "нед. 5–7", "модуль\nкластеризации"),
    ("5", "Офлайн-оценка\nпротив бейзлайна", "DS", "нед. 7–8", "отчёт\nо качестве"),
    ("G1", "Gate 1", "PO + DS lead", "нед. 8", ""),
]
ROW2 = [
    ("6", "Excel-отчёт и\nпрофили кластеров", "DS · PO", "нед. 8–9", "шаблон\nотчёта"),
    ("7", "API-сервис\n(FastAPI)", "MLE", "нед. 8–10", "докер-образ\nAPI"),
    ("8", "UI Streamlit,\nSSO, логирование", "MLE", "нед. 9–11", "сервис\nв dev"),
    ("9", "Тесты в dev:\nфункц. и нагрузка", "MLE", "нед. 11–12", "протокол\nтестов"),
    ("10", "Пилот: офлайн,\nэксперты, процесс", "PO · бизнес · DS", "нед. 12–16", "протокол\nпилота"),
    ("G2", "Gate 2", "решение ЛПР", "нед. 16", ""),
    ("11", "Прод, мониторинг,\nпередача в поддержку", "MLE · DevOps", "нед. 17–18", "сервис\nв prod"),
]

BW, BH, GAP = 0.98, 1.22, 0.22   # ширина/высота блока, промежуток (дюймы)


def draw_box(ax, x, y, item, highlight=False):
    num, title, roles, weeks, out = item
    head = GREEN if highlight else BLUE
    ax.add_patch(Rectangle((x, y), BW, BH, fc=LIGHT, ec=head, lw=0.8))
    ax.add_patch(Rectangle((x, y + BH - 0.2), BW, 0.2, fc=head, ec=head, lw=0.8))
    ax.text(x + 0.06, y + BH - 0.1, f"Этап {num}", color="white", fontsize=6.3, fontweight="bold", va="center")
    ax.text(x + BW - 0.06, y + BH - 0.1, weeks, color="white", fontsize=5.2, va="center", ha="right")
    ax.text(x + BW / 2, y + BH - 0.42, title, fontsize=6.1, fontweight="bold", ha="center", va="center",
            color="black", linespacing=1.1)
    ax.text(x + BW / 2, y + BH - 0.70, roles, fontsize=5.4, ha="center", va="center", color=head, fontweight="bold")
    ax.plot([x + 0.08, x + BW - 0.08], [y + 0.40, y + 0.40], color="#BBBBBB", lw=0.4)
    ax.text(x + BW / 2, y + 0.20, out, fontsize=5.2, ha="center", va="center", color=GRAY, linespacing=1.05,
            style="italic")


def draw_gate(ax, cx, cy, item):
    num, title, who, weeks, _ = item
    r = 0.42
    ax.add_patch(Polygon([(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)], closed=True,
                         fc="#FFF4E0", ec=AMBER, lw=0.9))
    ax.text(cx, cy + 0.08, title, fontsize=6.3, fontweight="bold", ha="center", va="center", color=AMBER)
    ax.text(cx, cy - 0.10, who, fontsize=4.8, ha="center", va="center", color="black")
    ax.text(cx, cy - r - 0.08, weeks, fontsize=5, ha="center", va="top", color=GRAY)


def arrow(ax, p1, p2, color="black", style="-|>", lw=0.7, ls="-", conn="arc3"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=6, color=color, lw=lw, ls=ls,
                                 connectionstyle=conn, shrinkA=0, shrinkB=0))


def draw_row(ax, items, x0, y0):
    """Рисует ряд, возвращает координаты центров/краёв элементов."""
    pos = []
    x = x0
    for it in items:
        if it[0].startswith("G"):
            cx = x + 0.45
            draw_gate(ax, cx, y0 + BH / 2, it)
            pos.append((x, x + 0.9, "gate", cx))
            x += 0.9 + GAP
        else:
            draw_box(ax, x, y0, it, highlight=(it[0] == "10"))
            pos.append((x, x + BW, "box", x + BW / 2))
            x += BW + GAP
    for a, b in zip(pos, pos[1:]):
        arrow(ax, (a[1] + 0.01, y0 + BH / 2), (b[0] - 0.01, y0 + BH / 2))
    return pos


def row_width(items):
    return sum((0.9 if i[0].startswith("G") else BW) for i in items) + GAP * (len(items) - 1)


def stages_row(items, fname, loop, below=0.45):
    W = row_width(items) + 0.2
    H = BH + 0.3 + below
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    y0 = below
    pos = draw_row(ax, items, 0.1, y0)
    loop(ax, pos, y0)
    fig.savefig(f"{OUT}/{fname}", dpi=DPI, facecolor="white")
    plt.close(fig)


def loop1(ax, pos, y0):
    g = pos[6]; m = pos[4]
    # нет -> к этапу 4
    arrow(ax, (g[3], y0 + BH / 2 - 0.42), (g[3], y0 - 0.25), color=RED, style="-")
    arrow(ax, (g[3], y0 - 0.25), (m[3], y0 - 0.25), color=RED, style="-")
    arrow(ax, (m[3], y0 - 0.25), (m[3], y0), color=RED)
    ax.text((g[3] + m[3]) / 2, y0 - 0.21, "нет: доработка модели, до 2 итераций", color=RED, fontsize=5.4,
            ha="center", va="bottom")
    ax.text(g[3] + 0.36, y0 + BH / 2 + 0.06, "да", color=GREEN, fontsize=5.6, fontweight="bold", va="bottom",
            ha="left")
    ax.text(0.1, y0 + BH + 0.18, "Подготовка и моделирование", fontsize=7.5, fontweight="bold", color=BLUE)


# Маршруты доработки на Gate 2 (README, §3.2): (индекс этапа в ROW2 или None — к этапу 4 в первом ряду, подпись)
REWORK = [
    (2, "Q3, Q4 (время цикла, использование) → этап 8: UI, отчёт, обучение"),
    (1, "p95, доля ошибок → этапы 7–9: производительность API, нагрузочные тесты"),
    (None, "ML-метрики, Q1, Q2 (качество, интерпретируемость) → этап 4: модель"),
]


def loop2(ax, pos, y0, title="Сервис, пилот и запуск   (Этап 12, документация и Issues, идёт сквозным потоком)"):
    g = pos[5]
    ax.text(g[3] + 0.47, y0 + BH / 2 + 0.06, "go", color=GREEN, fontsize=5.6, fontweight="bold", va="bottom")
    step = 0.15
    lanes = [y0 - 0.14 - step * i for i in range(len(REWORK))]
    ax.plot([g[3], g[3]], [y0 + BH / 2 - 0.42, lanes[-1]], color=RED, lw=0.7)
    for (idx, label), yl in zip(REWORK, lanes):
        if idx is None:
            xt = pos[0][0] + 0.02
            arrow(ax, (g[3], yl), (xt, yl), color=RED)
            ax.text(xt + 0.04, yl + 0.025, label, color=RED, fontsize=5.2, ha="left", va="bottom")
        else:
            xt = pos[idx][3]
            ax.plot([g[3], xt], [yl, yl], color=RED, lw=0.7)
            arrow(ax, (xt, yl), (xt, y0), color=RED)
            ax.text(xt + 0.05, yl + 0.025, label, color=RED, fontsize=5.2, ha="left", va="bottom")
    ax.text(g[3] + 0.06, y0 - 0.06, "доработка: +3 нед., не больше 1 раза", color=RED, fontsize=5.2,
            fontweight="bold", ha="left", va="top")
    ax.text(g[3] + 0.06, lanes[-1] + 0.03, "no-go → план Б: витрина +\nправила + отчёт без ML", color=RED,
            fontsize=5.2, fontweight="bold", ha="left", va="bottom", linespacing=1.1)
    ax.text(0.1, y0 + BH + 0.18, title, fontsize=7.5, fontweight="bold", color=BLUE)


stages_row(ROW1, "stages_row1.png", loop1)
stages_row(ROW2, "stages_row2.png", loop2, below=0.62)

# Полная схема для README: два ряда друг под другом
W = max(row_width(ROW1), row_width(ROW2)) + 0.2
H = 2 * (BH + 0.75) + 0.6
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
yA = H - BH - 0.35
pA = draw_row(ax, ROW1, 0.1, yA)
loop1(ax, pA, yA)
yB = 1.0
pB = draw_row(ax, ROW2, 0.1, yB)
loop2(ax, pB, yB, title="Сервис, пилот и запуск")
# переход G1 -> этап 6
g = pA[6]
ax.plot([g[1] - 0.45 + 0.42, W - 0.05], [yA + BH / 2] * 2, color=GREEN, lw=0.7)
yc = yB + BH + 0.42
ax.plot([W - 0.05, W - 0.05], [yA + BH / 2, yc], color=GREEN, lw=0.7)
ax.plot([W - 0.05, 0.03], [yc, yc], color=GREEN, lw=0.7)
ax.plot([0.03, 0.03], [yc, yB + BH / 2], color=GREEN, lw=0.7)
arrow(ax, (0.03, yB + BH / 2), (0.1, yB + BH / 2), color=GREEN)
ax.add_patch(Rectangle((0.1, 0.12), W - 0.3, 0.2, fc="#E3EAF2", ec=BLUE, lw=0.6))
ax.text(W / 2, 0.22, "Этап 12. Документация (алгоритм, API, эксплуатация), Issues с «белыми пятнами» — сквозной, DS · MLE",
        fontsize=6, ha="center", va="center", color=BLUE, fontweight="bold")
fig.savefig(f"{OUT}/scheme.png", dpi=DPI, facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------- план-график
TASKS = [
    ("0 Требования и критерии", 1, 2, "prep"), ("1 Доступы, EDA, DQ", 2, 4, "prep"),
    ("2 ETL и витрина v0", 3, 5, "prep"), ("3 Бейзлайн", 4, 5, "model"),
    ("4 MVP-модель", 5, 7, "model"), ("5 Офлайн-оценка", 7, 8, "model"),
    ("6 Отчёт и профили", 8, 9, "svc"), ("7 API-сервис", 8, 10, "svc"),
    ("8 UI, SSO, логи", 9, 11, "svc"), ("9 Тесты в dev", 11, 12, "svc"),
    ("10 Пилот", 12, 16, "pilot"), ("11 Прод и мониторинг", 17, 18, "prod"),
    ("Запас: доработка, сдвиги", 19, 21, "buf"),
    ("12 Документация", 1, 18, "doc"),
]
COL = {"prep": "#7A93AC", "model": BLUE, "svc": "#3C6E9F", "pilot": GREEN, "prod": "#5A5A5A", "doc": "#B8C7D6",
       "buf": "#F3D9D9"}
NAMES = {"prep": "подготовка", "model": "моделирование", "svc": "сервис", "pilot": "пилот", "prod": "прод",
         "doc": "документация", "buf": "запас"}
# Неделя 1 — 16.11.2026; новогодняя пауза до 10.01.2027 в счёт недель не идёт (README, §2.2)
import datetime as _dt
NWEEKS, PAUSE_AFTER, PAUSE_W = 21, 7, 0.75


def wx(w):  # координата недели с учётом паузы
    return w + (PAUSE_W if w > PAUSE_AFTER else 0)


def wstart(w):
    d = _dt.date(2026, 11, 16) + _dt.timedelta(weeks=w - 1)
    return d + _dt.timedelta(weeks=1) if w > PAUSE_AFTER else d  # пауза — одна календарная неделя (04.01–10.01)


fig, ax = plt.subplots(figsize=(6.4, 3.05))
for i, (name, a, b, k) in enumerate(TASKS):
    y = len(TASKS) - 1 - i
    if k == "buf":
        ax.barh(y, wx(b) - wx(a) + 1, left=wx(a) - 0.5, height=0.62, color=COL[k], edgecolor=RED, lw=0.5,
                hatch="////")
    else:
        ax.barh(y, wx(b) - wx(a) + 1, left=wx(a) - 0.5, height=0.62, color=COL[k], edgecolor="none")
# пауза
p0, p1 = wx(PAUSE_AFTER) + 0.5, wx(PAUSE_AFTER + 1) - 0.5
ax.axvspan(p0, p1, color="white", zorder=3)
ax.axvspan(p0, p1, fc="none", ec="#999999", hatch="....", lw=0, zorder=3)
ax.text((p0 + p1) / 2, len(TASKS) / 2 - 0.5, "праздники,\nпауза до\n11.01.2027", rotation=90, fontsize=4.6,
        color=GRAY, ha="center", va="center", zorder=4,
        bbox=dict(fc="white", ec="none", pad=0.8))
for w, lab, col in [(8, "Gate 1 · 15.01", AMBER), (16, "Gate 2 · 12.03", AMBER), (21, "срок · 16.04", RED)]:
    ax.axvline(wx(w) + 0.5, color=col, lw=0.8, ls="--")
    ax.text(wx(w) + 0.5 + (0.12 if w < 21 else -0.12), len(TASKS) - 0.35, lab, color=col, fontsize=5.6,
            ha="left" if w < 21 else "right", va="bottom", fontweight="bold")
ax.set_yticks(range(len(TASKS)))
ax.set_yticklabels([t[0] for t in TASKS][::-1], fontsize=6)
ax.set_xticks([wx(w) for w in range(1, NWEEKS + 1)])
ax.set_xticklabels([f"{w}\n{wstart(w):%d.%m}" for w in range(1, NWEEKS + 1)], fontsize=4.6, linespacing=1.15)
ax.set_xlim(0.4, wx(NWEEKS) + 0.6); ax.set_ylim(-0.6, len(TASKS) + 0.3)
ax.set_xlabel("рабочая неделя проекта и дата её начала (неделя 1 — 16.11.2026)", fontsize=6)
for s_ in ["top", "right"]:
    ax.spines[s_].set_visible(False)
ax.spines["left"].set_linewidth(0.5); ax.spines["bottom"].set_linewidth(0.5)
ax.tick_params(width=0.5, length=2)
ax.grid(axis="x", color="#E5E5E5", lw=0.4); ax.set_axisbelow(True)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=COL[k], ec=RED if k == "buf" else "none", hatch="////" if k == "buf" else None,
                         lw=0.5, label=NAMES[k]) for k in COL],
          fontsize=5.5, ncol=7, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.22), handlelength=1,
          columnspacing=1)
fig.tight_layout(pad=0.3)
fig.savefig(f"{OUT}/roadmap.png", dpi=DPI, facecolor="white")
plt.close(fig)

# ---------------------------------------------------------------- риски
RISKS = [  # id, коротко, P, I, P_ост, I_ост, группа
    ("R1", "Витрина не обновилась в срок", 3, 3, 2, 2, "Данные"),
    ("R2", "Нет «файла от бизнеса» / сломан формат", 4, 3, 2, 2, "Данные"),
    ("R3", "Пропуски и ошибки в данных", 3, 4, 2, 3, "Данные"),
    ("R13", "Изменилась схема источника", 3, 3, 2, 2, "Данные"),
    ("R4", "Кластеры «прыгают»", 4, 4, 2, 3, "Модель"),
    ("R5", "Мало ТК: мелкие, неустойчивые кластеры", 4, 3, 3, 2, "Модель"),
    ("R7", "Кластеры не интерпретируемы", 3, 4, 2, 3, "Модель"),
    ("R9", "Утечка коммерческих данных", 2, 5, 1, 5, "Сервис и ИБ"),
    ("R10", "Не держим SLA по времени", 2, 2, 1, 2, "Сервис и ИБ"),
    ("R6", "Недоверие пользователей", 3, 5, 2, 4, "Люди и процесс"),
    ("R11", "Уход ключевого сотрудника", 2, 3, 1, 3, "Люди и процесс"),
    ("R12", "Расширение скоупа", 3, 3, 2, 2, "Люди и процесс"),
    ("R8", "Эффект ниже затрат", 3, 3, 2, 3, "Бизнес-ценность"),
    ("R14", "Задержка доступов и ИБ", 4, 3, 2, 3, "Люди и процесс"),
    ("R15", "Смена или недоступность ЛПР", 2, 4, 1, 4, "Люди и процесс"),
    ("R16", "Неверная бизнес-гипотеза", 2, 5, 2, 3, "Бизнес-ценность"),
]


def level(s):
    if s >= 15: return "критический", "#F2A0A0", RED
    if s >= 10: return "высокий", "#FFC98F", "#A04A00"
    if s >= 5: return "средний", "#FFE9A6", "#7A5A00"
    return "низкий", "#CFE8C4", GREEN


def matrix(fname, residual=False):
    fig = plt.figure(figsize=(4.3, 3.3))
    ax = fig.add_axes([0.17, 0.18, 0.57, 0.78])
    for p in range(1, 6):
        for i in range(1, 6):
            _, fc, _ = level(p * i)
            ax.add_patch(Rectangle((p - 0.5, i - 0.5), 1, 1, fc=fc, ec="white", lw=1.2))
            ax.text(p + 0.42, i - 0.42, str(p * i), fontsize=5, color="#00000066", ha="right", va="bottom")
    cells = {}
    for r in RISKS:
        p, i = (r[4], r[5]) if residual else (r[2], r[3])
        cells.setdefault((p, i), []).append(r[0])
    for (p, i), ids in cells.items():
        txt = "\n".join(" ".join(ids[k:k + 2]) for k in range(0, len(ids), 2))
        ax.text(p, i, txt, fontsize=7, fontweight="bold", ha="center", va="center", color=BLUE, linespacing=1.15)
    ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
    ax.set_xticklabels(["1\nредко", "2", "3", "4", "5\nпочти\nточно"], fontsize=6)
    ax.set_yticklabels(["1 незначит.", "2", "3", "4", "5 критич."], fontsize=6)
    ax.set_xlabel("Вероятность (P)", fontsize=7, fontweight="bold", color=BLUE)
    ax.set_ylabel("Влияние (I)", fontsize=7, fontweight="bold", color=BLUE)
    ax.tick_params(length=0)
    for s in ax.spines.values(): s.set_visible(False)
    lx = fig.add_axes([0.77, 0.30, 0.22, 0.5]); lx.axis("off"); lx.set_xlim(0, 1); lx.set_ylim(0, 1)
    lx.text(0, 0.98, "Уровень = P × I", fontsize=6.5, fontweight="bold", va="top")
    for k, (lab, rng, s) in enumerate([("критический", "15–25", 16), ("высокий", "10–14", 12),
                                       ("средний", "5–9", 6), ("низкий", "1–4", 2)]):
        _, fc, tc = level(s)
        y = 0.80 - k * 0.19
        lx.add_patch(Rectangle((0, y - 0.06), 0.17, 0.12, fc=fc, ec="none"))
        lx.text(0.23, y + 0.02, lab, fontsize=6, va="center", color=tc, fontweight="bold")
        lx.text(0.23, y - 0.05, rng, fontsize=5.5, va="center", color=GRAY)
    fig.savefig(f"{OUT}/{fname}", dpi=DPI, facecolor="white")
    plt.close(fig)


matrix("risk_matrix.png")
matrix("risk_matrix_residual.png", residual=True)

# ---------------------------------------------------------------- компактные этапы для слайдов
def slide_stages(items, fname, footer, below=0.4):
    W, H = 5.5, 1.18 + below
    bw, gap, bh = 0.66, 0.12, 1.08
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    y0 = below
    x = 0.06
    centers = []
    for it in items:
        num, title, roles, weeks, out = it
        if num.startswith("G"):
            cx, cy, r = x + bw / 2, y0 + bh / 2, 0.36
            ax.add_patch(Polygon([(cx, cy + r), (cx + r * 0.95, cy), (cx, cy - r), (cx - r * 0.95, cy)],
                                 fc="#FFF4E0", ec=AMBER, lw=0.9))
            ax.text(cx, cy + 0.07, title, fontsize=6.3, fontweight="bold", ha="center", va="center", color=AMBER)
            ax.text(cx, cy - 0.09, roles.replace(" + ", "+\n") if "+" in roles else roles.replace(" ", "\n"),
                    fontsize=4.6, ha="center", va="center", linespacing=1.0)
            ax.text(cx - 0.04, y0 + 0.02, weeks, fontsize=5, ha="right", va="center", color=GRAY)
        else:
            hc = GREEN if num == "10" else BLUE
            ax.add_patch(Rectangle((x, y0), bw, bh, fc=LIGHT, ec=hc, lw=0.8))
            ax.add_patch(Rectangle((x, y0 + bh - 0.18), bw, 0.18, fc=hc, ec=hc, lw=0.8))
            ax.text(x + bw / 2, y0 + bh - 0.09, f"Этап {num}", color="white", fontsize=6.3, fontweight="bold",
                    ha="center", va="center")
            ax.text(x + bw / 2, y0 + bh - 0.42, title, fontsize=5.7, fontweight="bold", ha="center", va="center",
                    linespacing=1.08)
            ax.text(x + bw / 2, y0 + 0.36, roles.replace(" · бизнес · ", " · бизнес\n· "), fontsize=5.1,
                    ha="center", va="center", color=hc, fontweight="bold", linespacing=1.0)
            ax.text(x + bw / 2, y0 + 0.12, weeks, fontsize=5.1, ha="center", va="center", color=GRAY)
        centers.append((x, x + bw, x + bw / 2))
        x += bw + gap
    for a, b in zip(centers, centers[1:]):
        arrow(ax, (a[1] + 0.005, y0 + bh / 2), (b[0] - 0.005, y0 + bh / 2))
    footer(ax, centers, y0, bh)
    fig.savefig(f"{OUT}/{fname}", dpi=DPI, facecolor="white")
    plt.close(fig)


def short(items):
    m = {"Требования и\nкритерии успеха": "Требования,\nкритерии\nуспеха",
         "Доступы, EDA,\nкачество данных": "Доступы,\nEDA, DQ",
         "ETL и витрина\nпризнаков v0": "ETL и\nвитрина v0",
         "Бейзлайн:\nправила бизнеса": "Бейзлайн:\nправила\nбизнеса",
         "MVP: PCA + Ward,\nвыбор k": "MVP:\nPCA + Ward,\nвыбор k",
         "Офлайн-оценка\nпротив бейзлайна": "Офлайн-\nоценка vs\nбейзлайн",
         "Excel-отчёт и\nпрофили кластеров": "Excel-отчёт,\nпрофили\nкластеров",
         "API-сервис\n(FastAPI)": "API-сервис\n(FastAPI)",
         "UI Streamlit,\nSSO, логирование": "UI Streamlit,\nSSO, логи",
         "Тесты в dev:\nфункц. и нагрузка": "Тесты в dev:\nфункц.,\nнагрузка",
         "Пилот: офлайн,\nэксперты, процесс": "Пилот:\nретро, эксперты,\nпроцесс",
         "Прод, мониторинг,\nпередача в поддержку": "Прод,\nмониторинг,\nподдержка"}
    return [(a, m.get(b, b), c, d, e) for a, b, c, d, e in items]


def f1(ax, c, y0, bh):
    g, m = c[6], c[4]
    yl = 0.14
    ax.plot([g[2], g[2]], [y0 + bh / 2 - 0.36, yl], color=RED, lw=0.7)
    ax.plot([g[2], m[2]], [yl, yl], color=RED, lw=0.7)
    arrow(ax, (m[2], yl), (m[2], y0), color=RED)
    ax.text((g[2] + m[2]) / 2 + 0.05, yl + 0.03, "нет: доработка, не больше 2 итераций", color=RED, fontsize=5,
            ha="center", va="bottom")
    ax.text(g[2], y0 + bh / 2 + 0.41, "да → этап 6", color=GREEN, fontsize=5, fontweight="bold", ha="center")


def f2(ax, c, y0, bh):
    g = c[5]
    short_lab = ["Q3, Q4 → этап 8: UI и процесс", "p95, ошибки → этапы 7–9", "ML-метрики, Q1, Q2 → этап 4"]
    step = 0.15
    lanes = [y0 - 0.12 - step * i for i in range(3)]
    ax.plot([g[2], g[2]], [y0 + bh / 2 - 0.36, lanes[-1]], color=RED, lw=0.7)
    for (idx, _), lab, yl in zip(REWORK, short_lab, lanes):
        if idx is None:
            xt = c[0][0] + 0.02
            arrow(ax, (g[2], yl), (xt, yl), color=RED)
            ax.text(xt + 0.04, yl + 0.02, lab, color=RED, fontsize=5, ha="left", va="bottom")
        else:
            xt = c[idx][2]
            ax.plot([g[2], xt], [yl, yl], color=RED, lw=0.7)
            arrow(ax, (xt, yl), (xt, y0), color=RED)
            ax.text(xt + 0.04, yl + 0.02, lab, color=RED, fontsize=5, ha="left", va="bottom")
    ax.text(g[2] + 0.05, y0 - 0.04, "доработка:\n+3 нед., 1 раз", color=RED, fontsize=4.8, fontweight="bold",
            ha="left", va="top", linespacing=1.05)
    ax.text(g[2] + 0.05, lanes[-1] + 0.02, "no-go →\nплан Б", color=RED, fontsize=4.8, fontweight="bold",
            ha="left", va="bottom", linespacing=1.05)
    ax.text(g[2] + 0.38, y0 + bh / 2 + 0.04, "go", color=GREEN, fontsize=5.3, fontweight="bold", ha="center",
            va="bottom")


slide_stages(short(ROW1), "stages_slide1.png", f1)
slide_stages(short(ROW2), "stages_slide2.png", f2, below=0.56)
print("slides done")
