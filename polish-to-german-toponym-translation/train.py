"""
This code was executed on Kaggle platform with 1 × P100 GPU. It fine-tunes the Helsinki-NLP/opus-mt-pl-de model for Toponym translation task (Polish->German)
"""
# !pip install transformers datasets torch

SAVING_DIR = "ENTER YOUR DIRECTORY HERE"

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import Dataset
from torch.utils.data import DataLoader
import torch
from torch.optim import AdamW
import pandas as pd

df = pd.DataFrame(load_dataset("DebasishDhal99/german-polish-paired-placenames", split = "train")) #Link https://huggingface.co/datasets/DebasishDhal99/German_Names_Central_And_Eastern_Europe or https://huggingface.co/datasets/DebasishDhal99/german-polish-paired-placenames

dataset = Dataset.from_pandas(df[['polish', 'german']])

model_name = "Helsinki-NLP/opus-mt-pl-de"  # Polish to German model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def preprocess_function(examples):
    inputs = tokenizer(examples['polish'], padding="max_length", truncation=True, max_length=128)
    outputs = tokenizer(examples['german'], padding="max_length", truncation=True, max_length=128)
    inputs['labels'] = outputs['input_ids']
    return inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

train_dataset = tokenized_dataset.shuffle(seed=42).select([i for i in list(range(int(0.9*len(tokenized_dataset))))])
eval_dataset = tokenized_dataset.shuffle(seed=42).select([i for i in list(range(int(0.9*len(tokenized_dataset)), len(tokenized_dataset)))])

def collate_fn(batch):
    input_ids = torch.tensor([item['input_ids'] for item in batch])
    attention_mask = torch.tensor([item['attention_mask'] for item in batch])
    labels = torch.tensor([item['labels'] for item in batch])
    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True, collate_fn=collate_fn)
eval_dataloader = DataLoader(eval_dataset, batch_size=8, collate_fn=collate_fn)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu") #Simple device setup
model.to(device)

optimizer = AdamW(model.parameters(), lr=5e-5)

# Training 
epochs = 10
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in train_dataloader:
        optimizer.zero_grad()

        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss / len(train_dataloader):.4f}")


model.save_pretrained(f"{SAVING_DIR}/fine_tuned_polish_german_model")
tokenizer.save_pretrained(f"{SAVING_DIR}/fine_tuned_polish_german_model")
