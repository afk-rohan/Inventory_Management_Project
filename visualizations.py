import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.cm as cm
import numpy as np

# Base UI tuning for clean Material look
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#E0E0E0",
    "axes.labelcolor": "#212121",
    "xtick.color": "#424242",
    "ytick.color": "#424242",
    "text.color": "#212121",
    "font.size": 10
})

# --------------------------------------------------
# Helper: gradient colors
# --------------------------------------------------
def gradient_colors(n, cmap_name="cool"):
    cmap = cm.get_cmap(cmap_name)
    return [cmap(i) for i in np.linspace(0.2, 0.9, n)]


# --------------------------------------------------
# 1. Sales by Ship-State (Gradient, Horizontal)
# --------------------------------------------------
def plot_sales_by_state(orders, top_n=10):
    state_sales = defaultdict(float)

    for o in orders:
        if o.ship_state:
            state_sales[o.ship_state] += o.amount

    sorted_states = sorted(
        state_sales.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_states = sorted_states[:top_n]
    others = sum(v for _, v in sorted_states[top_n:])

    states = [s for s, _ in top_states]
    sales = [v for _, v in top_states]

    if others > 0:
        states.append("Others")
        sales.append(others)

    colors = gradient_colors(len(states), "cool")

    plt.figure(figsize=(10, 6))
    plt.barh(states, sales, color=colors)
    plt.xlabel("Total Sales Amount")
    plt.ylabel("Ship State")
    plt.title("Top States by Sales")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# 2. Order Status Distribution (Gradient Pie)
# --------------------------------------------------
def plot_status_distribution(orders):
    status_count = defaultdict(int)

    for o in orders:
        status_count[o.status] += 1

    total = sum(status_count.values())

    labels, sizes = [], []
    others = 0

    for status, count in status_count.items():
        percent = (count / total) * 100
        if percent >= 3:
            labels.append(status)
            sizes.append(count)
        else:
            others += count

    if others > 0:
        labels.append("Others")
        sizes.append(others)

    colors = gradient_colors(len(labels), "cool")

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors
    )
    plt.title("Order Status Distribution")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# 3. Sales by Category (Gradient Bars)
# --------------------------------------------------
def plot_sales_by_category(category_data):
    categories = list(category_data.keys())
    amounts = [category_data[c]["amount"] for c in categories]

    colors = gradient_colors(len(categories), "cool")

    plt.figure(figsize=(9, 5))
    plt.bar(categories, amounts, color=colors)
    plt.xlabel("Category")
    plt.ylabel("Total Sales Amount")
    plt.title("Sales by Category")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# 4. Sales Trend Over Time (Pink-Blue Line)
# --------------------------------------------------
def plot_sales_trend(orders):
    monthly_sales = defaultdict(float)

    for o in orders:
        if o.date:
            date = o.date.replace("/", "-")
            parts = date.split("-")
            if len(parts) == 3:
                month_year = parts[1] + "-" + parts[2]
                monthly_sales[month_year] += o.amount

    months = sorted(monthly_sales.keys())
    sales = [monthly_sales[m] for m in months]

    plt.figure(figsize=(10, 4))
    plt.plot(
        months,
        sales,
        marker="o",
        linewidth=2,
        color=cm.cool(0.7)
    )
    plt.xlabel("Month-Year")
    plt.ylabel("Total Sales Amount")
    plt.title("Sales Trend Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()
