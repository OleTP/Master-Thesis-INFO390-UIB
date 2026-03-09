import json
import os

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