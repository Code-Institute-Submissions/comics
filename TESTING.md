Expanded from [README.md](https://github.com/bob134552/comics/blob/master/README.md)

# Testing section

The site was tested on desktop using Google Chrome.
It was also tested on several devices: Samsung Galaxy S10+, iPhone 12, Samsung Tab A and iPhone 11.

[W3C CSS Validator](https://jigsaw.w3.org/css-validator/) was used to ensure there was no errors in style.css.  
[W3C HTML Validator](https://validator.w3.org/) was used to check for errors in all templates, any error left is due to jinja2 templating.  
[PEP8 online check](http://pep8online.com/) was used to check for errors in the code for app.py. 

### Manual Testing Based On User Stories.

#### New User

1. As a new visitor, I want to be able to navigate the site with ease.
    
    Desktop:  
    1. Clicking on each navigation link brings user to the respective page.  
    2. Clicking the site logo brings user to the Home page of the site.

    Mobile:  
    1. Clicking on the bars on the navigation bar brings up the links to the other pages in the site. Swiping left to right also
        brings up the links.  
    2. Clicking on the logo brings user to the Home page of the site.

2. As a new visitor, I want to be able to use the site before registering, 
   and still be able to use most features so that I make a informed decision on whether to sign up.  
   
   1. The user is able to click on both buy and the comic itself if they wish to know more about the comic.
   2. The Contact page is avialable for everyone to use.

3. As a new visitor, I want to be able to sign up easily and get started browsing.

    1. From the Home page there is a button available to bring the user to the registration page.
        Alternatively there is a navigation link to the registration page.

#### Returning User
1. As a returning user, I want to be able to favourite comics to know which ones I am interested in.

    1. Clicking on the heart at the bottom right of the comic image fills the heart.
    2. Returning to the Home page, favourited comics are remembered and display a filled heart.

2. As a returning user, I want to provide my own entries to the collection.

    1. After the user has logged in they are given the option to add more comics to the collection through a callout button
        or through the navigation bar link for New Comic.
    2. Clicking on either button or navigation link brings the user to the New Comic page which asks the user to fill in a form for 
        the details of the new comic.
    3. If a comic already exists the user will be notified and it will not be added.

3. As a returning user, I want to be able to edit my details should they change.

    1. From the profile page, clicking on the "Edit Profile" button brings the user to an editable form prefilled with their current details.
    2. Changing the details and clicking submit updates the users data in the database.
    3. From the profile page, clicking on the "Change Password" button brings the user to the change password page.
    4. The change password page requires the user to input their old password, and a new password twice, to confirm the change.

4. As a returning user, I want an easy to fill-in contact form, so I can contact the owner of the site for new ideas, or to help moderate the site.

    1. The contact page is available from the navigation bar.
    2. It is a simple form that asks for the users name, email, subject and message.
    3. Trying to send the message without filling all parts of the form informs the user that additional inputs are required.

#### Moderator

1. As a moderator, I want to be able to edit or delete other user posts should they contain anything inappropriate.

    1. When signed in as moderator the "Edit" and "Delete" buttons are available to the user even on comics they themselves did not submit.
    
2. As a moderator, I want to be able to give other users the moderator status should they be willing to help maintain the site.

    1. If a moderator goes on another users profile page, there is a "Mod Status" checkbox with a "Confirm" button to grant moderator status to the user.
    2. Unchecking the "Mod Status" checkbox will remove mod status from that user.

## Manual Testing of Elements and Features.

1. Call to Action button
    1. Clicking button when not signed in redirects user to Registration page.
    2. Clicking button when logged in redirects user to New Comic page.

2. Registration form
    1. If any inputs are incorrect or left empty the input will become underlined in red to notify the user.
    <img src="/static/images/testing/registration-form.jpg" alt="registration-form">
    The user will also be given helpful hints for some incorrect fields, like the password input.

    2. If the user tries to create a profile with a username that already exists, a flash message will notify them.
    <img src="/static/images/testing/registration-user.jpg">

3. Log In form
    1. If the username or password is input incorrectly the user is notified.
    <img src="/static/images/testing/login-test.jpg" alt="test-login">
    2. If both username and password are correct the user will be logged into their account.

4. Search bar
    1. The Search bar allows users to look for comics by name, author, genre or synopsis.
    2. If there is no match the user is notified that what they are searching for yields no results.
    <img src="/static/images/testing/no-results.jpg" alt="no-results">
    3. If a match is found the comic will be displayed.
    <img src="/static/images/testing/search.jpg" alt="result">

5. Navigation bar
    1. When in mobile view the navigation links are hidden and a sidenav is available to the user through the navbar toggler.  
    <img src="/static/images/testing/toggler1.jpg">   <img src="/static/images/testing/toggler2.jpg">  
    2. The links available are varied depending if user is logged in or not.  
    <img src="/static/images/testing/logged-out.jpg" alt="logged-out-links">  <img src="/static/images/testing/logged-in.jpg" alt="logged-in-links">

6. New Comic and edit entry form.
    1. The edit entry form is a prefilled version of the New Comic form.
    2. Attempting to submit if any inputs are blank will notify the user of missing data.
    3. Both the comic image and store link are required to be in http or https format.
    <img src="/static/images/testing/new-edit-form.jpg" alt="new/eidt-form">
    4. Cancelling from the Edit entry form returns users to the comic they were editting.

7. Edit Profile form
    1. Allows user to edit the details they provided at registration, except username and password.
    2. If there is an incorrect input, the user will be notified as that input is highlighted.
    3. Cancelling brings the user to their profile page.

8. Contact form
    1. The contact form requires the users name, email, subject and message in order to send the email.
    2. After a successful send the button is disabled until the email is sent. If the email is sent the user is notified with the text in the button changing 
        from "Submit" to "Sent!". Otherwise the text in the button changes to "Try again later" on a unsuccessful send.
    <img src="/static/images/testing/test-mail2.jpg" alt="contact-page">
    <img src="/static/images/testing/test-mail1.jpg" alt="received-mail">

### Problems and Bugs

- Intially on the registration and change details form, the datepicker input could accept any string. It was possible to type into the input by holding down the mouse after clicking on the datepicker,
    allowing the user to type into the input instead of the datepicker.

    <img src="/static/images/testing/datepicker.jpg" alt="datepicker-error">
    
    To prevent the user from being able to submit the form the following pattern was used:

        pattern="(?:((?:0[1-9]|1[0-9]|2[0-9])\/(?:0[1-9]|1[0-2])|(?:30)\/(?!02)(?:0[1-9]|1[0-2])|31\/(?:0[13578]|1[02]))\/(?:19|20)[0-9]{2})"
    This means that the input was required to be in the format dd/mm/yyyy and checked for leap years and months that had either 28, 29, 30 or 31 days in that month.
- The datapicker range doesn't allow the user to go past the current year but allows them to select any day of the current year as Date of Birth
    and accepts it on registration.
    <img src="/static/images/testing/date-regi.jpg" alt="date-range">
- Originally each favourite entry in the collection took the users _id and the comics name. This was changed to the user's username instead, as the _id wasn't able to compare with the user._id in jinja,
    causing the favourite button to not work.
- Jinja2 loop controls had to be added to allow the use of continue and break, to allow some templating logic to work.
- To prevent the page from refreshing every time a comic was favourited, custom JavaScript functions were written in script.js to allow for an asynchronous call to the favourites database without refreshing the page.
- Depending on a users connection speeds some images may take longer to load than others.