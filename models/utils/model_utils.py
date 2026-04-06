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
                            max_new_tokens: int = 130, do_sample: bool = False, model_name: str = "") -> list[str]:
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
