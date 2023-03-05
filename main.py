import encode_dataset as ed


dataset = ed.DatasetEncoder()
dataset.set_path("maestro-v3.0.0")

print(dataset._file_parser())
tokens = dataset.convert_midis_to_string_words()
print(dataset.tokens_dictionary)
print(len(dataset.tokens_dictionary))


print(len(tokens))
print(tokens[100])
dataset.save_tokens()

dataset.open_token_dictionary("token_dictionary.pickle")
dataset.open_token_sequences("token_sequences.pickle")


print(len(tokens))
print(tokens[100])