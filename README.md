# The Pool Hall
The Pool Hall is an app for member-only Pool Club.The app is a convenient way for members to reserve Pool tables for certin times. Members can log in check table availability, and book their time slot.The app also has an events page where the club can keep members up to date on the Club events and news.

# Strategy

This site is developed for a members only pool hall so that members can register their membership so they a book a table and see what time are available.
## Goals
The goal of this site is to build a booking system so staff of the pool hall can manage booking a members can make bookings online.


[Desktop Wireframes](documentation/poolhall%20wire%20%20frames/)

![ERD](documentation/erd.png)

 # LIVE LINK  [the Pool Hall](https://pp4poolhall-b3360ca06d73.herokuapp.com/)

# User Experience UX
----
Vistors to this site would be of the most part member of The Pool Hall Club They would be register on this app so they can make a booking for a table at the club and find information on Club events and news.

## Epics
This project was do in 5 epics, each epic has a list of user stories.

### [Epic 1](https://github.com/EdelCorbett/the-pool-hall/milestone/3) Basic System setup
Create the basic structure for a Django project                                              
### User Stories
- [As a Developer I can setup a project so that begin project.](https://github.com/EdelCorbett/the-pool-hall/issues/10)
- [As a Developer I can create a database so that store project](https://github.com/EdelCorbett/the-pool-hall/issues/11)
- [As a Developer I can Deploy project early so that I can continually test the application during development.](https://github.com/EdelCorbett/the-pool-hall/issues/12)

### [Epic 2](https://github.com/EdelCorbett/the-pool-hall/milestone/1)
This epic focuses on establishing a secure and user-friendly system for members to join and access the website's features and providing a secure and efficient authentication system for existing members.
### User Stories

- [As a Developer I can an Admin Site so that the site can be updated by the Admin](https://github.com/EdelCorbett/the-pool-hall/issues/14)
- [As a user I can create an account so that Register](https://github.com/EdelCorbett/the-pool-hall/issues/1)
- [As a user I can login so that I can book table.](https://github.com/EdelCorbett/the-pool-hall/issues/2)
- [As a Admin I can view memberships so that I can manage them](https://github.com/EdelCorbett/the-pool-hall/issues/9)
- [As an admin I can login so that I can view and manage bookings](https://github.com/EdelCorbett/the-pool-hall/issues/7)

### [Epic 3](https://github.com/EdelCorbett/the-pool-hall/milestone/2)
In this epic a booking form will be created and the user ability to cancel a booking.
### User Stories

- [As a users I can choose time so that make a reservation.](https://github.com/EdelCorbett/the-pool-hall/issues/3)






# Deployment
This Project was deployed through [HEROKU](https://www.heroku.com/) using these steps:

1. Create a Heroku account 
2. Then select New
3. [Select Create new app](documentation/heroku-new.png)
4. Name the App, select region
5. [Select Create app](documentation/name_region.png)
6. [Then select Settings from the menu bar](documentation/setting.png)
7. [From here scroll down to Config Vars and the KEY and VALUE to the list](documentation/config.png)
8. [Next add build packs for this project Python was used](documentation/build_pack.png)
9. [Then go to Deploy in the menu bar](documentation/deploy.png)
10. [Choose GitHub then choose connect to github](documentation/deploy-method.png)
11. [Now enter repository name in search](documentation/name.png) 
12. [Then click connect](documentation/connect.png)
13. [From here scroll down and pick either automatic Deploy or manual deploy](documentation/update-deploy.png)
14. [The app is now been built](documentation/building.png)
15. [Once this has finished click view to go to app](documentation/deployed_success.png)


---

## Local deployment

1. Clone the repository.

 - https://github.com/EdelCorbett/the-pool-hall

 2. Set up a virtual environment.

- Use the command 

        python3 -m venv venv 
        
   to create a new virtual environment named 'venv'.
- Activate the virtual environment with 

        source venv/bin/activate.

3. Install necessary packages.
 Then Run

        pip install -r requirements.txt 
        
        
   to install the dependencies required for the project.

 4. Create a env.py file.

 5.

 - Import the os module with import os.
 - Set your secret key with os.environ["SECRET_KEY"] = 'your secret key'.
 - Provide the database URL with os.environ["DATABASE_URL"] = 'your database url'.
- Provide Cloudinary URL with
os.environ["ClOUDINARY_URL"] your database url.

6. In settings.py File
 - Specify the debug mode ["DEBUG"] = 'True' or 'False'.
- Define the allowed hosts with os.environ["ALLOWED_HOSTS"] = 'app name.herokuapp.com','localhost'.
- Add  to installed apps
 

6. Set up and configure the database.

- Create the database
- Apply migrations to the Database 

- In terminal first run 

        python manage.py makemigrations

    Then Run
    
        python manage.py migrate

7. Create the superuser.

    In terminal

        python manage.py createsuperuser

### Setting Up a Database with ElephantSQL

1. Go to [ElephantSQL website](https://www.elephantsql.com/) and register for a new account.

2. Once registered, create a new database instance.

3. Assign a unique name to your database and opt for the free tier plan.

4. Proceed by clicking on "Select Region".

5. Choose a region that is close to you 

6. Review your selections by clicking on "Review".

7. Create your new database instance by clicking on "Create Instance".

8. Access your new database by clicking on its name, which will take you to the dashboard.

9. In the dashboard, you'll find the URL for your database. You'll need this URL to connect your Django project to the database.