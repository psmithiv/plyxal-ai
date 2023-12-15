# Import the necessary libraries
from datasets import load_dataset
from transformers import T5Tokenizer, DataCollatorForSeq2Seq, T5ForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer
import pprint
from src.utils.object_print import op

# Load T5 model and tokenizer
model_name = "google/flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir="./.cache/tokenizers", legacy=False)
model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir="./.models")

# Configure PrettyPrint
pp = pprint.PrettyPrinter(indent=4)

# Load and tokenize the OpenOrca dataset (remove [:10] for full run)
dataset = load_dataset("Open-Orca/OpenOrca", split="train[:10]", cache_dir="./.cache/datasets")
dataset = dataset.train_test_split(test_size=0.2)  # 0.2)
data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

# Define our preprocessing function
def preprocess_function(examples):
    # Combine system_prompt and question:
    inputs = []
    for i in range(len(examples["system_prompt"])):
        inputs.append(examples["system_prompt"][i] + "\n" + examples["question"][i])

    # Tokenize the inputs
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)

    # The "labels" are the tokenized outputs:
    labels = tokenizer(text_target=examples["response"], max_length=512, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Map the preprocessing function across our dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Set up training arguments
# NOTE: These parameters here are optimized to maximize batch size and training speed on a GPU with 16GB VRAM
training_args = Seq2SeqTrainingArguments(
    output_dir="./checkpoints/flan-orca-t5-base",
    learning_rate=3e-4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=4,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=2,
    predict_with_generate=True,
    use_cpu=True
)

# Set up trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("./checkpoints/flan-orca-t5-base")
