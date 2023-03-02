import music21 as mu
from fractions import Fraction

PATH = "/home/oem/PycharmProjects/midi_notes_reader/maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi"
# PATH = "/home/oem/PycharmProjects/midi_notes_reader/output.mid"

score = mu.converter.parse(PATH)
instruments_list = mu.instrument.partitionByInstrument(score)

notes = []

for instrument in instruments_list:
    print(instrument)
    for element in instrument.recurse():
        if str(type(element)) == "<class 'music21.note.Note'>":
            notes.append(element)
        elif str(type(element)) == "<class 'music21.note.Rest'>":
            notes.append(element)
        elif str(type(element)) == "<class 'music21.chord.Chord'>":
            notes.append(element)

song_tokens = ""


def add_offset_token(offset_diff):
    return f"OFF{(offset_diff)} "


offset_prev = 0
offset_diff = 0
for idx, el in enumerate(notes):
    offset_diff = float(Fraction(el.offset)) - offset_prev
    offset_prev = float(Fraction(el.offset))
    print(float(Fraction(el.offset)), offset_diff, el.duration.quarterLength)
    if offset_diff > 0:
        song_tokens += add_offset_token(offset_diff)

    if isinstance(el, mu.note.Note):
        song_tokens += f" NOTE {notes[idx].duration.quarterLength} {notes[idx].pitch} "
    if isinstance(el, mu.chord.Chord):
        song_tokens += f" CHORD {notes[idx].duration.quarterLength} " \
                       f"{' '.join([str(a.pitch) for a in notes[idx].notes])} "
    if isinstance(el, mu.note.Rest):
        song_tokens += f" REST {notes[idx].duration.quarterLength} "


def notefy(buffer):
    duration = float(Fraction(buffer[0]))
    pitch = buffer[1]
    note = mu.note.Note(pitch, quarterLength=duration)
    return note


def chordify(buffer):
    duration = float(Fraction(buffer[0]))
    pitches = buffer[1:]
    chord = mu.chord.Chord(pitches, quarterLength=duration)
    return chord


def restify(buffer):
    duration = float(Fraction(buffer[0]))
    rest = mu.note.Rest(quarterLength=duration)
    return rest


def tokens_to_midi(token_string):
    offset = 0.0
    token_list = [a for a in token_string.split(" ") if a != '']

    m21_stream = mu.stream.Stream()
    obj = None
    buffer = [token_list[0]]
    print(token_list[:100])

    for token in token_list[1:]:  # start from i=1
        if "OFF" in token:
            offset += float(token.strip("OFF"))
            continue

        if token not in ['NOTE', 'REST', 'CHORD']:
            buffer.append(token)
        else:
            if buffer[0] == 'REST':
                obj = restify(buffer[1:])
            elif buffer[0] == 'NOTE':
                offset += 0.25
                obj = notefy(buffer[1:])
            elif buffer[0] == 'CHORD':
                obj = chordify(buffer[1:])

            m21_stream.insert(offset, obj)
            buffer = [token]  # reset buffer with current token
    return m21_stream


stream = tokens_to_midi(song_tokens)
fp = stream.write('midi', fp='output.mid')
