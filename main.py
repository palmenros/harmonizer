from chord_generator import ChordGenerator
from definitions import NoteName, Note

if __name__ == "__main__":
    filename = "creation.mid"

    sequence = ChordGenerator.generate_chord_sequence(30)
    print(sequence)
    sequence.export_to_midi_file(filename)
