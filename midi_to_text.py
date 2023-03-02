import mido

PATH = "/home/oem/PycharmProjects/midi_notes_reader/maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi"

file = mido.MidiFile(filename=PATH)
print(file.ticks_per_beat)
msg_types = {}

print("start")
message_strings = ""
for track in file.tracks:
    for msg in track:
        msg_types[msg.type] = msg
        if isinstance(msg, mido.Message):
            if msg.type in ["note_on"]:
                message_strings += f"{msg.type} N{msg.note} {'ON' if msg.velocity > 0 else 'OFF'} T{msg.time} . "
            if msg.type == "control_change":
                message_strings += f"{msg.type} C{msg.control} V{60} T{msg.time} . "

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
output.save("a.mid")

print(msg_types)
