# mentalMendingApp
a mobile app base on gamification in order to help users confront their daily struggles

dev log
12 days remaining at date of writing this
The app must have, as a bare minimun:
- routing: create new battle, main battle hub, and the battle scenario (listo)
- create new battle: name of the enemy and the emotion asociated (listo)
- main battle hub: icons to select and resume current battles (listo)
- battle scenario: player as a trail, enemy in the top with his idle animation, damage feedback, and attack of the enemy
- logo and stable deploy

2 days to develop each point

note for develop:
all the proyect is build on top of mentalmending.kv, our principal ui template, in order to convert every aspect of the app in modules, when need to specify two main widgets, the first one is going to be the top and bottom addon, which one version will be for menu navigation, and the other version to the battle menu; the second main widget is going to be the current screen, and this will be the forman, main hub or the batlle place
this ensures that we can referenciate those widgets allways loaded in the main kv