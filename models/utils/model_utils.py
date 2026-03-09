import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

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
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        token=access_token, 
        dtype=torch.float16
        )

    return tokenizer, model



@torch.inference_mode()
def generate_model_responses(model: AutoModelForCausalLM, tokenizer: AutoTokenizer, prompts: list, device: torch.device, 
                            max_new_tokens: int = 100, do_sample: bool = False, model_name: str = "") -> list[str]:
    '''
    Generate text from a LLM using greedy decoding.
    The function tokenizes the prompt and runs model.generate. 
    
    :param model: Loaded causal language model.
    :param tokenizer: Tokenizer corresponding to the model.
    :param prompt: Input prompt string.
    :param device: Torch device.
    :param max_new_tokens: Number of new tokens to generate.
    :param do_sample: Bool for specific output, keep as False for deterministic output.

    :return: Generated text string.
    '''
    if model_name == "normistral":
        messages_batch = [[{"role": "user", "content": p}] for p in prompts]

        enc = tokenizer.apply_chat_template(
            messages_batch,
            add_generation_prompt=True,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        if isinstance(enc, torch.Tensor):
            input_ids = enc.to(device)
            attention_mask = None
        else:
            input_ids = enc["input_ids"].to(device)
            attention_mask = enc.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(device)

    else:
        enc = tokenizer(
            prompts, 
            return_tensors="pt", 
            padding=True, 
            truncation=True
        )
        input_ids = enc["input_ids"].to(device)
        attention_mask = enc.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(device)

    output_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        pad_token_id=tokenizer.eos_token_id,
    )


    if attention_mask is not None:
        prompt_lengths = attention_mask.sum(dim=1)
    else:
        prompt_lengths = torch.full((input_ids.size(0),), input_ids.size(1), device=input_ids.device)

    gen_text = []
    for i in range(output_ids.size(0)):
        new_tokens = output_ids[i, prompt_lengths[i]:]
        gen_text.append(tokenizer.decode(new_tokens, skip_special_tokens=True).strip())

    return gen_text


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
        base_dir = f"results/{model_name}/"
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