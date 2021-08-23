from definitions import Chord
from definitions import Transition
from definitions import NoteName


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


def check_transition_table_probabilities():
    trans = get_transition_probability_table()
    for key in trans.keys():
        total_sum = 0
        for t in trans[key]:
            total_sum += t.probability
        print(f"{key} sums {total_sum}")


if __name__ == "__main__":
    check_transition_table_probabilities()