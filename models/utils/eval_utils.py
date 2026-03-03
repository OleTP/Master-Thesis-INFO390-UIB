import pandas as pd
from tqdm import tqdm
from regex_utils.label_utils import predict_label_from_text, parse_choices
from regex_utils.regex_variables_utils import VALID_LABELS

def print_example_response(df: pd.DataFrame, 
                           indices: list, 
                           generator_func, #Function
                           prompt_func #Function
                           ):
    """
    Prints an response from the model. This function is used to analyse the model output.

    :param df: Pandas DataFrame to be used, must contain ['question', 'change', 'label'] columns
    :param indices: List of specific indices that should be printed out.
    :param generator_func: Function for model generation.
    :param prompt_func: Function for the specific prompt to the model.
    """
    for i in indices:
        question = df["question"].iloc[i]
        change = df["change"].iloc[i]

        true_label = str(df["label"].iloc[i]).strip().lower()

        prompt = prompt_func(question, change)
        generation_output = generator_func(prompt)

        text = (generation_output or "").strip()
        model_answer = predict_label_from_text(text)

        print("\n--- PROMPT ---")
        print(prompt.strip())
        print(f"\nModel Says       : {text}")

        print("\n--- Prediction vs True label---")
        print(f"Model prediction  : {model_answer}")
        print(f"True label       : {true_label}")
        print("-" * 100)


def question_classifier(df: pd.DataFrame, 
                        model: str, 
                        generator_func, #Function
                        prompt_func, #Function
                        num_of_examples: int | None = None, 
                        category: str | None = None
                        ) -> list[dict]:
    """
    Run model classification evaluation over a dataset

    :param df: Pandas DataFrame to be used, must contain ['question', 'change', 'label'] columns.
    :param model: Name of the model to be used. 
    :param generator_func: Function for model generation.
    :param prompt_func: Function for the specific prompt to the model.
    :param num_of_examples: Number of examples if you want to limit the classification. None will classify all instances in df.
    :param category: Category filtration to see which part of the dataset is being classified. 

    :return: List of results from the classification with all results being Dicts.
    """

    df = filter_by_category(df, category)
    n = number_of_examples(df, num_of_examples)

    results = []
    invalid_answers = 0

    for i in tqdm(range(n), desc=f"{model} | Category: {category} | {n} questions: "):
        row = df.iloc[i]

        prompt = prompt_func(row["question"])
        gen_text = generator_func(prompt)

        text = (gen_text or "").strip()
        pred_label = predict_label_from_text(text)
        true_label = str(row["label"]).strip().lower()

        choices_set = parse_choices(row.get("choices", None))
        if not choices_set:
            choices_set = set(VALID_LABELS)

        is_valid = pred_label in choices_set
        if not is_valid:
            invalid_answers += 1

        results.append({
            "row_index": int(df.index[i]),
            "true_label": true_label,
            "pred_label": pred_label,
            "generated_text": text,
            "is_valid": is_valid,
            "change": str(row.get("change", "")).strip().lower(),
            "category": str(row.get("category", "")).strip()
        })

    print("\n" + "-" * 100)
    print(f"Antall besvarte spørsmål: {n}")
    print(f"Antall spørsmål uten gyldig svar: {invalid_answers}")
    print("-" * 100)

    return results




##########################################
# HELPER FUNCTIONS question_classifier() #
##########################################
def number_of_examples(df: pd.DataFrame, num_of_examples: int | None = None) -> int:
    """
    Resolves how many examples to run.
    """
    if num_of_examples is None:
        return len(df)
    return min(int(num_of_examples), len(df))

def filter_by_category(df: pd.DataFrame, category: str | None = None) -> pd.DataFrame:
    """
    Filter DataFrame by category. With special handeling for intersectionality.
    """
    if category is None:
        return df
    
    if isinstance(category, str) and category.lower() == "interseksjonalitet":
        return df[df["category"].str.startswith("Interseksjonalitet")]
    
    if isinstance(category, (list, tuple, set)):
        return df[df["category"].isin(category)]
    
    return df[df["category"] == category]