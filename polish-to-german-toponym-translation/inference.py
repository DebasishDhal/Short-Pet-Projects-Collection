from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_path = "DebasishDhal99/polish-to-german-toponym-model-opus-mt-pl-de"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path) 

polish_name = "Stare miasteczko"

inputs = tokenizer(polish_name, return_tensors="pt", padding=True, truncation=True)
inputs = {k: v.to(device) for k, v in inputs.items()}

with torch.no_grad():
    outputs = model.generate(**inputs, max_length=50)
  
german_name = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(german_name)
