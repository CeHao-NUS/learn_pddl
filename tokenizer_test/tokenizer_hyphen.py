from collections import Counter
import re
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Sequence, Whitespace
from transformers import PreTrainedTokenizerFast

# Step 1: Define a function to tokenize hyphenated words and punctuation
def tokenize_with_hyphen(text):
    return re.findall(r'\w+(?:-\w+)*|[^\w\s]', text)

# Step 2: Load the article and build the vocabulary
article = """
This is an example article. It contains multiple sentences, repeated words, and punctuation!
For example, this sentence is repeated. This is an example article. No No No. real-world.
"""

# Tokenize the article using the custom function
tokens = tokenize_with_hyphen(article)
word_freq = Counter(tokens)

# Create a vocabulary with unique tokens and add special tokens
vocab = {word: idx for idx, (word, _) in enumerate(word_freq.items())}
vocab["[PAD]"] = len(vocab)  # Padding token
vocab["[UNK]"] = len(vocab)  # Unknown token

# Step 3: Create a WordLevel tokenizer
tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))

# Use a whitespace pre-tokenizer to split text at spaces
tokenizer.pre_tokenizer = Sequence([Whitespace()])

# Step 4: Wrap in PreTrainedTokenizerFast for compatibility
tokenizer_fast = PreTrainedTokenizerFast(tokenizer_object=tokenizer, unk_token="[UNK]", pad_token="[PAD]")

# Save the tokenizer
tokenizer_fast.save_pretrained("./custom_hyphen_tokenizer")

# Load the tokenizer
loaded_tokenizer = PreTrainedTokenizerFast.from_pretrained("./custom_hyphen_tokenizer")

# Step 5: Test the tokenizer on a sample text
sample_text = "This is a test for real-world examples and hyphenated-words."
tokens = loaded_tokenizer(sample_text, return_tensors="np")["input_ids"]
print("Input Text:", sample_text)
print("Token IDs:", tokens)

# Step 6: Convert token IDs back to tokens
token_ids = tokens[0]  # Extract token IDs from the tensor
converted_tokens = loaded_tokenizer.convert_ids_to_tokens(token_ids)
print("Converted Tokens:", converted_tokens)
