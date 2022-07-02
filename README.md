# Fifa Manager Mode Backend API
A simulation of Fifa manager mode.

## Features
- User can play as a manager of an existing team or create a new club.
- Each team initially has a number of players (may vary from team to team).
- Manager can choose to hire scouts to scout new players for the team.
- Team attributes: name, country, owner, players, budget, value, starting manager salary.
- Player attributes: first name, last name, country, team, value, price, position, status, date of birth, and Attributes (associated to playing).
- Categories of attributes: athletism, physique, defense, attack, technique.
- All attributes associated to playing: pace, strength, stand tackle, slide tackle, acceleration, finishing, power, accuracy, curve, dribble, pass, long pass, vision, marking, positioning.
- Scout attributes: first name, last name, country, team, salary.
- A team can set any player on the transfer list.
- Buyer and seller teams can negotiate transfer deal.
- Transfer window must be open for transfers to happen.
- Players can be free agents.

## Setup Database and Environment
The database used here is `MySQL`.

## Testing and Running

## Design Principles
- Make all deals atomic transactions.
- Put different models in different modules.
- Make models fat if necessary but not views.
- Use class based views unless function views are absolutely necessary.
- Use an extra service layer between views and models.
- Test all modules and get close to 100% coverage.
- Maintain code quality using pylint.
