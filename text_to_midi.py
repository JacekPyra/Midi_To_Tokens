import mido
from encode_dataset import DatasetEncoder
import os

if os.path.exists("output.mid"):
    os.remove("output.mid")
    print("Deleting output.mid ")

datasetEncoder = DatasetEncoder()

tokens = datasetEncoder.open_token_sequences("token_sequences.pickle")
datasetEncoder.open_token_dictionary("token_dictionary.pickle")

message_strings = datasetEncoder.decode_ints(tokens[3])
print(message_strings)

output = mido.MidiFile()
midi_messages = [mido.MetaMessage('set_tempo', tempo=500000, time=0),
                 mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                                  notated_32nd_notes_per_beat=8, time=0)]

for msg in message_strings.split("."):
    msg_parts = msg.split(" ")
    while "" in msg_parts:
        msg_parts.remove("")
    if len(msg_parts) > 0:
        if msg_parts[0] == "note_on":
            midi_messages.append(
                mido.Message("note_on",
                             channel=0,
                             note=int(msg_parts[1].strip("N")),
                             velocity=60 if msg_parts[2] == "ON" else 0,
                             time=int(msg_parts[3].strip("T"))))
        elif msg_parts[0] == "control_change":
            midi_messages.append(
                mido.Message("control_change",
                             channel=0,
                             control=int(msg_parts[1].strip("C")),
                             value=int(msg_parts[2].strip("V")),
                             time=int(msg_parts[3].strip("T"))))

output.tracks.append(midi_messages)
output.save("output.mid")
