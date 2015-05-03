# Adventure Time Classifier
a classifier that tells you who in Ooo talks most like you.

AT is awesome, maybe so great that sometimes we kinda talk like the characters do...

If you've ever been curious about who you're most like, this model is trained on the transcripts of every episode and aims to classify phrases by character.

# Current Status
Turns out the entirety of speech in the show is smaller than expected, about 19455 lines total and they range in size from 1 word to 5ish sentences(raw-data contains the whole transcript). I ended up using sklearn's Logistic Regression to get started and achieved raw accuracy scores in the high 40s to mid 50s range. Unfortunately, it appears this is the result of heavy overfitting on Finn and Jake (safe bets as they have the most lines by far). When trained on an even sample of 300 lines per every character that has at least 300, the raw accuracy hovers at ~0.35. More tweaking and testing soon!

## Update 0
Just finished MVP of scraper that automates the grabbing of transcript text, am now working on organizing data collection/labelling and have yet to start playing with [Indico](http://www.indico.io)'s model creation tool called [Passage](https://github.com/IndicoDataSolutions/Passage), authored by Alec Radford.

## ?
This is my first project that touches even a high level interface to ML, so it's going to be generally exploratory for me. If I can get my bearings and build something that works decently, I want to help others by making tutorials as I have been trying to document the process closely. Long way to go but up's the only road.

Interested in getting involved in this project? Suggestions? Definitely feel free to open a pull request or tweet [@illustratedDan](https://twitter.com/illustratedDan)
