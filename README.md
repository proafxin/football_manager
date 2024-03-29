# Fifa Manager Mode Simulation

## Development stopped for higher priority stuff

![Build](https://github.com/proafxin/football_manager/actions/workflows/test.yml/badge.svg)

![codecov](https://github.com/proafxin/football_manager/blob/develop/coverage.svg)

A virtual backend simulation of football manager mode.

## Features

- User can play as a manager of an existing team or create a new club.
- Each team initially has a number of players (may vary from team to team).
- Manager can choose to hire scouts to scout new players for the team (lower priority so will be implemented last, if at all).
- Team attributes: name, country, owner, players, budget, value, starting manager salary.
- Player attributes: first name, last name, country, team, value, price, position, status, date of birth, and Attributes (associated to playing).
- Categories of attributes: athletism, physique, defense, attack, technique.
- All attributes associated to playing: pace, strength, stand tackle, slide tackle, acceleration, finishing, power, accuracy, curve, dribble, pass, long pass, vision, marking, positioning, form, morale.
- Scout attributes: first name, last name, country, team, salary.
- A team can set any player on the transfer list.
- Buyer and seller teams can negotiate transfer deal.
- Transfer window must be open for transfers to happen.
- Players can be free agents.
- Team can buy players or take players on loan.
- In loans, dealing teams must agree on proportions of contribution to the salary of the player.
- Players and Managers can negotiate salary with the team.
- Managers can search for jobs.

## Setup Database and Environment

The database used here is `MySQL`. Create the following environment variables in your operating system with appropriate values for Django to access the database.

- DATABASE_NAME
- DATABASE_USERNAME
- DATABASE_HOST
- DATABASE_PASSWORD
- DATABASE_PORT

Go to MySQL terminal as root user. Run `show databases;` and see the list of databases. If your database is not created, run `create database {DATABASE_NAME};`. Replace {DATABASE_NAME} with the value of the environment variable. Run `show databases;` again and make sure the database is in the list. Run `CREATE USER '{DATABASE_USERNAME}'@'{DATABASE_HOST}' IDENTIFIED BY '{DATABASE_PASSWORD}';` then `GRANT ALL ON DATABASE_NAME.* TO '{DATABASE_USERNAME}'@'{DATABASE_HOST}';` and `FLUSH PRIVILEGES;`. Replace the variables with appropriate values from environment variables. If your database is hosted in your machine, `{DATABASE_HOST}` should be `localhost`. Make sure that the user you create has permission to create test database when tox runs the tests.

Make sure you have `virtualenv` installed (`python -m pip install virtualenv`). You may need to specify `python3` instead of `python` depending on your system. Create a virtual environment in your root project directory using `virtualenv env`. Activate the environment using `env/Scripts/activate` on Windows or `source bin/activate` on Linux/Mac. When you are done, you can deactivate the environment by using `deactivate`. Inside the environment, run `python -m pip install -r requirements.txt`.

Generate a Django secret key and assign it to the environment variable `FIFA_MANAGER_DJANGO_SECRET_KEY` in your machine.

Run `python manage.py makemigrations manager` and `python manage.py makemigrations`. Then run `python manage.py migrate`. This will create the necessary tables for the application to run.

## Testing and Running

Activate the virtual environment in your root project directory. Run `tox` command. See that all commands succeed.

If you want to run the commands individually, run the tests using the command `python .\manage.py test --settings='fifa_manager.setting.testing'`. See that all tests are passed. After all tests pass, run `coverage report -m` and check that coverage is at least 95%. Then run `pylint .\manager\ --disable=wrong-import-order,too-many-instance-attributes --ignore=migrations,admin.py,apps.py` and verify that the score is 10/10 with no errors/warnings in pylint.

Finally, run the project using `python manage.py runserver 8000`. You can specify another port if necessary.

## Generating Documentation

Change to `docs` directory. Run `sphinx-apidoc.exe -f -o . .. ..\manager\migrations\ ..\manager\tests\  ..\manage.py` then `.\make clean` and `.\make html`. Output should be built with no errors or warnings.

Run `sphinx-quickstart`. In `conf.py`, uncomment the lines
    ```
    import os
    import sys
    sys.path.insert(0, os.path.abspath("."))
    ```
and save it. Add `"sphinx.ext.autodoc",` to the `extensions` list. Run `python -m pip install -U sphinx_rtd_theme` and set `html_theme = "sphinx_rtd_theme"`.

## Design Principles

- Make all deals atomic transactions.
- Put different models in different modules.
- Make models fat if necessary but not views.
- Use class based views unless function views are absolutely necessary.
- Use an extra service layer between views and models.
- Put different tests in different modules.
- Test all modules and get close to 100% coverage.
- Maintain code quality using pylint.
- Split settings for different uses. Testing will be done using the `testing` setting in `fifa_manager.setting.testing`.
