## Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app.
                    "python app.py" to run after installing dependences
  ├── models.py *** includes all defined models and their methods.
  ├── enums.py *** Contains all enums for validating forms.
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Main driver behind forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user.
* `models.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code.

### Features:
At it's current state, this app provide the following features:
1. posting, editing and listing of artists and venues.
2. ability to search for artists or venues based on their names, cities, states and genres.
3. post new shows to the app. The app validates the artist's availability on the show's specified date and provides user feedback.
4. Artists can choose days of the week in which they can be booked by venues.

### Development Setup

First, [install Postgresql](https://www.postgresql.org/download/) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

### pipenv setup
you can also run a local virtual environment using pipenv:
```
$ pip3 install pipenv
$ cd PROJECT_DIRECTORY_PATH/
$ pipenv shell
$ pipenv install # installing dependencies
```
pipenv will install all required dependencies for you.

### migrating data
before running the application, you should create a database, and set the credentials in the `config.py` file.
After that, run the flask migration tool to create the application database schema.
```
$ flask db upgrade
```

### to do:
A few things I want to follow up on with this project:
1. Better time availability implementation.
2. User management for artists and venues.
3. Showcases for artists and venues. (live performances, sound cloud integration, etc...)
4. public profile pages for artists, venues, and shows.

### Final Notes:
While this was a project to demenstrate my abilities to work with flask and SQLAlchemy, I find this app very interesting, and I honestly could see myself developing it further.
The consipt of such application in saudi is very promicing, hopefully I will be able to do that in the future, or maybe someone else will.