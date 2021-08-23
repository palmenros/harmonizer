from enum import Enum
from midiutil import MIDIFile


class Database:
    @staticmethod
    def get_transition_probability_table():
        return {
            Chord.I: [Transition(Chord.IV, 0.37), Transition(Chord.VI, 0.23), Transition(Chord.II, 0.25), Transition(Chord.V, 0.14), Transition(Chord.VII, 0.01)],
            Chord.II: [Transition(Chord.V, 0.80), Transition(Chord.VII, 0.17), Transition(Chord.VI, 0.03)],
            Chord.III: [Transition(Chord.IV, 0.22), Transition(Chord.I, 0.18, Chord.IV), Transition(Chord.VI, 0.60)],
            Chord.IV: [Transition(Chord.VII, 0.28), Transition(Chord.II, 0.24), Transition(Chord.V, 0.33), Transition(Chord.I, 0.15)],
            Chord.V: [Transition(Chord.I, 0.85), Transition(Chord.VI, 0.13), Transition(Chord.IV, 0.02)],
            Chord.VI: [Transition(Chord.II, 0.55), Transition(Chord.V, 0.07), Transition(Chord.IV, 0.35), Transition(Chord.III, 0.03)],
            Chord.VII: [Transition(Chord.III, 0.42), Transition(Chord.I, 0.51), Transition(Chord.V, 0.07)]
        }

    @staticmethod
    def get_chord_note_names():
        return {
            Chord.I: [NoteName.DO, NoteName.MI, NoteName.SOL],
            Chord.II: [NoteName.RE, NoteName.FA, NoteName.LA],
            Chord.III: [NoteName.MI, NoteName.SOL, NoteName.SI],
            Chord.IV: [NoteName.FA, NoteName.LA, NoteName.DO],
            Chord.V: [NoteName.SOL, NoteName.SI, NoteName.RE, NoteName.FA],
            Chord.VI: [NoteName.LA, NoteName.DO, NoteName.MI],
            Chord.VII: [NoteName.SI, NoteName.RE, NoteName.FA]
        }

    @staticmethod
    def get_voice_ranges():
        return {
            Voice.SOPRANO: (Note(NoteName.MI, 4), Note(NoteName.LA, 5)),
            Voice.CONTRALTO: (Note(NoteName.SI, 3), Note(NoteName.DO, 5)),
            Voice.TENOR: (Note(NoteName.FA, 3), Note(NoteName.SOL, 4)),
            Voice.BASS: (Note(NoteName.MI, 2), Note(NoteName.DO, 4))
        }

    # First notes will have smaller ranges
    @staticmethod
    def get_voice_ranges_first_chord():
        return {
            Voice.SOPRANO: (Note(NoteName.SOL, 4), Note(NoteName.MI, 5)),
            Voice.CONTRALTO: (Note(NoteName.SI, 3), Note(NoteName.SOL, 5)),
            Voice.TENOR: (Note(NoteName.FA, 3), Note(NoteName.DO, 4))
        }

    @staticmethod
    def get_voice_octave_range():
        return {
            Voice.SOPRANO: range(4, 6),
            Voice.CONTRALTO: range(3, 6),
            Voice.TENOR: range(3, 5),
            Voice.BASS: range(2, 5)
        }

    # Helper
    @staticmethod
    def check_transition_table_probabilities():
        trans = Database.get_transition_probability_table()
        for key in trans.keys():
            total_sum = 0
            for t in trans[key]:
                total_sum += t.probability
            print(f"{key} sums {total_sum}")


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


class Note:
    def __init__(self, name: NoteName, octave: int):
        self.name = name
        self.octave = octave

    def get_midi_number(self):
        # MIDI Number corresponding to DO1, from which we calculate all other MIDI numbers
        MIDI_NUMBER_DO1 = 24
        return MIDI_NUMBER_DO1 + 12 * (self.octave - 1) + self.name.offset_from_do()

    def __str__(self):
        return self.name.name + str(self.octave)

    # Relational operators
    def __eq__(self, other):
        if isinstance(other, Note):
            return self.get_midi_number() == other.get_midi_number()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.get_midi_number())

    def __lt__(self, other):
        return self.get_midi_number() < other.get_midi_number()

    def __gt__(self, other):
        return self.get_midi_number() > other.get_midi_number()

    def __le__(self, other):
        return self.get_midi_number() <= other.get_midi_number()

    def __ge__(self, other):
        return self.get_midi_number() >= other.get_midi_number()


class Chord(Enum):
    I = 0
    II = 1
    III = 2
    IV = 3
    V = 4
    VI = 5
    VII = 6

    def chord_number_starting_with_0(self) -> int:
        return self.value

    def chord_number_starting_with_1(self) -> int:
        return self.value + 1

    def get_required_note_names(self) -> list[NoteName]:
        arr = Database.get_chord_note_names()[self].copy()
        if self == Chord.VII:
            return arr

        del arr[2]
        return arr


class Transition:

    # In case restriction isn't None, if this transition is taken, the next
    # transition MUST be towards restriction chord
    def __init__(self, to: Chord, prob: float, restriction: Chord = None):
        self.to = to
        self.probability = prob
        self.restriction = restriction


class ChordSequence:

    def __init__(self, initial_chords: list[Chord] = None):
        if initial_chords is not None:
            self.arr = initial_chords
        else:
            self.arr = []

    def append(self, chord: Chord):
        self.arr.append(chord)

    def export_to_midi_file(self, filename: str):
        track = 0
        channel = 0
        time = 0  # In beats
        duration = 2  # In beats
        tempo = 90  # In BPM
        volume = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
        # automatically)
        MyMIDI.addTempo(track, time, tempo)

        i = 0
        for chord in self:
            # Add all notes corresponding to this chord
            for name in Database.get_chord_note_names()[chord]:
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


class Voice(Enum):
    BASS = 0
    TENOR = 1
    CONTRALTO = 2
    SOPRANO = 3

    def is_note_in_range(self, note: Note, first_chord: bool = False) -> bool:
        if first_chord:
            low, high = Database.get_voice_ranges()[self]
        else:
            low, high = Database.get_voice_ranges_first_chord()[self]

        return low <= note <= high

    def return_possible_note_names(self, possible_note_names, first_chord: bool = False) -> list[Note]:
        res = []
        for octave in Database.get_voice_octave_range()[self]:
            for note_name in possible_note_names:
                note = Note(note_name, octave)
                if self.is_note_in_range(note, first_chord):
                    res.append(note)
        return res


class VoiceLeadChord:
    def __init__(self):
        self.arr = [None, None, None, None]

    def __len__(self):
        return len(self.arr)

    def __iter__(self):
        return iter(self.arr)

    def __delitem__(self, key):
        if isinstance(key, Voice):
            key = key.value

        self.arr.__delitem__(key)

    def __getitem__(self, key):
        if isinstance(key, Voice):
            key = key.value

        return self.arr.__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, Voice):
            key = key.value

        self.arr.__setitem__(key, value)
