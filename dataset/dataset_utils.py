import json
import pandas as pd

CATEGORY_BASE_ID = {
    "Innvandring": 10000,
    "Fylke": 20000,
    "Oslo øst/vest": 30000,
    "Interseksjonalitet (oslo og innvandring)": 40000,
    "Interseksjonalitet (Fylke og innvandring)": 50000,
}

def generate_template_id(index: int, category: str):
    """
    Generates a unique template ID based on the category and index.
    
    :params index: The index number.
    :params category: The category name.
    
    :return: A unique template ID.
    """
    base_id = CATEGORY_BASE_ID.get(category)
    if base_id is None:
        raise ValueError(f"Ukjent kategori: {category}")
    return base_id + index + 1


def load_targets(template_name: str):
    """
    Loads targets from JSON files based on the template name.
    
    :params template_name: The name of the template.
    
    :return: list with the targets
    """
    target_file_path = f'ses_dataset_templates/{template_name}/target_template.json'

    with open(target_file_path, 'r', encoding="utf-8") as file:
        targets = json.load(file)
    
    return targets


def combine_target_text_target_column(target_1, target_2):
    """
    Combines two target names with ' og ' separator for the target column.
    
    :params target_1: First target name
    :params target_2: Second target name
    
    :return: Combined target string
    """
    return f'{target_1} og {target_2}'


def attach_questions_to_df(df: pd.DataFrame, questions_file_path: str):
    """
    This function attaches questions from a JSON file to a DataFrame based on an 'index' column.
    Exception is raised if any questions are missing or the DataFrame does not contain the 'index' column.
    
    :params df: DataFrame containing an 'index' column.
    :params questions_file_path: Path to the JSON file containing questions.
    
    :return: Modified DataFrame with an added 'question' column.
    """
    if "index" not in df.columns:
        raise ValueError("DataFrame mangler kolonnen 'index'")

    with open(questions_file_path, 'r', encoding="utf-8") as file:
        questions = json.load(file)

    question_map = dict()
    for index_key in questions:
        question_map[int(index_key)] = questions[index_key]
    
    df['question'] = df['index'].map(question_map)

    if df["question"].isna().any():
        missing = df[df["question"].isna()]["index"].tolist()
        raise ValueError(f"Mangler spørsmål for index: {missing}")
    
    return df


def get_target_text(target_name, category):
    """
    Generates the appropriate target text based on the category.
    
    :params target_name: The name of the target
    :params category: The category name ("Innvandring", "Fylke", "Oslo øst/vest")
    
    :return: Formatted target text for use in questions
    """
    if category == "Innvandring":
        return f"som opprinnelig er fra {target_name}"
    elif category == "Oslo øst/vest":
        return f"som bor på {target_name}"
    else: 
        return f"som bor i {target_name} fylke"


def get_target_texts_intersectionality(target_1_name, target_2_name, category_1):
    """
    Generates appropriate target text for intersectionality (region/oslo + immigration).
    Immigration is always target_2 and comes at the end.
    
    :params target_1_name: Name of region/oslo target
    :params target_2_name: Name of immigration target
    :params category_1: Category of target_1 ("Oslo øst/vest" or "Fylke")
    
    :return: Tuple of (text1, text2) where text2 includes "og" connector
    """
    if category_1 == "Oslo øst/vest":
        return f"som bor på {target_1_name}", f"og opprinnelig er fra {target_2_name}"
    else:
        return f"som bor i {target_1_name} fylke", f"og opprinnelig er fra {target_2_name}"