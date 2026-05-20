import json
from pathlib import Path

MODELS = ["nb_alpaca", "normistral", "norwai"]
BASE_SIZES = {
    "Innvandring": 100,
    "Fylke": 110,
    "Oslo øst/vest": 20
}
INTER_SIZES = {
    "Interseksjonalitet (oslo og innvandring)": 200,
    "Interseksjonalitet (Fylke og innvandring)": 1100
}

RESULTS_DIR = Path(__file__).parent.parent
OUTPUT_DIR = Path(__file__).parent


def process_model(model):
    """Create subsets for a single model."""
    model_dir = OUTPUT_DIR / model
    model_dir.mkdir(exist_ok=True)
    
    # Base subset
    base_file = RESULTS_DIR / model / "base_results_full.json"
    if base_file.exists():
        with open(base_file) as f:
            base_data = json.load(f)
        base_subset = {cat: base_data[cat][:size] for cat, size in BASE_SIZES.items() if cat in base_data}
        with open(model_dir / "base_subset.json", "w") as f:
            json.dump(base_subset, f, ensure_ascii=False, indent=2)
        print(f"  ✓ base_subset.json")
    
    # Intersectionality subset
    inter_file = RESULTS_DIR / model / "inter_results_full.json"
    if inter_file.exists():
        with open(inter_file) as f:
            inter_data = json.load(f)
        inter_subset = {cat: inter_data[cat][:size] for cat, size in INTER_SIZES.items() if cat in inter_data}
        with open(model_dir / "inter_subset.json", "w") as f:
            json.dump(inter_subset, f, ensure_ascii=False, indent=2)
        print(f"  ✓ inter_subset.json")


for model in MODELS:
    process_model(model)
