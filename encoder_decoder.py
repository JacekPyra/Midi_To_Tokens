import mido


class Encoder:
    def __init__(self, path):
        self.file = mido.MidiFile(filename=path)
        self.tokens_dictionary = {}
        self.dictionary_of_tokens = {}
        self.vocabulary = {".": 1}

    def __add_words_to_vocabulary(self, *args):
        for arg in args:
            self.vocabulary[arg] = True

    def encode_as_strings(self):
        """ create unique strings for each field in Message objects"""
        message_strings = ""
        msg_types = {}

        for track in self.file.tracks:
            for msg in track:
                msg_types[msg.type] = msg
                if isinstance(msg, mido.Message):
                    if msg.type in ["note_on"]:
                        velocity = 'ON' if msg.velocity > 0 else 'OFF'
                        self.__add_words_to_vocabulary(msg.type, "N"+str(msg.note), velocity, "T"+str(msg.time))
                        message_strings += f"{msg.type} N{msg.note} {velocity} T{msg.time} . "
                    if msg.type in ["control_change"]:
                        self.__add_words_to_vocabulary(msg.type, "C"+str(msg.control), "V60", "T"+str(msg.time))
                        message_strings += f"{msg.type} C{msg.control} V60 T{msg.time} . "

        print("Unique words in this piece: ", len(self.vocabulary))
        return message_strings

    def encode_as_ints(self, message_strings:str, tokens_dict:dict = None):
        messages = message_strings.split(" ")
        while "" in messages:
            messages.remove("")

        if tokens_dict is None:
            self.tokens_dictionary = {}
            index = 1
            for word in self.vocabulary:
                index += 1
                self.tokens_dictionary[word] = index
        else:
            self.tokens_dictionary = tokens_dict
            index = len(tokens_dict)
            for word in self.vocabulary:
                if self.tokens_dictionary.get(word) is None:
                    index += 1
                    self.tokens_dictionary[word] = index

        token_list = []
        for message in messages:
            token_list.append(self.tokens_dictionary[message])

        return token_list, self.tokens_dictionary
