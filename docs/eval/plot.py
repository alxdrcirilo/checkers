import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read data
df = pd.read_csv(filepath_or_buffer="docs/eval/results.csv")

# Plot: boxplot games won by AI (WHITE)
fig, ax = plt.subplots()
sns.boxplot(data=df, x="depth", y="WHITE", ax=ax)
ax.set(ylim=(0, 100), xlabel="Depth", ylabel="Number of games won (AI)")
lines = ax.get_lines()
categories = ax.get_xticks()

# source: https://stackoverflow.com/a/56879116
for cat in categories:
    y_min = int(lines[cat * 6].get_ydata()[0])
    y = int(lines[4 + cat * 6].get_ydata()[0])

    ax.text(
        cat,
        y_min - 20,
        f"{y}",
        ha="center",
        va="center",
        size=9,
        fontweight="bold",
        color="white",
        bbox=dict(facecolor="#445A64"),
    )
sns.despine()
plt.savefig("plot_games_won.png")

# Plot: BLACK vs WHITE games won
fig, ax = plt.subplots()
sns.lineplot(data=df, x="depth", y="BLACK", ax=ax)
sns.lineplot(data=df, x="depth", y="WHITE", ax=ax)
ax.set(ylim=(0, 100), xlabel="Depth", ylabel="Number of games won")
sns.despine()
plt.savefig("plot_BLACK_vs_WHITE.png")

# Plot: runtime
fig, ax = plt.subplots()
sns.lineplot(data=df, x="depth", y="runtime", ax=ax)
ax.set(xlabel="Depth", ylabel="Runtime (min)")
sns.despine()
plt.savefig("plot_runtime.png")
