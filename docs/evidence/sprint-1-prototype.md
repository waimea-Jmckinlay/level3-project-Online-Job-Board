# Sprint 1 - Developing a DB and UI Prototype


## Sprint Goals

Develop a design for the database and a UI prototype that simulates the key functionality of the system. Test and refine the UI so that it can serve as the model for the next phase of development in Sprint 2.

### Specific Goals

**Edit these goals as needed**

- Design the database:
    - Tables
    - Fields / types
    - Primary keys
    - Default / nullable values
    - Relationships (foreign keys)
- Design the UI
    - Key pages
    - User interactions and 'flow'
    - Page layouts / features
    - Colour palette
    - Etc.


## Initial Database Design

Replace this text with notes regarding the DB design.

![DB Design](screenshots/draw-sql.png)


### Required Data Input

when the user makes an account they will input their name the pasword (only hash pasword storded) their rough location 
and contact information. once job is done the user will be rated by the job owner on porformants 

### Required Data Output

the user information will be displayed but only for job owners and the other way around if they accpted each other e.g location and contact-info but before that the owner 
can see the user rating to deside if he wants this user for his job and his own rating is displayed on the job he posted 

### Required Data Processing

when processing the password we will hash it and add a salt so we aren't storing the password but the hash of one for 
safety reasions  


## UI 'Flow'

The first stage of prototyping was to explore how the UI might 'flow' between states, based on the required functionality.

This penport demo shows the initial design for the UI 'flow':

https://design.penpot.app/#/view?file-id=f0485fb1-4e63-8165-8008-3908e675a64e&page-id=f0485fb1-4e63-8165-8008-3908e675a64f&section=interactions&frame-id=0013c019-5066-804b-8008-39090ca72598&index=0&share-id=6956fb43-d0b4-807f-8008-4215d766031a

### Testing

I had one of my class friends move around and use what was their at the time  

### Changes / Improvements

I made changes as they played around with it as not all conections where conected so i fixed that

https://design.penpot.app/#/view?file-id=f0485fb1-4e63-8165-8008-3908e675a64e&page-id=f0485fb1-4e63-8165-8008-3908e675a64f&section=interactions&frame-id=0013c019-5066-804b-8008-39090ca72598&index=0&share-id=6956fb43-d0b4-807f-8008-4215d766031a



## Initial UI Prototype

The next stage of prototyping was to develop the layout for each screen of the UI.

This Figma demo shows the initial layout design for the UI:

https://design.penpot.app/#/view?file-id=a234c67f-eb39-8116-8008-3f6d0a90e616&page-id=f0485fb1-4e63-8165-8008-3908e675a64f&section=interactions&frame-id=0013c019-5066-804b-8008-39090ca72598&index=0&share-id=6956fb43-d0b4-807f-8008-4220bc76509d

### Testing

for the testing i had a different user to test / play with it to make sure the layout is good and working

### Changes / Improvements

while testing the user recmend i had a feature where we could also deny users that apply for the job to shorten the list so i did that before I 
added the link above so you can see it their if you go you your job post I also found i made a pontless page that I remove being the contact infomation 
page once accpting a user to do the job as yu could just see their information by clicking oin their account

https://design.penpot.app/#/view?file-id=a234c67f-eb39-8116-8008-3f6d0a90e616&page-id=f0485fb1-4e63-8165-8008-3908e675a64f&section=interactions&index=0&share-id=6956fb43-d0b4-807f-8008-4220bc76509d


## Refined UI Prototype

Having established the layout of the UI screens, the prototype was refined visually, in terms of colour, fonts, etc.

This Figma demo shows the UI with refinements applied:  

https://design.penpot.app/#/view?file-id=6956fb43-d0b4-807f-8008-4222f81ef218&page-id=f0485fb1-4e63-8165-8008-3908e675a64f&section=interactions&frame-id=0013c019-5066-804b-8008-39090ca72598&index=0&share-id=83dd9eca-2062-81d6-8008-5a78cc756210

### Testing

to test myself and a tester went though the prototype and descuss issuses and things

### Changes / Improvements

while creating this prototype I relize I missed a few things from the other prototype which nor me or my testeder relizes 
I never made the page that lets the job owner user give a rating to the other user so i made that page and a way to and back from it but 
giving a rating by comniting on how well the user did the job.

*FIGMA IMPROVED REFINED PROTOTYPE - PLACE THE FIGMA EMBED CODE HERE - MAKE SURE IT IS SET SO THAT EVERYONE CAN ACCESS IT*


## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

