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

@torch.inference_mode()
def generate_model_response(model, tokenizer, prompt: str, device: torch.device, max_new_tokens: int = 1, do_sample: bool = False):
    """
    Generate text from a LLM using greedy decoding.

    The function tokenizes the prompt and runs model.generate. 
    
    :param model: Loaded causal language model.
    :param tokenizer: Tokenizer corresponding to the model.
    :param prompt: Input prompt string.
    :param device: Torch device (CPU or CUDA).
    :param max_new_tokens: Number of new tokens to generate.
    :param do_sample: Bool for specific output, keep as False for deterministic output.

    :return: Generated text string.
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs.get("attention_mask"),
        max_new_tokens=max_new_tokens,
        do_sample=do_sample,
        pad_token_id=tokenizer.eos_token_id,
    )

    prompt_length = inputs["input_ids"].shape[-1]
    new_tokens = output_ids[0, prompt_length:]

    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    


def print_example_response(df, indices, generator_func, prompt_func):
    '''
    Generate and print prediction for some examples.

    :param df: DataFrame with question, choices, label.
    :param indices: The specific index/indices that i want to check.
    :param generator: Generator function.
    :param prompt_func: Prompt function.

    '''
    for i in indices:
        question = df["question"].iloc[i]
        true_label = df["label"].iloc[i]

        prompt = prompt_func(question)
        generation_output = generator_func(prompt)

        text = generation_output.strip()
        tokens = text.split()
        model_answer = tokens[-1].lower() if tokens else "ingen_svar"

        print("\n--- PROMPT ---")
        print(prompt.strip())

        print(f"Model Says       : {text}")

        print("\n--- Prediction vs True label---")
        print(f"Model prediction  : {model_answer}")
        print(f"True label       : {true_label}")
        print("-" * 100)