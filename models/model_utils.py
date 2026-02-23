from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


def load_model(model_name: str, access_token: str):
    '''
    Loads base model and tokenizer
    
    :param model_name: The specific model
    :param access_token: Access token from HuggingFace

    :return: The model and tokenizer
    '''
    tokenizer = AutoTokenizer.from_pretrained(
        model_name, 
        token=access_token
        )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        token=access_token, 
        dtype=torch.float16
        )

    return tokenizer, model


def create_model_generators(models: dict, access_token: str):
    '''
    Create a HuggingFace text-generation pipeline for each model.
    
    :param model_name: A dictonary containing all the models
    :param access_token: Access token from HuggingFace

    :return: Dictionary of text-generation pipeline
    '''
    generator_dict = dict()

    for name, model_dict in models.items():
        generator_dict[name] = pipeline(
            "text-generation",
            model=model_dict['model'],
            tokenizer=model_dict['tokenizer'],
            token=access_token
        )

    return generator_dict


def print_response(generation_output, true_label = None):
    '''
    Print model output and extracted prediction.

    :param generation_output: Raw generated text from the model.
    :param true_label: Optional ground truth label for comparison
    '''
    text = generation_output.strip()
    tokens = text.split()
    model_answer = tokens[-1].lower() if tokens else "<ingen_svar>"  

    if true_label:
        print(f"True label       : {true_label}")
    print(f"Model Says       : {generation_output.strip()}")
    print(f"Predicted Genre  : {model_answer}")
    print("-" * 100)
