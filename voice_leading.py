from definitions import ChordSequence, VoiceLeadChord, Note, NoteName, Voice, Chord


def voice_lead(chord_sequence: ChordSequence):
    pass


def generate_first_voice_led_chord() -> VoiceLeadChord:
    chord = VoiceLeadChord()

    # The bass will always do a DO3
    chord[Voice.BASS] = Note(NoteName.DO, 3)

    # We generate the rest of the voices
    res = []
    backtrack_first_voice(chord, 1, Chord.I, Database.get_chord_note_names()[Chord.I] )

"""
    Asignar a cada voz una nota (nombre de nota y octava). 
    Empezamos asignando de más baja a más alta por backtracking. Podamos con las siguientes restricciones:
        1* Bajo <= Tenor <= Contralto <= Soprano
        2* Soprano(t).midi - Contralto(t).midi <= 12
        3* Que finalmente se usen todas las notas del acorde

    k: Indice de la voz a asignar ahora mismo (entre 0 y 3)
"""
def backtrack_first_voice(
        current_voice_led_chord : VoiceLeadChord,
        k,
        chord : Chord,
        yet_to_be_used_notes : list[NoteName],
        res: list[VoiceLeadChord],
        used_third_note: bool # Marca si se ha usado todavía la tercera nota del array (la que es opcional en la mayoría de acordes)
):
    pass


if __name__ == "__main__":
    from definitions import Database
    # arr = Voice.SOPRANO.return_possible_note_names(Database.get_chord_note_names()[Chord.I])

    for c in Chord:
        arr = c.get_required_note_names()
        print([str(e) for e in arr])