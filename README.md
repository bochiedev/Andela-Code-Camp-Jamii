[![Build Status](https://travis-ci.com/bochiedev/Andela-Code-Camp-Jamii.svg?branch=master)](https://travis-ci.com/bochiedev/Andela-Code-Camp-Jamii)

[![Coverage Status](https://coveralls.io/repos/github/bochiedev/Andela-Code-Camp-Jamii/badge.svg?branch=master)](https://coveralls.io/github/bochiedev/Andela-Code-Camp-Jamii?branch=master)


# Jamii Business

A App that lets you register, login, logout and reset password for users,   
create, read, update and delete a business and/or its review the business.  

[Link to Jamii Business!](https://code-camp-jamii.herokuapp.com/)

#### Tasks

- [x] create UI and UX workflow
- [x] deploy to heroku
- [ ] Write tests
- [ ] Create reset password for users

###Resource(ENDPOINTS):

#### GET:

Endpoint | Function
--------- | ----------
/ | View home page
/home | View home page
/business | List all businesses
/businesses/>id</| List a single business
businesses/search/ | List all businesses found using a parameter search
/businesses/>id</reviews |  Get all reviews for a business


#### POST:

Endpoint | Function
--------- | ---------
/register/ | Register a user
/login/ | Login a user
/logout/ | Logout a user
/category/ | Create a business Category
/businesses/ | Create a business
/businesses/>id</reviews |  Create a review for a business

#### PUT & DELETE:

Endpoint | Function
--------- | ----------
/dashboard/ | Update an existing user
/businesses/edit/>id< | Update an existing business
/businesses/delete/>id<  | Delete an existing business


#### Installation

To get your build running just simply do:

* Git clone the repo to your machine;
  >  * git clone https://github.com/bochiedev/Andela-Code-Camp-Jamii.git
  >  * cd Andela-Code-Camp-Jamii

* Install virtualenv globally but if you got them you can skip this step;
> * pip install virtualenv

* Create a virtualenv ;
    * virtualenv ;
        > * virtualenv -p python3 venv             


* Install the requirements;
   > pip install -r requirements.txt

##### Run It!

To start the server just do;
> python run.py

The server will be running on    `http://127.0.0.1:5000/`   
Now you can include an endpoint of choice;   
eg:   `http://127.0.0.1:5000/register`


You can test on postman or use curl.
