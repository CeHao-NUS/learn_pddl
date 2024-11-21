from collections import Counter
import re
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Sequence, Whitespace, Punctuation
from transformers import PreTrainedTokenizerFast

# Step 1: Load the article
article = """
This is an example article. It contains multiple sentences, repeated words, and punctuation!
For example, this sentence is repeated. This is an example article. No No No. real-word. InFridge, RealWorld.
"""

# Step 2: Build the vocabulary from the article (with punctuation split)
# Tokenize the article
split_tokens = re.findall(r'\w+|[^\w\s]', article)  # Split on words and punctuation
word_freq = Counter(split_tokens)

# Create a vocabulary with unique tokens and add special tokens
vocab = {word: idx for idx, (word, _) in enumerate(word_freq.items())}
vocab["[PAD]"] = len(vocab)  # Padding token
vocab["[UNK]"] = len(vocab)  # Unknown token

# Step 3: Create a WordLevel tokenizer
tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))

# Use a combination of whitespace and punctuation splitting
tokenizer.pre_tokenizer = Sequence([Whitespace(), Punctuation()])

# Step 4: Wrap in PreTrainedTokenizerFast for compatibility
tokenizer_fast = PreTrainedTokenizerFast(tokenizer_object=tokenizer, unk_token="[UNK]", pad_token="[PAD]")

# Save the tokenizer
tokenizer_fast.save_pretrained("./custom_tokenizer")

# Load the tokenizer
loaded_tokenizer = PreTrainedTokenizerFast.from_pretrained("./custom_tokenizer")

# Step 5: Test the tokenizer on a sample text
# sample_text = "This is an example sentence. It contains punctuation! real-word. InFridge [PAD]"
sample_text = "[PAD]"
tokens = loaded_tokenizer(sample_text, return_tensors="np")["input_ids"]
print("Input Text:", sample_text)
print("Token IDs:", tokens)

# Step 6: Convert token IDs back to tokens
token_ids = tokens[0]  # Extract token IDs from the tensor
converted_tokens = loaded_tokenizer.convert_ids_to_tokens(token_ids)
print("Converted Tokens:", converted_tokens)
