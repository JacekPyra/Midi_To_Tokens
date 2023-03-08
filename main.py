import encode_dataset as ed


dataset = ed.DatasetEncoder()
dataset.path = "/home/oem/PycharmProjects/midi_notes_reader"
dataset.find_midi_files()


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