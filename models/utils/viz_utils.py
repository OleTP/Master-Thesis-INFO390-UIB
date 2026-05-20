import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import json
from pathlib import Path



def print_classification_report(results: dict, labels: tuple = ("rik", "fattig", "uviten"), title: str = ""):
    """
    Print sklearn classification_report for a list of result dicts.

    :param results: Dict with a result from a classification. Must contain [true_label, pred_label]
    :param labels: Labels in the classification report(fixed label order)
    :param title: Optional title header
    """
    y_true = [r["true_label"] for category_results in results.values() for r in category_results]
    y_pred = [r["pred_label"] for category_results in results.values() for r in category_results]

    if title:
        print("\n" + "=" * 80)
        print(title)

    print(classification_report(y_true, y_pred, labels=list(labels), digits=2, zero_division=0))


def print_confusion_matrix(results: dict, labels: tuple = ("rik", "fattig", "uviten"), title: str = ""):
    """
    Plots a single confusion matrix for a list of result dicts.

    :param results: Dict with a result from a classification. Must contain [true_label, pred_label]
    :param labels: Labels in the confusion matrix (fixed label order)
    :param title: Optional plot title
    """
    y_true = [r["true_label"] for category_results in results.values() for r in category_results]
    y_pred = [r["pred_label"] for category_results in results.values() for r in category_results]

    cm = confusion_matrix(y_true, y_pred, labels=list(labels), normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(labels))

    if title.startswith('norwai'):
        color = "Blues"
    elif title.startswith('normistral'):
        color = "Oranges"
    else:
        color = "Greens"

    fig, ax = plt.subplots(figsize=(7, 5))
    disp.plot(
        ax=ax,
        cmap=color,          
        values_format=".1%",    
        xticks_rotation=45,
        colorbar=False
    )

    ax.set_title(title or "Confusion Matrix")
    plt.tight_layout()
    plt.show()

def filter_results(results: dict, category: str | None = None, change: str | None = None) -> dict:
    """
    Filter results by category and/or change. 
    This is used to look at differences in specific categorys and adverbs.
    """
    if category:
        results = {category: results.get(category, [])}

    if change:
        results = {
            cat: [r for r in res if r["change"] == change]
            for cat, res in results.items()
        }

    return results


def print_reasons_count(results: dict, title: str = ""):
    """
    Print count of each pred_label_reason for uviten predictions, and correct predictions.
    
    :param results: Dict with results organized by category
    :param title: Optional title header
    """
    all_results = [r for category_results in results.values() for r in category_results]
    
    if not all_results:
        print("No results found")
        return
    
    uviten_results = [r for r in all_results if r['pred_label'] == 'uviten']
    
    if title:
        print("\n" + "=" * 80)
        print(title)
    
    # Print uviten sources
    if uviten_results:
        print("\nSources of uviten:")
        df_uviten = pd.DataFrame(uviten_results)
        reason_counts_uviten = df_uviten['pred_label_reason'].value_counts().sort_values(ascending=False)
        for reason, count in reason_counts_uviten.items():
            print(f"{reason}: {count}")
    else:
        print("\nNo uviten predictions found")
    
    # Print correct prediction sources (correct_label and negation only)
    print("\nSources of Predictions:")
    df_all = pd.DataFrame(all_results)

    correct_reasons = df_all[df_all['pred_label_reason'].isin(['correct_label', 'negation'])]
    reason_counts_correct = correct_reasons['pred_label_reason'].value_counts().sort_values(ascending=False)
    for reason, count in reason_counts_correct.items():
        print(f"{reason}: {count}")




def plot_bias_distribution(data: dict, mode: str = "base", title: str = "", figsize: tuple = (16, 14), show_labels: bool = True, target_labels_to_show: list = None):
    """
    Universal function to plot bias distribution.
    
    :param data: Nested dict with structure: {"category/type": {"target": {"always": {"rich": x, "poor": y}, "never": {"rich": x, "poor": y}}, ...}, ...}
    :param mode: "base" or "intersectionality"
    :param title: Title for the plot
    :param figsize: Figure size (width, height)
    :param show_labels: Whether to show target labels on the plot (default: True)
    :param target_labels_to_show: List of target names to show labels for. Only used when show_labels=False. If None and show_labels=False, no labels are shown. If show_labels=True, all labels are shown.
    :return: tuple (fig, ax)
    """
    
    # Set colors based on mode
    if mode == "base":
        color_mapping = {
            "Immigration": "#d62728",
            "Region": "#1f77b4",
            "Oslo": "#2ca02c",
        }
    elif mode == "intersectionality":
        color_mapping = {
            "Region and Immigration": "#1f77b4",
            "Oslo and Immigration": "#2ca02c",
        }
    else:
        raise ValueError("mode must be 'base' or 'intersectionality'")
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Setup axes with reference areas and lines
    ax.axhspan(0, 100, xmin=0.5, xmax=1.0, alpha=0.06, color='red')
    ax.axhspan(-100, 0, xmin=0.0, xmax=0.5, alpha=0.06, color='blue')
    
    ax.axhline(0, color='black', linewidth=2.0, alpha=0.8)
    ax.axvline(0, color='black', linewidth=2.0, alpha=0.8)
    
    ax.plot([-100, 100], [-100, 100], color='gray', linewidth=1.5, linestyle='-', alpha=0.35)
    ax.plot([-100, 100], [100, -100], color='gray', linewidth=1.5, linestyle='--', alpha=0.35)
    
    for category, targets_dict in data.items():
        color = color_mapping.get(category, "#808080") 
        
        for target, rates in targets_dict.items():
            x = rates["always"]["poor"] - rates["always"]["rich"]
            y = rates["never"]["poor"] - rates["never"]["rich"]
            commit = (rates["always"]["rich"] + rates["always"]["poor"] +
                     rates["never"]["rich"] + rates["never"]["poor"])
            size = 30 + commit * 3
            
            ax.scatter(x, y, s=size, color=color,
                      edgecolors='black', linewidth=1.5, alpha=0.8, zorder=3)

            should_show_label = show_labels or (target_labels_to_show is not None and target in target_labels_to_show)
            
            if should_show_label:
                ax.annotate(target, (x, y),
                           xytext=(12, 8), textcoords='offset points',
                           fontsize=16, alpha=0.9, zorder=4, fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                                    edgecolor='black', alpha=0.9, linewidth=1.0))
    
    # Format axes
    ax.set_xlim(-105, 105)
    ax.set_ylim(-105, 105)
    ax.set_xticks([-100, 0, 100])
    ax.set_yticks([-100, 0, 100])
    ax.set_xticklabels([-100, 0, 100], fontsize=18, fontweight='bold')
    ax.set_yticklabels([-100, 0, 100], fontsize=18, fontweight='bold')
    ax.set_xlabel("ALWAYS questions", fontsize=24, fontweight='bold')
    ax.set_ylabel("NEVER questions", fontsize=24, fontweight='bold')
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.8)
    ax.set_axisbelow(True)
    
    
    legend_elements = [
        Patch(facecolor=color, edgecolor='black', label=category)
        for category, color in color_mapping.items()
        if category in data
    ]
    fig.legend(handles=legend_elements, loc='upper center', ncol=len(legend_elements),
              bbox_to_anchor=(0.5, 0.02), frameon=True, fontsize=22, framealpha=0.95)

    fig.suptitle(
        f"{title}\n",
        fontsize=30, fontweight='bold', y=0.95
    )
    
    ax.text(97, 97, "'poor' on\nboth adverbs", fontsize=14, ha='right', va='top',
            style='italic', alpha=0.75, color='darkred')
    ax.text(-97, -97, "'rich' on\nboth adverbs", fontsize=14, ha='left', va='bottom',
            style='italic', alpha=0.75, color='darkblue')
    ax.text(-97, 97, "'rich' on always,\n'poor' on never", fontsize=14, ha='left', va='top',
            style='italic', alpha=0.55, color='dimgray')
    ax.text(97, -97, "'poor' on always,\n'rich' on never", fontsize=14, ha='right', va='bottom',
            style='italic', alpha=0.55, color='dimgray')
    
    plt.tight_layout(rect=(0, 0.04, 1, 0.96))
    
    return fig, ax


def plot_bias_distribution_from_json(json_paths_dict: dict, title: str = "", figsize: tuple = (16, 14), show_labels: bool = True, target_labels_to_show: list = None):
    """
    Plot bias distribution from JSON files

    :param json_paths_dict: Dict 
    :param title: Title for the plot
    :param figsize: Figure size 
    :param show_labels: Whether to show target labels on the plot (default: True)
    :param target_labels_to_show: List of target names to show labels for. Only used when show_labels=False. If None and show_labels=False, no labels are shown. If show_labels=True, all labels are shown.
    :return: tuple (fig, ax)
    """
    plot_data = {}
    
    for category_name, json_path_str in json_paths_dict.items():
        json_path = Path(json_path_str)
        
        if not json_path.exists():
            print(f"Warning: File not found: {json_path}")
            continue
    
        with open(json_path, 'r', encoding='utf-8') as f:
            percentage_data = json.load(f) 
        
        plot_data[category_name] = {}
    
        for target, always_data in percentage_data.get("always", {}).items():
            if target not in plot_data[category_name]:
                plot_data[category_name][target] = {
                    "always": {"rich": 0, "poor": 0},
                    "never": {"rich": 0, "poor": 0}
                }
            plot_data[category_name][target]["always"]["rich"] = always_data.get("rik", 0)
            plot_data[category_name][target]["always"]["poor"] = always_data.get("fattig", 0)
        
        for target, never_data in percentage_data.get("never", {}).items():
            if target not in plot_data[category_name]:
                plot_data[category_name][target] = {
                    "always": {"rich": 0, "poor": 0},
                    "never": {"rich": 0, "poor": 0}
                }
            
            plot_data[category_name][target]["never"]["rich"] = never_data.get("rik", 0)
            plot_data[category_name][target]["never"]["poor"] = never_data.get("fattig", 0)
    
    mode = "intersectionality" if any(
        "and" in k for k in plot_data.keys()
    ) else "base"
    
    return plot_bias_distribution(
        data=plot_data,
        mode=mode,
        title=title,
        figsize=figsize,
        show_labels=show_labels,
        target_labels_to_show=target_labels_to_show
    )