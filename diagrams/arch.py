"""Схема архитектуры сервиса кластеризации."""
import sys, dataclasses
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
for f in ["cmu-sans-serif-500-roman.ttf", "cmu-sans-serif-700-roman.ttf", "cmu-sans-serif-500-italic.ttf"]:
    font_manager.fontManager.addfont(f"fonts/{f}")
font_manager.fontManager.ttflist = [dataclasses.replace(e, stretch="normal") if e.name == "CMU Sans Serif" else e
                                    for e in font_manager.fontManager.ttflist]
plt.rcParams["font.family"] = "CMU Sans Serif"

BLUE, LIGHT, GREEN, AMBER, GRAY = "#003366", "#F0F0F0", "#006400", "#AA6400", "#555555"
W, H = 6.6, 3.45
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")


def group(x, y, w, h, title, solid=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06", fc="none",
                                ec=BLUE if solid else "#7A93AC", lw=1.1 if solid else 0.7,
                                ls="-" if solid else (0, (4, 2))))
    ax.text(x + 0.08, y + h - 0.06, title, fontsize=6.8, fontweight="bold", color=BLUE, va="top")


def box(x, y, w, h, title, sub="", fc=LIGHT, ec=BLUE):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.8))
    if sub:
        ax.text(x + w / 2, y + h - 0.1, title, fontsize=6.5, fontweight="bold", ha="center", va="center")
        ax.text(x + w / 2, y + (h - 0.18) / 2, sub, fontsize=5.2, ha="center", va="center", color="#222222",
                linespacing=1.1)
    else:
        ax.text(x + w / 2, y + h / 2, title, fontsize=6.5, fontweight="bold", ha="center", va="center")
    return dict(l=x, r=x + w, b=y, t=y + h, cx=x + w / 2, cy=y + h / 2)


def cyl(x, y, w, h, title, sub):
    e = 0.12
    ax.add_patch(Rectangle((x, y + e / 2), w, h - e, fc="#FFF4D6", ec="none"))
    ax.plot([x, x], [y + e / 2, y + h - e / 2], color=AMBER, lw=0.8)
    ax.plot([x + w, x + w], [y + e / 2, y + h - e / 2], color=AMBER, lw=0.8)
    ax.add_patch(Ellipse((x + w / 2, y + e / 2), w, e, fc="#FFF4D6", ec=AMBER, lw=0.8))
    ax.add_patch(Rectangle((x + 0.01, y + e / 2), w - 0.02, 0.07, fc="#FFF4D6", ec="none"))
    ax.add_patch(Ellipse((x + w / 2, y + h - e / 2), w, e, fc="#FFE8B0", ec=AMBER, lw=0.8))
    ax.text(x + w / 2, y + h - 0.22, title, fontsize=6.5, fontweight="bold", ha="center", va="center")
    ax.text(x + w / 2, y + (h - 0.3) / 2 + 0.02, sub, fontsize=5.2, ha="center", va="center", linespacing=1.1)
    return dict(l=x, r=x + w, b=y, t=y + h, cx=x + w / 2, cy=y + h / 2)


def arr(p1, p2, both=False, color="#333333", ls="-", label=None, lpos=0.5, loff=(0, 0.05), conn="arc3"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="<|-|>" if both else "-|>", mutation_scale=6, color=color,
                                 lw=0.7, ls=ls, shrinkA=0, shrinkB=0, connectionstyle=conn))
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + loff[0]
        my = p1[1] + (p2[1] - p1[1]) * lpos + loff[1]
        ax.text(mx, my, label, fontsize=5, color=GRAY, ha="center", va="bottom", style="italic",
                bbox=dict(fc="white", ec="none", pad=0.6))


# ---- источники
group(0.08, 0.78, 1.32, 2.6, "Источники")
src = [("DWH", "продажи, операции,\nдоли категорий, dim_store"), ("CRM / лояльность", "клиентские KPI\n(агрегаты по ТК)"),
       ("Геосервис", "изохроны, конкуренты,\nдоход населения"), ("Файл от бизнеса", "xlsx по шаблону,\nраз в квартал")]
S = []
for k, (t, s) in enumerate(src):
    S.append(box(0.18, 2.72 - k * 0.6, 1.12, 0.48, t, s))

# ---- ETL
group(1.6, 1.35, 1.35, 1.45, "ETL · Airflow")
dag = box(1.68, 1.48, 1.19, 1.05, "DAG store_features",
          "раз в квартал +\nручной запуск\n\nизвлечение → DQ →\nвитрина → версия")
for s in S:
    arr((s["r"], s["cy"]), (dag["l"], dag["cy"] + (s["cy"] - 2.0) * 0.25))

# ---- хранилища
group(3.15, 0.78, 1.15, 2.6, "Хранилища")
s3 = cyl(3.25, 2.2, 0.95, 0.82, "S3 + DVC", "витрина признаков\n(parquet),\nверсия = квартал")
pg = cyl(3.25, 0.95, 0.95, 0.9, "PostgreSQL", "текущая версия,\nэталон квартала,\nкэш, журнал")
arr((dag["r"], dag["cy"] + 0.2), (s3["l"], s3["cy"]), label="parquet", lpos=0.45)
arr((dag["r"], dag["cy"] - 0.2), (pg["l"], pg["cy"] + 0.1), label="версия", lpos=0.45, loff=(0, -0.13))

# ---- k8s
group(4.45, 0.78, 1.33, 2.6, "Kubernetes · dev / prod", solid=True)
ing = box(4.53, 2.62, 1.17, 0.46, "nginx ingress", "+ oauth2-proxy\n(SSO через AD)", fc="#E6DDF0", ec="#6A4C93")
ui = box(4.53, 1.82, 1.17, 0.58, "Streamlit UI", "выбор ТК, признаков, k;\nдендрограмма, профили,\nэкспорт в Excel",
         fc="#DCE8F5")
api = box(4.53, 0.9, 1.17, 0.7, "Clustering API", "FastAPI: POST /clusterings,\nGET /reports/{id}, /health\n"
          "библиотека: бейзлайн,\nPCA + Ward, выбор k", fc="#DCE8F5")
arr((ing["cx"], ing["b"]), (ui["cx"], ui["t"]), both=True)
arr((ui["cx"], ui["b"]), (api["cx"], api["t"]), both=True, label="REST", loff=(0.13, -0.05))
arr((api["l"], api["cy"] + 0.2), (s3["r"], s3["cy"] - 0.15), label="чтение витрины", lpos=0.5, loff=(0.02, 0.06))
arr((api["l"], api["cy"] - 0.1), (pg["r"], pg["cy"] - 0.05), both=True, label="кэш, журнал", loff=(0, 0.03))

# ---- пользователь
ax.text(6.18, 2.98, "Пользователи", fontsize=6.5, fontweight="bold", ha="center")
ax.text(6.18, 2.62, "~10 человек,\nCVP и коммерция", fontsize=5.2, ha="center", va="center", linespacing=1.1)
ax.text(6.18, 2.3, "ЛПР получает\nExcel-отчёт", fontsize=5.2, ha="center", va="center", color=GRAY,
        linespacing=1.1)
arr((ing["r"], ing["cy"]), (5.95, ing["cy"]), both=True)
ax.text((ing["r"] + 5.95) / 2, ing["cy"] + 0.06, "HTTPS", fontsize=4.6, color=GRAY, ha="center", style="italic")

# ---- эксплуатация
group(0.08, 0.06, 6.5, 0.6, "Эксплуатация")
ci = box(4.6, 0.13, 1.85, 0.42, "GitLab CI/CD", "test → build → dev; тег main → prod", fc="#E8F2E3", ec=GREEN)
mon = box(1.35, 0.13, 1.5, 0.42, "Prometheus + Grafana", "метрики, алерты → почта", fc="#E8F2E3", ec=GREEN)
log = box(3.05, 0.13, 1.35, 0.42, "ELK", "логи, аудит запусков (кто, что)", fc="#E8F2E3", ec=GREEN)
arr((api["l"] + 0.1, api["b"]), (log["r"] - 0.15, log["t"]), ls=(0, (3, 2)))
arr((api["l"] + 0.04, api["b"] + 0.08), (mon["r"] - 0.1, mon["t"]), ls=(0, (3, 2)), label="метрики", lpos=0.7, loff=(0, -0.02))
arr((dag["cx"] - 0.2, dag["b"]), (mon["cx"] - 0.2, mon["t"]), ls=(0, (3, 2)), label="SLA DAG, DQ", lpos=0.5,
    loff=(0, 0))
arr((ci["l"] + 0.45, ci["t"]), (ci["l"] + 0.45, 0.78), ls=(0, (1, 1.5)), color=GREEN)
ax.text(ci["l"] + 0.49, 0.69, "деплой", fontsize=4.8, color=GREEN, ha="left", style="italic")

fig.savefig(f"{OUT}/scheme_architecture.png", dpi=300, facecolor="white")
print("ok")
