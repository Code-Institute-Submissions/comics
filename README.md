# Comic Box

## Milestone Project 3 - Data Centric Developement

## Bobby Jackson

<img src="/static/images/responsive-mockup.jpg" alt="responsive-mockup">

A site designed for use by anyone that is enthusiastic about reading, sharing and finding comic books.
The website contains comics from a variety of genres. 
The website features a gallery of various comic books with search function, user registration, comic book editting,
the ability to favourite comics and a contact page. 
The primary goal of the website is to create a large collection of various comic books for a wide user base. 

## UX

The ideal user for this site is:
- Interested in sharing and recommending comic books they have read.
- Interested in searching for new comics to read.
- English speaking.

Visitors to the site are looking for:
- A place to return to for suggestions on the next comic book to read.
- The ability to make new entries on comics that may not be already on the site.
- The ability to favourite comics they are interested in reading, so they can easily find them in the future. 

The website should be:
- Easy to navigate.
- Have a simple registration and log in.
- Able to search through a collection of comics to find specific ones.
- Able to moderate content added to the site. 

### User Stories

#### New User

1. As a new visitor, I want to be able to navigate the site with ease.
2. As a new visitor, I want to be able to use the site before registering, 
   and still be able to use most features, so that I make a informed decision on whether to sign up. 
3. As a new visitor, I want to be able to sign up easily and get started browsing.

#### Returning User
1. As a returning user, I want to be able to favourite comics to know which ones I am interested in.
2. As a returning user, I want to provide my own entries to the collection.
3. As a returning user, I want to be able to edit my details should they change.
4. As a returning user, I want an easy to fill-in contact form, so I can contact the owner of the site for new ideas or to help moderate the site.

#### Moderator

1. As a moderator, I want to be able to edit or delete other user posts should they contain anything inappropriate.
2. As a moderator, I want to be able to give other users the moderator status should they be willing to help maintain the site.

### Design

- Colour Scheme
    - The colour scheme for the site was based on the [Spider-Man](https://www.behance.net/gallery/18419415/Comic-Books-Color-Palettes) colour 
      pallete, which was found while searching on Google.

- Imagery
    - The images used throughout the site are chosen to appeal to comic book readers and people with an interest in superhero comics.

### Wireframe Mockups

- Site Map - [View](https://github.com/bob134552/comics/tree/master/wireframes/sitemap.pdf)
- Deskop Wireframe - [View](https://github.com/bob134552/comics/tree/master/wireframes/desktop-wf.pdf)
- Mobile Wireframe - [View](https://github.com/bob134552/comics/tree/master/wireframes/mobile-wf.pdf)

## Features

Every page features a responsive navigation bar(navbar) containing relevant links depending on who is using the site. The site logo which sits at the left of the
navbar and also redirects users to the home page.

#### Home Page

The Home page is the main page of the site and features a full gallery of all user submitted comics. 
Some comics with mature content are omitted for users under the age of 16 and for users not logged in.
The home page also contains a search bar for users to find comics based on
the comics name, description, author or genre. The page also allows the user to see more about individual comics and redirect them to a
site where they may purchase the comic if interested.

The Home page allows signed in users to favourite/unfavourite comics by clicking the heart button next to each comic image.

A comic entry will have management options if the user is a moderator or the one who submitted the comic(Edit and delete).

#### Profile Page

The Profile Page allows users to view/change any relevant information about themselves through the edit profile button or the change password button.
Moderators are able to grant mod status to non moderator users.
It is also possible to view the profile page of users that have submitted comics. 
If you click on the username visible when looking at the added comic, it will bring you to that users profile page. 

#### New/Edit Entry Page

This page consits of a form gathering all the relevant information required for inputting or editing a new comic on the site.
 In particular this includes the following:
 - Comic name
 - Author
 - Brand
 - Genre
 - Cover Image link
 - Synopsis
 - Store link (to buy)
 - Check box if there is mature content

If the inputted comic already exists, the user will be notified after clicking on the submit button and the comic is not added to the site. 

#### My Submission Page

This page only displays submissions made by the logged in user. 
Similar to the Home page it displays a gallery of the submitted comics by the user. 
The comics on the Submission page can be favourited, deleted or edited. 
A search bar is also available, similar to the Home Page, where users can search for comics based on the comics name, description, author or genre.

#### Favourites Page

This page is similar in apperance to the Submission/Home page. 
Any comics that have been favourited, 
by clicking on the 'heart' button, appear in the gallery on the Favourites page. Comics can be favouited from either the Home or Submission pages.  
Deleting/editing is availalbe if the comic was submitted by the logged in user, or if the user is a moderator. 
It is possible to remove any comics from the favourite page by clicking on the 'heart' button. 
A buy button takes you to a site for purchasing the comic, as on the Home and Submission pages. 
A search bar is also included as on the Home and Submission pages.


#### Contact Page

The Contact page features a contact form, which requests the following information:
- Name
- Email Address
- Subject
- Message

There is a submit button on the bottom of the page, which allows the user to send their message after completing the form. 
If any of the above inputs are empty, after clicking submit, the message will not be sent,
and the user is notified of the required information that was missing. 

#### Register Page

The Register page is only visible to users that are not logged in or new users. 
This page allows a new user to input their information so that they can be added to the database.
This allows them to login and use all features (excluding moderator features) of the website.
The register page featres a registration form, which requires the following information: 
- First Name
- Last Name
- Date of Birth
- Email
- Username
- Password

A submit button at the bottom of the registration form allows the user to input the information to the database. 
On the registration form if any field is left empty/incorrectly filled, a red line appears underneath the inccorect information.
Additionally, the form cannot be submitted unless all fields are correctly filled. 
The user is notified of the missing inforation if they click on the submit button before all fields are correctly filled. 
If the inputted username is already taken, the user will be notified after clicking on the submit button, so that they can pick a different username.

Below the submit button, there is a link to the login page for users that are already registered. 

#### Login Page

The Login page contains a simple form that requires two inputs; username and password.
A submit button below the form brings the user to their Home page, if the login details are entered correctly.
If the details are incorrect the user is notified that either the username/password was incorrect. 
Below the submit button, there is a link to the registration page for users that are not registered. 

#### 404 Page

This page is used to handle 404 errors in the event that the user tries to open a page that does not exist.
It contains a button that redirects users to the Home page.

### Existing Features

- Callout button for both users and new visitors, Allows new visitors to register and users to go to new entry page.
- Navbar logo on all pages, Allows users to return to the home page.
- Search bar, allows users to search comic book collection.
- Mature filter, Filters content for users under 16.
- Card gallery, Displays all available comics in the collection.
- New entry form, Allows users to submit their own comic suggestions.
- Profile page, Allows users to edit their own information.
- Comic page, Displays more information on a chosen comic.
- Favourite/Unfavourite button and page, Users are able to favourite and unfavourite comics and view them on a seperate page.
- Contact page, For users that would like to message the creator of the site.
- Registration form, Allowing users to easily sign up to the site.
- Edit and delete function for comics, Allows users to edit and delete their submissions.
- Moderator system, Allows users to become Moderators in order to monitor/edit/delete submissions. 
- 404 error handling, To redirect user back to the Home page if they try accessing other non existing pages.

### Features to add in the future.

- Rating system, For all users to rate comic entries so they can be ranked by rating/popularity.
- Live chat, For users to communicate with each other.
- Language options, To allow a broader range of users to the site.
- CAPTCHA to new/edit entry form and contact form, To reduce spam sent on the contact form and new comics that are added.
- A page that displays all current signed up users, where moderators can easily access the different users profile pages.


## Technologies used (Frameworks, Libraries, Languages and Programs used)

- [HTML5](https://en.wikipedia.org/wiki/HTML)
    - To structure the content on each page of the site.
- [CSS](https://en.wikipedia.org/wiki/CSS)
    - To style the site in order to make it more appealing to the user.
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
    - To initialise materialize functions and write custom functions to the site.
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language))
    - To write and handle back end functions for the site.
- [Jinja2](https://en.wikipedia.org/wiki/Jinja_(template_engine))
    - To help with creating the html pages through the site.
- [jQuery](https://en.wikipedia.org/wiki/JQuery)
    - Allows for easier DOM manipulation.
- [Materialize](https://materializecss.com/)
    - The site uses Materialize to help simplify the structure of the site and make it more responsive.
- [Flask](https://en.wikipedia.org/wiki/Flask_(web_framework))
    - Helps writing code in Python by importing functions such as render_template and flash etc.
- [Heroku](https://www.heroku.com/)
    - Used for deploying and managing the project.
- [MongoDB](https://www.mongodb.com/)
    - Used for managing and storing data sent from the site.
- [Balsamiq](https://balsamiq.com/)
    - Used to design the wireframe of the project during the design process.
- [GitHub](https://github.com/)
    - Used to store the projects code.
- [GitPod](https://www.gitpod.io/)
    - IDE used to build the site.
- [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
    - To secure a users log in password by creating a hash of the password.

## Testing

Testing can be found in [TESTING.md](https://github.com/bob134552/comics/blob/master/TESTING.md)

## Deployment

The project was developed using Gitpod IDE. It was committed and pushed to GitHub through the use of git using the functions in Gitpod.

It was then deployed on Heroku by connecting the GitHub repository to the Heroku app.

To deploy the app on Heroku, first clone the repository.

To Clone the repository:
1. Log into GitHub.
2. Install [Gitpod](https://www.gitpod.io/)
3. Select the [comics repository](https://github.com/bob134552/comics) from the list of repositories.
4. At the top of the page click the drop down button with "code". 

<img src="/static/images/dropdown-code.jpg" alt="code-button">

5. Copy the HTTPS link provided.
6. Open your IDE and change the current directory to the location where you want the cloned directory to be.
7. Type ```git clone``` and paste the copied HTTPS link after.

    Example:

    ```git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY```

8. Hit Enter and your clone of the repository will be made.

If any problems occur refer [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) for help.

To deploy on Heroku.

1. Log into Heroku.
2. Click on "New" button and "Create new app" on the drop down.
3. Write your apps name and select a region close to you.
4. From the app page select "Deploy" and connect to the GitHub cloned repository from before.
5. For the app to work there are a few settings required, Select the "Settings" tab.
6. Click Reveal Config Vars to show this.

<img src="/static/images/config-vars.jpg" alt="config-vars">

7. Once filled in you can then return to the "Deploy" tab and scroll to the bottom and click "Deploy branch".

Your app should be deployed and a link will be available to view it.

### Notes:
- You will need your own config vars.
- Secret key was generated from [here](https://randomkeygen.com/).
- Mongo URI can be found by clicking connect in your mongoDB cluster and will look like this:

        mongodb+srv://<username>:<password>@<clustername>.vv32m.mongodb.net/<dbname>?retryWrites=true&w=majority

- Your MongoDB database will require to be set up with 3 collections(books, users and favourites.)

## Credits

### Media

- Comic images and logo taken from searching on Google images.
- Each comic is user submission.

### Aknowledgements

- [This](https://stackoverflow.com/questions/52199280/how-to-set-jquery-ajax-post-data) post on StackOverflow for the suggestion of using async call to send data to backend without refreshing page.
- [This](https://www.geeksforgeeks.org/python-program-to-calculate-age-in-year/) article on how to work out age in python to enable the maturity filter.
- My wife for help in design and support.
- My mentor for the support through the project.