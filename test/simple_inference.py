from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def analyze_text(text, model_name="Qwen/Qwen3-0.6B", prompt_template="Analyze this text and provide insights about its content, tone, and key points: {text}"):
    # Force CPU usage
    device = torch.device("cpu")
    print(f"Using device: {device}")
    
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # Use FP32 for CPU
        device_map="cpu"  # Force CPU device
    )
    
    # Prepare prompt
    prompt = prompt_template.format(text=text)
    messages = [{"role": "user", "content": prompt}]
    
    # Generate response
    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text_input], return_tensors="pt").to(device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512, # control de la longitud de la respuesta
        temperature=0.7, # control de la aleatoriedad de la respuesta
        top_p=0.9 # mas probabilidad de que se elija la respuesta mas probable
    )
    
    # Get the response after the input
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    analysis = tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")
    
    return analysis

if __name__ == "__main__":
    # Example text
    text = "The rapid advancement of artificial intelligence has transformed how we interact with technology. From virtual assistants to autonomous vehicles, AI systems are becoming increasingly sophisticated and integrated into our daily lives."
    
    print("Analyzing text...")
    analysis = analyze_text(text, model_name="google/gemma-3-1b-it")  # cambia aqui el modelo texto y prompt
    # prueba los modelos de qwen y tinyllama, ademas busca en huggingface modelos que puedas usar, tambien puedes cambiar el prompt o el texto
    # "TinyLlama/TinyLlama-1.1B-Chat-v1.0
    # "Qwen/Qwen3-0.6B"
    # "google/gemma-3-1b-it"
    print("\nAnalysis:")
    print(analysis) 