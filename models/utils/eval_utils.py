import time
import pandas as pd
from tqdm import tqdm
from utils.regex_utils.label_utils import predict_label_from_text, parse_choices
from utils.regex_utils.regex_variables_utils import VALID_LABELS

def print_example_response(df: pd.DataFrame, indices: list, generator_func, prompt_func):
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
        generation_output = generator_func([prompt])[0]

        text = (generation_output or "").strip()
        model_answer = predict_label_from_text(text)

        print("\n--- PROMPT ---")
        print(prompt.strip())
        print(f"\nModel Says       : {text}")

        print("\n--- Prediction vs True label---")
        print(f"Model prediction  : {model_answer}")
        print(f"True label       : {true_label}")
        print("-" * 100)

def question_classifier(df: pd.DataFrame, model_name: str, generator_func, prompt_func, num_of_examples: int | None = None, 
                        category: str | None = None, batch_size: int = 8) -> list[dict]:
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

    for start in tqdm(range(0, n, batch_size), desc=f"{model_name} | Category: {category} | {n} questions"):
        end = min(start + batch_size, n)
        batch_df = df.iloc[start:end]

        prompts = [prompt_func(row["question"], row["change"]) for _, row in batch_df.iterrows()]
        gen_text = generator_func(prompts)

        for (idx, row), text in zip(batch_df.iterrows(), gen_text):
            text = (text or "").strip()
            pred_label = predict_label_from_text(text)
            true_label = str(row["label"]).strip().lower()

            choices_set = parse_choices(row.get("choices", None))
            if not choices_set:
                choices_set = set(VALID_LABELS)

            is_valid = pred_label in choices_set
            if not is_valid:
                invalid_answers += 1

            results.append({
                "row_index": int(idx),
                "true_label": true_label,
                "pred_label": pred_label,
                "generated_text": text,
                "is_valid": is_valid,
                "change": str(row.get("change", "")).strip().lower(),
                "category": str(row.get("category", "")).strip(),
            })
    print("\n" + "-" * 100)
    print(f"Antall besvarte spørsmål: {n}")
    print(f"Antall spørsmål uten gyldig svar: {invalid_answers}")
    print("-" * 100)

    return results

def benchmark_batch_size(df, model_prompt, generator_batch, test_size=100):
    '''
    Benchmark different batch sizes to find optimal throughput for model generation.
    Tests batch sizes from 1 to 256 and returns the size with highest throughput.
    
    :param df: DataFrame containing question and change data
    :param model_prompt: Function to format question and change into model prompt
    :param generator_batch: Function to run model generation on a batch of prompts
    :param test_size: Number of prompts to use for benchmarking (default 100)
    
    :return: Optimal batch size with highest throughput (prompts/sec)
    '''
    test_prompts = [model_prompt(row["question"], row["change"]) for _, row in df.iloc[:test_size].iterrows()]
    best_batch_size, best_throughput = 1, 0
    
    print(f"Running batch size benchmark test...\nTotal prompts: {len(test_prompts)}\n")
    
    for batch_size in [1, 2, 4, 8, 16, 32, 64, 128]:
        generator_batch(test_prompts[:batch_size])
        
        start_time = time.time()
        for idx in range(0, len(test_prompts), batch_size):
            generator_batch(test_prompts[idx:idx+batch_size])
        
        total_seconds = time.time() - start_time
        minutes, seconds = int(total_seconds // 60), int(total_seconds % 60)
        throughput = len(test_prompts) / total_seconds
        
        print(f"Testing batch_size={batch_size}... Done! ({minutes:02d}:{seconds:02d} total, {throughput:.1f} prompts/sec)")
        
        if throughput > best_throughput:
            best_throughput = throughput
            best_batch_size = batch_size
    
    print(f"\nOPTIMAL batch_size: {best_batch_size}")
    return best_batch_size


##########################################
#            HELPER FUNCTIONS            #
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