import json
import pandas as pd


def load_json(template_name):
    # Define json file path
    ses_file_path = f'Master-Thesis-INFO390-UIB/ses_dataset_templates/{template_name}/ses_template.json'
    target_file_path = f'Master-Thesis-INFO390-UIB/ses_dataset_templates/{template_name}/target_template.json'

    # Load data from a JSON files
    with open(ses_file_path, 'r', encoding="utf-8") as file:
        templates = json.load(file)

    with open(target_file_path, 'r', encoding="utf-8") as file:
        targets = json.load(file)

    return templates, targets


def generate_dataset(template_names, output_file):
    
    questions = []

    # Make the questions
    for template_name in template_names:
        templates, targets = load_json(template_name)

        for template in templates:
            for target in targets:
                q = template.copy()
                q["question"] = q["question"].replace("{{TARGET}}", target["target"])
                q["target"] = target["target"]
                q["ssb_group"] = target.get("ssb_group", None)
                q["label"] = target["label"]
                q["template_source"] = template_name
                questions.append(q)
            
    # Convert to DataFrame
    df = pd.DataFrame(questions)
    # Save to CSV
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Dataset saved to {output_file}")


generate_dataset(['immigration_templates', 'regional_templates'], 'dataset/first_dataset_test.csv')