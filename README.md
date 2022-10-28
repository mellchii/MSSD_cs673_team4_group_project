# PSC - Project Support Center

## TEAM 4: TeamPSC

> This is a web application which serves as a Project Support Center under an academic setting. It allows registered users to post questions, tips, tutorial and other forms of help for student projects. Users can also vote on the relevance of Posts, search for Posts by title, tags or authors, make comments of Posts, and manage their accounts in the application.

[![team 4](https://img.shields.io/badge/CS673-TEAM%204-red)](https://github.com/BUMETCS673/team-project-cs673olf22team4)
[![Framework](https://img.shields.io/badge/Framework-Django-yellow)](https://www.djangoproject.com/)
[![Language](https://img.shields.io/badge/Language-Python-brightgreen)](https://www.python.org/)
[![Language](https://img.shields.io/badge/Language-JavaScript-brightgreen)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Language](https://img.shields.io/badge/Language-CSS-brightgreen)](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
[![Language](https://img.shields.io/badge/Language-HTML-brightgreen)](https://developer.mozilla.org/en-US/docs/Web/HTML)

![Alt text](static/Project%20Suppo.png)

## Requirements (Prerequisites)

Tools and packages required to successfully install this project:

- Python 3.3 and up [Install](https://www.python.org/downloads/)
- Github Desktop / Git Bash [Install](https://git-scm.com/downloads)

## Installation

Follow the steps below to install an instance of this project.

- **Step 1:** Clone the git repo (Open your teminal and navigate to the directory you wish to store the project and run the following command)
  - `git clone https://github.com/BUMETCS673/team-project-cs673olf22team4.git`
- **Step 2:** Navigate into the repository. Create a virtual environment and activate it as follows:
  - Install virtual environment `pip install virtualenv`
  - Make your virtual environment `virtualenv venv`
  - Activate your virtual environment as below:
    - For Linux/Unix OS: `source venv/Scripts/activate`
    - For Windows OS: `venv\Scripts\activate`
- **Step 3:** Install requirements
  - `pip install -r requirements.txt`
- **Step 4:** Migrate Database
  - `python manage.py migrate`
- **Step 5:** Create superuser for access to database admin (follow prompts to set username, password)
  - `python manage.py createsuperuser`
- **Step 6:** Run the local server
  - `python manage.py runserver`
- **Step 7:** Navigate to the link below in your browswe to see the output
  - `http://127.0.0.1:8000/`

## Screenshots

Snapshots of the Home Page showing Post feeds and the Post Details page are shown below.

![Home Page](static/Home%20Page.png)

![Post Detail](static/Post%20Details.png)

## Features

Some unique features of the application are listed below:

- Logged-in Users can place upvotes or downvotes on Posts to indicate relevance.
- Users can search Posts by tags, post title, post content, post category, or username.
- Logged-in Users can write comments on Posts under the comments section.
- Post feed can be filtered by clicking on tag buttons
- Key security features like strong password validation, prevention of external access to
  backend data, and reset/forget password functionality.

## Tech Stack / Built With

List of technology / frameworks / tools used in this project.

1. [Django](https://www.djangoproject.com/) - The Python-based web framework
2. [Bootstrap](https://getbootstrap.com/) - CSS framework directed at responsive, mobile-first front-end web development.
3. [jQuery](https://jquery.com/) - JavaScript library designed to simplify HTML DOM tree traversal and manipulation.

## ✍Authors

### **CS673OLF22P4:**

    Prashant Bhandari  – Leader/ QA Leader
    Gabriel Ako        – Requirement Leader
    Hui Wang           – Security Leader/ QA Leader
    Mike Blanchet      – Design and ImplementationLeader/ Configuration Leader
    Sean Shea          – Design and ImplementationLeader/ Configuration Leader
    Tiffany Yu         – Security Leader/ Requirement Leader

## Additional Information

Thanks to Professor `Yuting Zhang` and Team Facilitator `John Chandra` for valuable feedback and guidance throughout the CS 673 course. Your input has helped Team 4 put up a quality Project.

### License

#### MIT © Team PSC [Team 4]
