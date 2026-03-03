import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

def print_classification_report(results: list[dict], labels: tuple = ("rik", "fattig", "uviten"), title: str = ""):
    """
    Print sklearn classification_report for a list of result dicts.

    :param results: List[dict] with a result from a classification. Must contain [true_label, pred_label]
    :param labels: Labels in the classification report(fixed label order)
    :param title: Optional title header
    """
    y_true = [r["true_label"] for r in results]
    y_pred = [r["pred_label"] for r in results]

    if title:
        print("\n" + "=" * 80)
        print(title)

    print(f"Antall spørsmål: {len(results)}")
    print(classification_report(y_true, y_pred, labels=list(labels), digits=2, zero_division=0))


def print_confusion_matrix(results: list[dict], labels: tuple = ("rik", "fattig", "uviten"), title: str = ""):
    """
    Plots a single confusion matrix for a list of result dicts.

    :param results: List[dict] with a result from a classification. Must contain [true_label, pred_label]
    :param labels: Labels in the confusion matrix (fixed label order)
    :param title: Optional plot title
    """
    y_true = [r["true_label"] for r in results]
    y_pred = [r["pred_label"] for r in results]

    cm = confusion_matrix(y_true, y_pred, labels=list(labels), normalize=None)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(labels))

    fig, ax = plt.subplots(figsize=(7, 5))
    disp.plot(
        ax=ax,
        values_format=".2f",
        xticks_rotation=45,
        colorbar=False
    )
    ax.set_title(title or "Confusion Matrix")
    plt.tight_layout()
    plt.show()

def filter_results(results: list[dict], category: str | None = None, change: str | None = None) -> list[dict]:
    """
    Filter results by category and/or change. 
    This is used to look at differences in specific categorys and adverbs.
    """
    out = results
    if category is not None:
        out = [r for r in out if r.get("category") == category]
    if change is not None:
        c = str(change).strip().lower()
        out = [r for r in out if r.get("change") == c]
    return out

