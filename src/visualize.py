import json
import sys
import re
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import config

STRATEGIES = ["bfs", "inlink", "bm25", "semantic"]
COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]

# support loading a serialized experiment's results via its exp id
def load_results(experiment_id):
    experiment_dir = Path(config.RESULTS_DIR) / experiment_id
    results = {}
    for path in sorted(experiment_dir.glob("*.json")):
        topic = path.stem
        with open(path, "r", encoding="utf-8") as f:
            results[topic] = json.load(f)
    return results

# load the sub-graph for a given topic, respecting the depth of each node
def load_graph(topic):
    # load graph from the topic path
    graph_path = Path(config.OUTPUT_DIR) / f"{topic}.json"

    with open(graph_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # get the depth of each node
    depths = {node: content.get("depth", -1) for node, content in data["nodes"].items()}
    return depths

# routine which plots the score for a given topic
def plot_topic(experiment_id, topic, data, results_dir):
    # retrieve the scores for each strategy in the experiment
    strategies = [s for s in STRATEGIES if s in data]
    scores = [data[s]["score"] for s in strategies]

    # define the plot characteristics and save
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(strategies, scores, color=COLORS[:len(strategies)], width=0.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Avg Cosine Similarity")
    ax.set_title(f"{topic.replace('_', ' ')}")
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{score:.3f}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    out_path = results_dir / f"{experiment_id}_{topic}_scores.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path.name}")

# plots average results for an entire experiment
def plot_overall(experiment_id, all_results, results_dir):
    # retrieve all topics, strategies, and calculate the average score for each strategy
    totals = defaultdict(float)
    counts = defaultdict(int)
    for topic_data in all_results.values():
        for strategy, result in topic_data.items():
            totals[strategy] += result["score"]
            counts[strategy] += 1
    strategies = [s for s in STRATEGIES if s in totals]
    averages = [totals[s] / counts[s] for s in strategies]

    # define plot characteristics and save
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(strategies, averages, color=COLORS[:len(strategies)], width=0.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Avg Cosine Similarity")
    ax.set_title("Overall Average Score by Strategy")
    for bar, avg in zip(bars, averages):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{avg:.3f}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    out_path = results_dir / f"{experiment_id}_overall_scores.png"
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path.name}")

# this is a fancy custom routine to plot a unique visualization of a topic's crawl data
# each dot represents an article crawled by at least one strategy
# they are color coded and grouped according to which strategy(s) crawled the article
# the higher the article's score, the higher it is from the center
# NOTE: we do not plot the BFS strategy because it would mess up the triangular display
# This is fine, since BFS is the most basic strategy with no heuristic to improve results
def plot_subgraph(experiment_id, topic, data, results_dir):
    import random
    import numpy as np
    random.seed(42)

    STRATEGY_COLORS = {
        "inlink":   np.array([1.0,  0.85, 0.0 ]), # yellow
        "bm25":     np.array([0.85, 0.1,  0.1 ]), # red
        "semantic": np.array([0.15, 0.4,  0.85]), # blue
    }
    BLACK = (0.0, 0.0, 0.0)

    # Anchoring locations in an upside-down Y shape: inlink=up, bm25=bottom-left, semantic=bottom-right
    anchors = {
        "inlink":   np.array([ 0.0,    1.0 ]),
        "bm25":     np.array([-0.866, -0.5 ]),
        "semantic": np.array([ 0.866, -0.5 ]),
    }

    # load all node's depth
    depths = load_graph(topic)
    max_depth = max(depths.values(), default=1)

    # Build the node -> strategies map (excluding bfs)
    node_strategies = defaultdict(set)
    for strategy, result in data.items():
        if strategy == "bfs":
            continue # skip bfs-only articles
        for title in result["visited"]:
            node_strategies[title].add(strategy)

    # edge case handling; should not occur under regular usage
    if not node_strategies:
        print(f"No visited nodes found for subgraph plot: {topic}")
        return

    # Assign color and position to each visited node
    positions = {}
    node_colors = {}
    for node, strategies in node_strategies.items():
        relevant = [s for s in strategies if s in anchors]
        if not relevant:
            continue

        # if crawled by all 3, we assign black
        if len(relevant) == 3:
            node_colors[node] = BLACK
        else:
            # handle mixed colors
            mixed = sum(STRATEGY_COLORS[s] for s in relevant) / len(relevant)
            node_colors[node] = tuple(mixed)

        # Direction is handled by summing the anchors for all strategies used for node
        # If only one strategy, it will use the default anchor
        direction = sum(anchors[s] for s in relevant)
        norm = np.linalg.norm(direction)
        if norm > 0:
            direction = direction / norm

        # Radius of the node is set to the average semantic score across it's visited strategies, normalized to [0.15, 1.0]
        scores_for_node = [data[s]["node_scores"].get(node, 0.0) for s in relevant if s in data]
        avg_node_score = sum(scores_for_node) / len(scores_for_node) if scores_for_node else 0.0

        # bind to [0, 1] since scores are able to be negative
        avg_node_score = max(0.0, min(1.0, avg_node_score))
        radius = 0.15 + 0.85 * avg_node_score

        # Scatter each node slightly perpendicular to the arm direction
        # each node gets a random jitter factor that helps spread out the points for visibility purposes
        # radius is preserved
        perpendicular = np.array([-direction[1], direction[0]])
        jitter = perpendicular * random.uniform(-0.22, 0.22) + direction * random.uniform(-0.04, 0.04)
        positions[node] = direction * radius + jitter

    # visualization definitions
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor("white")

    # draw concentric rings at 0.1 intervals
    # these enable you to see what scores the nodes of each strategies cluster around
    for score in [i * 0.1 for i in range(1, 11)]:
        r = 0.15 + 0.85 * score
        circle = plt.Circle((0, 0), r, color="lightgray", fill=False,
                             linewidth=0.6, linestyle="--", zorder=1)
        ax.add_patch(circle)
        ax.text(0.02, r + 0.01, f"{score:.1f}", fontsize=7, color="gray",
                ha="left", va="bottom", zorder=2)

    # Draw arms as thick black lines for each strategy
    for name, vec in anchors.items():
        ax.plot([0, vec[0]], [0, vec[1]], color="black", linewidth=4, zorder=1, solid_capstyle="round")

    # Plot each visited node according to the position we caluclated earlier
    xs = [positions[n][0] for n in positions]
    ys = [positions[n][1] for n in positions]
    colors = [node_colors[n] for n in positions]
    ax.scatter(xs, ys, c=colors, s=35, zorder=3, alpha=0.90, linewidths=0)

    # labels
    for name, vec in anchors.items():
        ax.text(vec[0] * 1.12, vec[1] * 1.12, name, ha="center", va="center",
                fontsize=13, fontweight="bold")

    # legend definition - shows which colors correspond to each of the strategy options
    legend_items = [
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple(STRATEGY_COLORS["inlink"]), markersize=10, label="inlink"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple(STRATEGY_COLORS["bm25"]),   markersize=10, label="bm25"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple(STRATEGY_COLORS["semantic"]),markersize=10, label="semantic"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple((STRATEGY_COLORS["inlink"]+STRATEGY_COLORS["bm25"])/2), markersize=10, label="inlink + bm25"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple((STRATEGY_COLORS["inlink"]+STRATEGY_COLORS["semantic"])/2), markersize=10, label="inlink + semantic"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=tuple((STRATEGY_COLORS["bm25"]+STRATEGY_COLORS["semantic"])/2), markersize=10, label="bm25 + semantic"),
        plt.Line2D([0],[0], marker="o", color="w", markerfacecolor=BLACK, markersize=10, label="all three"),
    ]
    ax.legend(handles=legend_items, loc="lower center", fontsize=9, ncol=4,
              bbox_to_anchor=(0.5, -0.02), frameon=True)

    # final properties, and then save to png
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{topic.replace('_', ' ')} — Crawl Coverage by Strategy", pad=20, fontsize=14)

    plt.tight_layout()
    out_path = results_dir / f"{experiment_id}_{topic}_subgraph.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path.name}")

# main routine that develops both the score bar chart and the subgraph visualization for each topic in the experiment
# it also plots the overall average score bar chart
def main(experiment_id):
    results_dir = Path(config.RESULTS_DIR) / experiment_id
    all_results = load_results(experiment_id)
    if not all_results:
        print(f"No results found for experiment: {experiment_id}")
        return
    print(f"Found {len(all_results)} topics for experiment {experiment_id}")
    for topic, data in all_results.items():
        plot_topic(experiment_id, topic, data, results_dir)
        plot_subgraph(experiment_id, topic, data, results_dir)
    plot_overall(experiment_id, all_results, results_dir)
    print("Done.")

# main entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <experiment_id>")
        print("Example: python visualize.py 20260502_195517")
        sys.exit(1)
    main(sys.argv[1])
