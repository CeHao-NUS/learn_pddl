from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import PreTrainedTokenizerFast

# Step 1: Define your limited vocabulary
vocab = ["hello", "world", "I", "am", "learning", "[PAD]", "[UNK]"]
vocab_dict = {word: i for i, word in enumerate(vocab)}

# Step 2: Create a tokenizer with a WordLevel model
tokenizer = Tokenizer(WordLevel(vocab=vocab_dict, unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()  # Simple whitespace tokenizer

# Step 3: Save the tokenizer to a file
tokenizer_file_path = "custom_tokenizer.json"
tokenizer.save(tokenizer_file_path)

# Step 4: Load the custom tokenizer with PreTrainedTokenizerFast
tokenizer_fast = PreTrainedTokenizerFast(tokenizer_file=tokenizer_file_path, unk_token="[UNK]", pad_token="[PAD]")

# Step 5: Test the tokenizer
text = "hello am"
tokens = tokenizer_fast(text, return_tensors="np")["input_ids"]
print("Input text:", text)
print("Token IDs:", tokens)
