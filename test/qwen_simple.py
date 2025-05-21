from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def analyze_text(text):
    # Force CPU usage
    device = torch.device("cpu")
    print(f"Using device: {device}")
    
    # Load model and tokenizer
    model_name = "Qwen/Qwen3-0.6B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # Use FP32 for CPU
        device_map="cpu"  # Force CPU device
    )
    
    # Prepare prompt
    prompt = f"Analyze this text and provide insights about its content, tone, and key points: {text}"
    messages = [{"role": "user", "content": prompt}]
    
    # Generate response
    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    model_inputs = tokenizer([text_input], return_tensors="pt").to(device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    
    # Parse thinking content
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0
    
    thinking = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    
    return thinking, content

if __name__ == "__main__":
    # Example text
    text = "The rapid advancement of artificial intelligence has transformed how we interact with technology. From virtual assistants to autonomous vehicles, AI systems are becoming increasingly sophisticated and integrated into our daily lives."
    
    print("Analyzing text...")
    thinking, analysis = analyze_text(text)
    
    print("\nModel's Thinking Process:")
    print(thinking)
    print("\nFinal Analysis:")
    print(analysis) 