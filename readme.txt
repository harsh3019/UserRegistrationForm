1.create virtual environment by using python -m  venv virtualenvironmentname
2.Then activate virtual environment by using venvname\Scripts\activate
3.Then install the packages we required for this project by using "pip install packagename" we can check previouse packagename
by using "pip list" command

4. For this we required :- FastAPI,SQLALCHEMY,Python-Dotenv,Pymysql ,uvicorn
5. by using pip install fastapi[all]  sqlalchemy pymysql  we can install this package at a time
6. For account of packgae install you can also use requirements.txt file using "pip freeze > requirements.txt"
7. Create a folder application where our main code will available
8. Create main.py file for testing if api in fastapi is working or not and write simple code to check it 
9. for running main.py now can go to application folder uisng cd and then run "fastapi dev main.py"
10.Create .env file containing configuration of database and Also contain Database URL string for connection
11.Create db.py for database configuration 
12. create models and schemas file for given tables 
13.Create a api folder where we write user_root.py routes which we call in main.py file using 
"app.include_router(userapi, prefix='/users', tags=['users'])"

14.now create crud opeation for image and other entry .we will use form module for crud operation 
15. Also use random module for generating random number 4 digit 

*********************************************************************************************************
