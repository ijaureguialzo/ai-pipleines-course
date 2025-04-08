#!/usr/bin/env python3
"""
Test script to verify Hugging Face SDK installation is working correctly.
Run this script to check if the necessary components are installed and accessible.
"""

import sys

def check_huggingface_installation():
    """Check if required Hugging Face packages are installed."""
    
    print("Checking Hugging Face SDK installation...")
    
    # Check PyTorch first as it's required for transformers
    try:
        import torch
        print(f"✅ PyTorch is installed (version: {torch.__version__})")
    except ImportError:
        print("❌ PyTorch is not installed. Install it with: pip install torch")
        print("   For specific instructions based on your system: https://pytorch.org/get-started/locally/")
        return False
    
    try:
        import transformers
        print(f"✅ transformers package is installed (version: {transformers.__version__})")
    except ImportError:
        print("❌ transformers package is not installed. Install it with: pip install transformers")
        return False
    
    try:
        import datasets
        print(f"✅ datasets package is installed (version: {datasets.__version__})")
    except ImportError:
        print("❌ datasets package is not installed. Install it with: pip install datasets")
        return False
    
    try:
        import accelerate
        print(f"✅ accelerate package is installed (version: {accelerate.__version__})")
    except ImportError:
        print("❌ accelerate package is not installed. Install it with: pip install accelerate")
        print("   This is needed for many Hugging Face operations, especially with larger models")
        return False
    
    try:
        from huggingface_hub import HfApi
        print(f"✅ huggingface_hub package is installed")
        api = HfApi()
        # Test if we can connect to the API
        models = api.list_models(limit=1)
        print("✅ Successfully connected to Hugging Face Hub API")
    except ImportError:
        print("❌ huggingface_hub package is not installed. Install it with: pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"❌ Failed to connect to Hugging Face Hub: {str(e)}")
        return False
        
    # Try loading a simple model as a final test
    try:
        print("Testing model loading (this may take a moment)...")
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # Choose a tiny model for testing
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        
        # Load tokenizer and model separately to identify issues more precisely
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("✅ Successfully loaded tokenizer")
        
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("✅ Successfully loaded model")
        
        # Test simple inference
        test_text = "This is a test to check if Hugging Face works!"
        inputs = tokenizer(test_text, return_tensors="pt")
        with torch.no_grad():
            output = model(**inputs)
        
        print("✅ Successfully ran inference")
        print(f"   Test completed with model: {model_name}")
    except Exception as e:
        print(f"❌ Failed to load model or run inference: {str(e)}")
        print("   This might indicate issues with backend dependencies.")
        return False
    
    print("\nHugging Face SDK is properly installed and working!")
    print("If you encounter any issues, ensure all packages are installed correctly:")
    print("   pip install -r requirements.txt")
    return True

if __name__ == "__main__":
    success = check_huggingface_installation()
    sys.exit(0 if success else 1) 