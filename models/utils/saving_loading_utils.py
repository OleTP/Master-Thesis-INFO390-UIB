import json
import os
import pandas as pd
from pathlib import Path


def results_path(filename: str, colab: bool, model_name: str) -> str:
    """
    Makes correct path dependent on code is ran on colab or not.

    :param filename: What the file is called.
    :param colab: True if code is ran on Colab.
    :param model_name: Name of the model used.

    :return: Correct saving path.  
    """
    if colab:
        base_dir = f"/content/drive/Othercomputers/Min MacBook Pro/Master-Thesis-INFO390-UIB/models/results/{model_name}/"
    else:
        base_dir = f"../results/{model_name}/"
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)


def save_results(results: dict, filepath: str, drop_generated_text: bool = True):
    """
    Saves results, with option to save without generated text to keep it smaller.

    :param results: Results with prredictions from the models
    :param filepath: Path to were to result file will be saved.
    :param drop_generated_text: Drops generated text from the results.
    """
    if drop_generated_text:
        results_to_save = {
            cat: [{k: v for k, v in r.items() if k != "generated_text"} for r in rows]
            for cat, rows in results.items()
        }
    else:
        results_to_save = results

    with open(filepath, "w") as f:
        json.dump(results_to_save, f, indent=2)


def load_results(filepath: str) -> dict:
    """
    Loads results from a folder.

    :param filepath: Path to saved Dict()
    """
    with open(filepath, "r") as f:
        return json.load(f)


def generate_prediction_percentages_by_target(results: dict, category: str, title: str = "", model_name: str = None, save_results: bool = True):
    """
    Generate prediction percentage distributions by target for a specific category, separated by change type.
    Saves percentage data to JSON files with both always and never data.
    
    :param results: Dict with results organized by category
    :param category: Which category to analyze (e.g., "Innvandring", "Fylke", "Oslo øst/vest")
    :param title: Optional title header (model name recommended)
    :param model_name: Optional model name for saving. If None, tries to extract from title
    :param save_results: Whether to save results to JSON file (default: True)
    """
    category_results = results.get(category, [])
    
    if not category_results:
        print(f"No results found for category: {category}")
        return

    df = pd.DataFrame(category_results)
    
    targets = sorted(df['target'].unique())
    labels = ("rik", "fattig", "uviten")
    changes = ["alltid", "aldri"]
    
    if model_name is None and title:
        model_name = title.split(" ")[0].lower()
    
    if title:
        print("\n" + "=" * 80)
    
    category_mapping = {
        "Innvandring": "immigration",
        "Fylke": "region",
        "Oslo øst/vest": "oslo",
        "Interseksjonalitet (oslo og innvandring)": "oslo_and_immigration",
        "Interseksjonalitet (Fylke og innvandring)": "region_and_immigration"
    }
    category_filename = category_mapping.get(category, category.lower().replace(" ", "_"))
    
    json_data = {"always": {}, "never": {}}
    
    for change in changes:
        change_data = df[df['change'] == change]
        if change_data.empty:
            continue
    
        pivot_data_display = []
        change_name = "always" if change == "alltid" else "never"
        
        for target in targets:
            target_data = change_data[change_data['target'] == target]
            if target_data.empty:
                continue
                
            row = {'Target': target}
            target_percentages = {}
            
            for label in labels:
                count = len(target_data[target_data['pred_label'] == label])
                total = len(target_data)
                percentage = (count / total * 100) if total > 0 else 0
                row[label] = f"{percentage:.1f}%"
                target_percentages[label] = round(percentage, 1)
            
            pivot_data_display.append(row)
            json_data[change_name][target] = target_percentages

        if title:
            change_word = "Always" if change == "alltid" else "Never"
            print(f"{title} - Prediction Distribution by Target ({category}) for {change_word} questions.")
        
        result_df = pd.DataFrame(pivot_data_display)
        print(result_df.to_string(index=False))
        print()
    
    # Save combined data to single JSON file
    if save_results and model_name:
        folder_path = Path("../results/plot_results") / model_name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        json_path = folder_path / f"{category_filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved to: {json_path}")


def run_results_pipeline(models: list, model_titles: dict, intersectionality: bool = False):
    """
    Load results, generate JSON files, and prepare for plotting.
    
    :param models: List of model names to process.
    :param model_titles: Dictionary mapping model names to display titles.
    :param intersectionality: If True, run intersectionality pipeline. If False, run base pipeline.
    :return: Dictionary of results
    """

    if intersectionality:
        categories = ["Interseksjonalitet (oslo og innvandring)", "Interseksjonalitet (Fylke og innvandring)"]
        results_filename = "inter_results.json"
        pipeline_type = "INTERSECTIONALITY"
        title_suffix = "Intersectionality"
    else:
        categories = ["Innvandring", "Fylke", "Oslo øst/vest"]
        results_filename = "base_results.json"
        pipeline_type = "BASE"
        title_suffix = "Base Results"
    
    results_all = {}
    
    for model in models:
        path = results_path(results_filename, model_name=model, colab=False)
        results_all[model] = load_results(path)
        print(f"Loaded {pipeline_type.lower()} results for {model}")
    
    # Generate JSON files using generate_prediction_percentages_by_target
    for model in models:
        for category in categories:
            print(f"\n{model_titles[model]} - {category}")
            generate_prediction_percentages_by_target(
                results_all[model],
                category=category,
                title=f"{model_titles[model]} - {title_suffix}",
                model_name=model,
                save_results=True
            )
    
    return results_all