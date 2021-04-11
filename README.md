# Timeular Pomodoro

Timeular Pomodoro allows you to set end times to any of your Timeular activities. When you are tracking an activity, your activity will automatically end based on the length you have set. 

## Prerequisites
1. A Timeular account at https://timeular.com. This should work with any subscription.
2. An API key defined in your Timeular profile. You can set this at https://profile.timeular.com/#/app/account. You will use the API Key and API secret created in your profile when you create your .env file below, so be sure to save these values somewhere _safe_, like a password manager (_hint hint_)

## Installation
1. Clone this repository
2. cd to your repository folder
3. Create a file named .env
4. In your .env file, define the following variables.
   
```
API_KEY=3sLznaE3ZG7B66UZ1NE68ytlwYViJH0F6BeQaLlHHUIkF7IZ9lh3
API_SECRET=6CvZBr55kR5mlNgb7inF9KtGYHSqewIepgcaJ9S3S5H=
API_ACTIVITIES=[{"name":"Break", "time":"6"},{"name":"Lunch", "time":"31"}]
```
5. Set your local docker instance to run Linux containers
6. Run the docker-compose.yml file using the following command:
7. In your local Timeular settings, go to Reminders and Emails, and uncheck "Reminder Long Time Entries".
```
    docker-compose up
```

## Usage Example
I typically like to set my time as 25 minutes of Dev Work and 5 minutes of Break. I also typically take a 1/2 hour lunch at some point during the day.
For this setup, my .env file would look like:
```
API_KEY=3sLznaE3ZG7B66UZ1NE68ytlwYViJH0F6BeQaLlHHUIkF7IZ9lh3
API_SECRET=6CvZBr55kR5mlNgb7inF9KtGYHSqewIepgcaJ9S3S5H=
API_ACTIVITIES=[{"name":"Break", "time":"6"},{"name":"Lunch", "time":"31"},{"name":"Dev Work", "time":"26"}]
```
_Note that each of my items is one more minute than desired_

## Release History
* 0.0.1 Initial work

## Meta

Bruce Parr
Twitter - [@bruber4151](https://twitter.com/bruber4151) 
LinkedIn - [linkedin.com/in/bruceparr](linkedin.com/in/bruceparr)

Distributed under the GPL-3.0 license. See ``LICENSE`` for more information

[https://github.com/bp4151/github-link](https://github.com/dbader/)
