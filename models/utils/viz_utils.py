import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

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

    cm = confusion_matrix(y_true, y_pred, labels=list(labels), normalize=None)
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
        values_format="d",    
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