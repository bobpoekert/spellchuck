Spellcheck
==========

Client-side spell checker using Count-Min Sketch.

Procedure for checking spelling of word is as follows:
------------------------------------------------------

1. Download Count-Min Sketch of word counts observed from wikipedia stored as png file (via PIL)

2. Add image to canvas

3. Get Typed Array view of canvas framebuffer (ie: the counts)

4. For each word less than three edits away from given word, look up word count

5. Pick argmax word count / edit distance from edits
