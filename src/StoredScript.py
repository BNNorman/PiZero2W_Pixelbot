# Music
music = [(196, 1, .1), (261, 1, .1), (174, 1, .1), (87, 1, .1), (130, 2, 0)]
for (f,d,w) in music:
    # f=frequency, d=duration, w=wait_after (between notes)
    speaker.play(f,d,w,True) # play note and wait
