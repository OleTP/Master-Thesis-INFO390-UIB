import matplotlib.pyplot as plt
import pandas as pd
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


def print_prediction_by_target(results: dict, category: str, title: str = ""):
    """
    Print prediction distribution by target for a specific category.
    Shows all targets in the category as rows, predicted labels as columns (rik, fattig, uviten).
    Each cell shows the percentage of predictions for that target.
    
    :param results: Dict with results organized by category
    :param category: Which category to analyze (e.g., "Innvandring", "Fylke", "Oslo øst/vest")
    :param title: Optional title header
    """
    category_results = results.get(category, [])
    
    if not category_results:
        print(f"No results found for category: {category}")
        return

    df = pd.DataFrame(category_results)
    
    targets = sorted(df['target'].unique())
    labels = ("rik", "fattig", "uviten")
    
    pivot_data = []
    for target in targets:
        target_data = df[df['target'] == target]
        row = {'Target': target}
        
        for label in labels:
            count = len(target_data[target_data['pred_label'] == label])
            total = len(target_data)
            percentage = (count / total * 100) if total > 0 else 0
            row[label] = f"{percentage:.1f}%"
        
        pivot_data.append(row)
    
    # Print results
    if title:
        print("\n" + "=" * 80)
        print(title)
    
    result_df = pd.DataFrame(pivot_data)
    print(result_df.to_string(index=False))
    print()


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