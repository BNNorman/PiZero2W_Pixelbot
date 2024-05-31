# Speaker.md

The speaker only plays simple tones.

## speaker.play(freq,duration,pause_after=0,wait=True)

Plays a note of the given frequency and duration. If pause_after is non-zero inserts a period of silence. This enables you to play several notes one-after the other with a suitable inter-note gap.

Normally, this would only be used for warning beeps.
