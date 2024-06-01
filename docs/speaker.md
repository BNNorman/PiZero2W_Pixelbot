# Speaker.md

The speaker only plays simple tones.

## speaker.play(freq,duration,pause_after=0,wait=True)

Plays a note of the given frequency and duration. If pause_after is non-zero inserts a period of silence. This enables you to play several notes one-after the other with a suitable inter-note gap.

Normally, this would only be used for warning beeps but can play a sequence of notes

# Example program

This example plays the 5 notes from Close Encounters of the Third Kind

```
# each note is frequency,duration,pause_before_next
music=[(196,.5,.1),(261,.5,.1),(174,.5,.1),(87,.5,.1),(130,1,2)]

while True:
    for note in music:
        (f,d,p)=note
        speaker.play(f,d,p)
    # have a rest before starting again
    time.sleep(2)
```
