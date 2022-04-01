# Postuino
Real-time slouch detection using posture estimation. Get insights on your sitting patterns. Ideal for students and workplace setup.

## How to Run?
Clone the repository and navigate to the project directory
```
git clone https://github.com/mohilkhare1708/postuino.git
cd postuino
```
Create a virtual environment and install the dependencies
```
python3 -m venv venv
venv\Scripts\activate.bat OR source venv/bin/activate (for Linux devices)
pip install -r requirements.txt
```
Perform the migrations
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Create the superuser account
```
python3 manage.py createsuperuser
```
Run the server
```
python3 manage.py runserver
```

## How to Contribute?
Please fork the repository, create a new branch, commit your changes to it and issue a pull request.

## Credits and Team
We hope that we create a difference in the world with our approach towards hardware-free posture correction.

Developed by Mohil Khare, Prasuk Jain, Harsh Katkade
