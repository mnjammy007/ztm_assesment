# ZTM - Zippee Task Manager
## Requirements
1. Django
2. ProstreSQL
3. VS Code
## Steps to run the project
1. Create a folder named ztm_assesment
2. Open the folder in VSCode.
3. Create a virtual environment(I am assuming the you have mac, for linux/windows command to create and activate virtual environments slightly differ, google them if don't know, it's quite easy.), using terminal from VS Code.
```python3 -m venv .venv```
4. Acticate it from the terminal and use cmd+shift+P to select it as your default interpreter.
```source .venv/bin/activate```
5. Run this command to install requirements.
```pip install -r requiremnts.txt```
6. Create a .env file, have a look at .env.example file for the reference, you need to have all the values for the keys mentioned in .env.example, eg. in .env you might have DEBUG=True
7. Run below command in terminal to cretae SECRET_KEY for you project and paste it's value in .env file.
```python3 -c 'import secrets, string; alphabet = string.ascii_letters + string.digits + "@%^&*(-_=+)"; print("".join(secrets.choice(alphabet) for i in range(50)))'```
8. Use this in .env for running you app locally.
```ALLOWED_HOSTS=127.0.0.1,localhost```
9. Make sure you have a newly cretaed databse and a user that has read/write access to this database, in my case, I had this for my database running locally, you can have yours.
>DB_NAME=ztm_db
>DB_USER=ztm_dev
>DB_PASSWORD=ztm@007
>DB_HOST=localhost
>DB_PORT=5432