from enum import Enum
from midiutil import MIDIFile


class Chord(Enum):
    I = 0
    II = 1
    III = 2
    IV = 3
    V = 4
    VI = 5
    VII = 6

    def chord_number_starting_with_0(self):
        return self.value

    def chord_number_starting_with_1(self):
        return self.value + 1


class NoteName(Enum):
    DO = 0
    DO_s = 1
    RE = 2
    MI_b = 3
    MI = 4
    FA = 5
    FA_s = 6
    SOL = 7
    LA_b = 8
    LA = 9
    SI_b = 10
    SI = 11

    def offset_from_do(self):
        return self.value


class Transition:

    # In case restriction isn't None, if this transition is taken, the next
    # transition MUST be towards restriction chord
    def __init__(self, to: Chord, prob: float, restriction: Chord = None):
        self.to = to
        self.probability = prob
        self.restriction = restriction


class Note:
    def __init__(self, name: NoteName, octave: int):
        self.name = name
        self.octave = octave

    def get_midi_number(self):
        # MIDI Number corresponding to DO1, from which we calculate all other MIDI numbers
        MIDI_NUMBER_DO1 = 24
        return MIDI_NUMBER_DO1 + 12 * (self.octave - 1) + self.name.offset_from_do()


class ChordSequence:
    def __init__(self, initial_chords: list[Chord] = None):
        if initial_chords is not None:
            self.arr = initial_chords
        else:
            self.arr = []

    def append(self, chord: Chord):
        self.arr.append(chord)

    def export_to_midi_file(self, filename):
        import database

        track = 0
        channel = 0
        time = 0  # In beats
        duration = 2  # In beats
        tempo = 60  # In BPM
        volume = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
        # automatically)
        MyMIDI.addTempo(track, time, tempo)

        i = 0
        for chord in self:
            # Add all notes corresponding to this chord
            for name in database.get_chord_note_names()[chord]:
                # TODO: For now we treat all octaves as 4
                MyMIDI.addNote(track, channel, Note(name, 4).get_midi_number(), time + i, duration, volume)
            i += duration

        with open(filename, "wb") as output_file:
            MyMIDI.writeFile(output_file)

    def __str__(self):
        res = "["
        first = True
        for c in self:
            if first:
                first = False
            else:
                res += ", "
            res += c.name
        res += "]"
        return res

    def __iter__(self):
        return iter(self.arr)
