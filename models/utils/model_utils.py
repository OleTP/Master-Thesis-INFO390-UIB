from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_model(model_name: str, 
               access_token: str
               ):
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
def generate_model_response(model: AutoModelForCausalLM, 
                            tokenizer: AutoTokenizer, 
                            prompt: str, 
                            device: torch.device, 
                            max_new_tokens: int = 5, 
                            do_sample: bool = False,
                            model_name: str = ""
                            ) -> str:
    '''
    Generate text from a LLM using greedy decoding.
    The function tokenizes the prompt and runs model.generate. 
    
    :param model: Loaded causal language model.
    :param tokenizer: Tokenizer corresponding to the model.
    :param prompt: Input prompt string.
    :param device: Torch device (CPU or CUDA).
    :param max_new_tokens: Number of new tokens to generate.
    :param do_sample: Bool for specific output, keep as False for deterministic output.

    :return: Generated text string.
    '''
    if model_name == "normistral":
        messages = [{"role": "user", "content": prompt}]

        enc = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt",
        )

        # enc kan være Tensor eller BatchEncoding -> gjør det til input_ids Tensor
        if isinstance(enc, torch.Tensor):
            input_ids = enc.to(device)
            attention_mask = None
        else:
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

        prompt_length = input_ids.shape[-1]

    else:
        enc = tokenizer(prompt, return_tensors="pt")
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

        prompt_length = input_ids.shape[-1]

    new_tokens = output_ids[0, prompt_length:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
    
