# ZTM - Zippee Task Manager
## Requirements
1. Django
2. ProstreSQL
3. VS Code
4. PGAdmin4(Optional but recommended)
## Steps to run the project
1. Clone the reposirory.
2. Open it in VSCode.
3. Create a virtual environment(I am assuming the you have mac, for linux/windows command to create and activate virtual environments slightly differ, google them if don't know, it's quite easy.), using terminal from VS Code.
```bash
python3 -m venv .venv
```
4. Acticate it from the terminal and use cmd+shift+P to select it as your default interpreter.
```bash
source .venv/bin/activate
```
5. Run this command to install requirements.
```bash
pip install -r requiremnts.txt
```
6. Create a .env file, have a look at .env.example file for the reference, you need to have all the values for the keys mentioned in .env.example, eg. in .env you might have DEBUG_FLAG=False
7. Run below command in terminal to cretae SECRET_KEY for you project and paste it's value in .env file.
```bash
python3 -c 'import secrets, string; alphabet = string.ascii_letters + string.digits + "@%^&*(-_=+)"; print("".join(secrets.choice(alphabet) for i in range(50)))'
```
8. Use this in .env for running you app locally.
```bash
ALLOWED_HOSTS=127.0.0.1
```
9. Make sure you have a newly cretaed databse and a user that has read/write access to this database, in my case, I had these creds for my database running locally, you can have yours.
- DB_NAME=ztm_db
- DB_USER=ztm_user
- DB_PASSWORD=ztm@007
- DB_HOST=localhost
- DB_PORT=5432
10. Create and run migraitons in VS Code terminal
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
11. Create superuser for for accessing djnago's built-in admin panel
```bash
python manage.py createsuperuser
```
12. Add values for ACCESS_TOKEN_LIFETIME_MINS and REFRESH_TOKEN_LIFETIME_HOURS, it is recommened to have their values as 5 and 24 respectively.
13. In production you need to collect staticfiles, but in developemnt mode you don't need to do so. Admin panel should now be visible at this address, (use the username and password you entered during superuser creation in terminal).
[http://127.0.0.1:8000/admin/]
14. You can access your API documentation at this address.
[http://127.0.0.1:8000/api/schema/swagger-ui/#/]

### Commands to run tests
- Run these commands to run the tests
```bash
pytest
```
```bash
pytest -v
```
```bash
pytest --cov=apps
```

### Wanna have a look how RABC works? Switch to monolith_rbac branch and proceed as follows.
1. Apart from a super user that you created earlier, you need to have 2 more users.
2. Visit admin panel and under user section make one of these 2 users staff by making is_staff=True.
3. Now we have 3 types of users in our system.
    - The Super User - Most privilleged user, can perform any action facilitated by the system.
    - The Admin - can read other user's data, and update only his own.
    - The User - can raed and update only his own data.