Version 0 - Time frame (7-10 days):
1.  Ranking page: 
	- restore google sheet for ranking. 
		- Layout: 1st line is user's info (world ranking, username, score). 
		- Below scroll view for top 10 scores worldwide.
	-Additional issues with ranking (should be fixed)
		- RANKING DOES NOT UNDATE SCORE!! -- FIXED
		- RANKING RELOAD AND ADDS EACH TIME THE PAGE IS OPENED - IF YOU OPEN CONSECUTIVE TIMES NAMES APPEAR MULTIPLE TIMES ON THE LIST -- FIXED
2. Settings page:
	- add username for the user + check that username has not already been taken
3. Obstacles:
	- Clear obstacles upon death. Sometimes when you are reborn there are obstacles infront of you and you die immediately, fix that
	- Randomly obstacles lag (see video) - I suspect its is because of the background image restarting. 
	- Fix obstacle speed (bird become too fast) - set max upper speed	
	- Avoid obstacles being created too close to one another
4. Ads:
	- refresh banner every approx 10s while playing. Currently we display a single banner for the entire race. 
	- interstitials: avoid over advertising. Make sure interstitial are not shown too often when dieing. 

Version 1 - (20 days from Version 0):
1. Ads:
	- Add reward video for redemption when you die
2. In app purchases: 
	- Add in app purchases (no ads version of the game)
3. API:
	- Google leaderboard connectivity
	- Game Center connectivity
4. Graphics:
	- fix aesthetics of project - choose a color palate + stick with those colors all round - set screen to match that of the current phone you are on
	- design AOCT Dev logo
	- Try to add flower in the grass

Version 2 - (7 days from Version 1):
1. Gameplay:
	- Add reward like candies or kitten treats. Gather them --> Potentially: use reward ads also to unlock these candy
	- double jump recharge
	- Add jump height dependence with press time
2. Graphics: 
	- more cat colors --> unlock with score & candy
	- background that changes with the weather


Examples of how to use pyobjus:
- https://github.com/kivy/plyer/tree/master/plyer/platforms/ios
- https://github.com/eviltnan/kognitivo/blob/master/billing/android_billing.py
