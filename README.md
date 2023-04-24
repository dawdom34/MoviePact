# MoviePact
MoviePact is a simple application that allows you to easily book a ticket for your favorite movie

## Features
- ### User authentication
  The application gives you the ability to log in and register new users, and it also allows you to change your password and reset your password if you forget it
  
  ![login](https://user-images.githubusercontent.com/79845962/233980562-6763ca83-b460-4173-a8d1-52ec598e5c62.jpg)
 
- ### Adding new movies
  The ability to add new films to the database and set the date and time of the screening
  
- ### Filtering shows by date
  
  ![home](https://user-images.githubusercontent.com/79845962/233985818-443f4193-6785-4620-8f17-a9c894cd2897.jpg)
  
- ### See the details of the seance

  ![details](https://user-images.githubusercontent.com/79845962/233986178-61ef42cb-78bc-4afe-9db5-0d5f65d668a4.jpg)
  
- ### Buy a ticket
  The user can buy a ticket after selecting the seats in advance. The payment system is not supported

  ![ticket_buy](https://user-images.githubusercontent.com/79845962/233986641-a2f2da80-159a-4270-8649-2124543322db.jpg)
  
- ### Users tickets
  The user can see all their tickets for upcoming movies, and can return the ticket if there is not less than 12 hours left to the screening.
  A qr code is generated for each ticket with the option of downloading it
  
  ![my_tickets](https://user-images.githubusercontent.com/79845962/233987130-030708ab-ec6e-4734-abe7-5268742dc60e.jpg)
  
- ### API
  The application has implemented RESTful api created with django rest framework. The API supports all the above-described functionalities
  
## Setup (Windows)
1. Create virtual environment and activate it. To do this open cmd and execute commands below
```bash
python -m venv name
```
- change the name to whatever you prefer
- Change library to created folder and activate your environment
```bash
Scripts\activate
```
2. Open git bash and clone this repository
```bash
git clone https://github.com/dawdom34/MoviePact.git
```
3. Change directory to MoviePact
4. Now is the time to install all required packages to run this app
```bash
pip install -r requirements.txt
```
5. Create migrations files
```bash
python manage.py makemigrations
```
6. Apply all migrations
```bash
python manage.py migrate
```
7. Create superuser
```bash
python manage.py createsuperuser
```
- After execute this command follow the instructions
8. For now your database is empty. Let's change that by adding some products to work with
- Make sure you're in MoviePact
- Run the command:
```bash
python manage.py runscript load_movies
```
- This command will generate database objects based on data from csv file
9. Run the development server
```bash
python manage.py runserver
```
- Once the server is hosted, head over to http://127.0.0.1:8000/
## Now you're ready to have fun with this app
