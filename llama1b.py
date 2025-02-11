import torch
from transformers import pipeline

# Role message común para ambos modelos
role_message = (
    "You are a digital clone of Albert Einstein, answering questions exactly as he would. "
    "When a question is asked, provide an accurate, detailed, and direct answer based solely on the prompt. "
    "Do not simulate a conversation or add extraneous commentary."
)

model_id_1b = "meta-llama/Llama-3.2-1B-Instruct"

pipe_1b = pipeline(
    "text-generation",
    model=model_id_1b,
    torch_dtype=torch.bfloat16,
    device_map="cuda",
)

def ask_Llama1B(user_message: str) -> str:
    """
    Genera una respuesta usando el modelo Llama 1B según el prompt.
    Se permite una respuesta extensa si es necesario.
    """
    prompt = f"{role_message}\nUser: {user_message}\nAlbert:"
    outputs = pipe_1b(
        prompt,
        max_new_tokens=512,  # Permite respuestas largas si es necesario
        do_sample=False,
        temperature=0.3,
        num_return_sequences=1,
        pad_token_id=pipe_1b.tokenizer.eos_token_id
    )
    response = outputs[0]["generated_text"].split("Albert:")[-1].strip()
    return response