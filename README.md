Project Overview: The goal of the Real Estate Listing Web Application is to solve inefficiencies in both online and conventional real estate transaction systems. It offers a centralized platform with sophisticated screening, safe user identification, and an intuitive user experience that enables property owners, purchasers, and tenants to interact with property listings.
Steps to setup and Run code: cloning the repository and installing the dependencies/libraries flask, flask_sqlalchemy, flask_login, flask_wtf and etc,. and setting up real database, running the application like falsk run through local repository,
Dependencies and Prerequesites: python version, flask, flask_sqlalchemy, and some other dependencies
Explanation of the main files: **apps.py**--- where the skeleton view of the application will be there and it initializes the https requests, configure routes, and its functionalities are user page, admin page, register page. **models.py**-- here the user model if it is buyer or owner, property model like name, price and description etc and also favourite models. **forms.py**--- to handel validation and user input and ensuring correct data is submitted to login and registration and property management. **templates**-- contains html pages for to render dynamic web pages.
