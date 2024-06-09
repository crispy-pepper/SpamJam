# SpamJam | JamHacks 2024
SpamJam is improving the lives of everyone one jar of jam at a time. Do you often find yoursef dozing off? Laying on the couch for hours, scrolling mindlessly? Well, SpamJam is the solution for you! Combining a dreadful siren and the addictive nature of gatcha games, tech nerds can be not only forced into excercising, but actually enjoying excercising. <br><br>

[SpaceJam - Demo](https://www.youtube.com/watch?v=fkfGmcQMPg4)

## Functions
- Buy and collect different flavoured jams - level up and earn berries
   - Different symbols, colours, expressions, and movement
- Tracks body features and turns "making" jam into an exercise mini game
- After a period of time (set by the user), SpamJam goes into "locked mode" where an extremely loud siren plays until exercise is completed and the user cannot close the fullscreened exercise window

## How it was built
The python libraries `opencv` and `mediapipe` where used to process and capture the landmarks while `pygame` was used to make the user interface and game. It is split up into 3 "pages": the main menu, the shop, and the gameplay (seperate window). Objects were created for each of the characters and buttons. The gameplay window was written as a seperate library `pp.py` where the sequences of the gameplay were stored and run. `Data.py` was used to store the games process. <br>
Libraries used:
- pygame
- time
- cv2
- mediapipe
- numpy
- random
