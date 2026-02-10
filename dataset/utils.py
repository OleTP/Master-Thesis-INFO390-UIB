import json
from pandas import DataFrame

def attach_questions_to_df(df: DataFrame, questions_file_path: str):
    """
    This function attaches questions from a JSON file to a DataFrame based on an 'index' column.
    Exception is raised if any questions are missing or the DataFrame does not contain the 'index' column.
    Args:
        df (pd.DataFrame): DataFrame containing an 'index' column.
        questions_file_path (str): Path to the JSON file containing questions.
    Returns:
        DataFrame: modified DataFrame with an added 'question' column.
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


CATEGORY_BASE_ID = {
    "Innvandring": 10000,
    "Fylke": 20000,
    "Oslo øst/vest": 30000,
    "Interseksjonalitet (oslo og innvandring)": 40000,
    "Interseksjonalitet (oslo og fylke)": 50000,
    "Interseksjonalitet (Fylke og innvandring)": 60000,
}

def generate_template_id(index: int, category: str):
    """
    Generates a unique template ID based on the category and index.
    Args:
        index (int): The index number.
        category (str): The category name.
    Returns:
        int: A unique template ID. 100s for "Innvandring", 200s for "Region", 300s for "Oslo øst/vest".
    """
    base_id = CATEGORY_BASE_ID.get(category)
    if base_id is None:
        raise ValueError(f"Ukjent kategori: {category}")
    return base_id + index + 1



def load_targets(template_name: str):
    """
    Loads targets from JSON files based on the template name.
    Args:
        template_name (str): The name of the template.
    Returns:
        list[dict]: targets
    """
    target_file_path = f'ses_dataset_templates/{template_name}/target_template.json'

    with open(target_file_path, 'r', encoding="utf-8") as file:
        targets = json.load(file)
    
    return targets

def combine_target_text_question_column(target_1, target_2):
    return f'både {target_1} og {target_2}'

def combine_target_text_target_column(target_1, target_2):
    return f'{target_1} og {target_2}'