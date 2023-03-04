import glob
import pickle
import json

from encoder_decoder import Encoder


class DatasetEncoder:
    def __init__(self):
        self.path = ""
        self.midi_files_list = []
        self._file_parser()
        self.tokens_dictionary = {".": 0}
        self.tokens_sequences = []

    def set_path(self, path):
        self.path = path

    def _file_parser(self):
        filenames = glob.glob(self.path + "\**\*.*", recursive=True)
        for f in filenames:
            if f.endswith(".mid") or f.endswith(".midi"):
                self.midi_files_list.append(f)
        return self.midi_files_list

    def convert_midis_to_tokens(self):
        for index, file in enumerate(self.midi_files_list):
            print(f"\nFile number {index}:\n {file}")
            encoder = Encoder(file)
            token_strings = encoder.encode_as_strings()
            token_ints, self.tokens_dictionary = encoder.encode_as_ints(token_strings, self.tokens_dictionary)
            self.tokens_sequences.append(token_ints)
        return self.tokens_sequences

    def save_tokens(self, json_save=False):
        if json_save:
            with open("token_sequences.json", "w+") as file:
                json.dump(self.tokens_sequences, file)

            with open("token_dictionary.json", "w+") as file:
                json.dump(self.tokens_dictionary, file)
        else:
            with open("token_sequences.pickle", "wb") as file:
                pickle.dump(self.tokens_sequences, file)

            with open("token_dictionary.pickle", "wb") as file:
                pickle.dump(self.tokens_dictionary, file)

    @staticmethod
    def __open_json(path):
        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def __open_pickle(path):
        with open(path, "rb") as file:
            return pickle.load(file)

    def open_token_sequences(self, path):
        if path.endswith(".json"):
            self.tokens_sequences = self.__open_json(path)
        elif path.endswith(".pickle"):
            self.tokens_sequences = self.__open_pickle(path)
        return self.tokens_sequences

    def open_token_dictionary(self, path):
        if path.endswith(".json"):
            self.tokens_dictionary = self.__open_json(path)
        elif path.endswith(".pickle"):
            self.tokens_dictionary = self.__open_pickle(path)
        return self.tokens_dictionary

    def decode_ints(self, tokens:list) -> str:
        decoded_tokens = ""
        inv_tokens_dictionary = {v: k for k, v in self.tokens_dictionary.items()}
        for number in tokens:
            decoded_tokens += inv_tokens_dictionary[int(number)] + " "
        return decoded_tokens
