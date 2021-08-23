from definitions import Chord, ChordSequence, Database
import random as rnd


class ChordGenerator:
    @staticmethod
    def generate_chord_sequence(length) -> ChordSequence:
        current_chord = Chord.I
        chord_sequence = ChordSequence([Chord.I])

        # We repeat until we run out of chords to generate
        while length > 0:
            length -= 1
            random_number = rnd.random()

            # Let's calculate the corresponding transition to the chosen random number

            # Accumulated probability with previous list elements
            accumulated_probability = 0

            for t in Database.get_transition_probability_table()[current_chord]:
                accumulated_probability += t.probability
                if random_number <= accumulated_probability:
                    # We take this transition
                    chord_sequence.append(t.to)

                    if t.restriction is not None:
                        chord_sequence.append(t.restriction)
                        current_chord = t.restriction
                    else:
                        current_chord = t.to

                    break

        return chord_sequence
