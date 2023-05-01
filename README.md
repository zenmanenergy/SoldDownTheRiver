# SoldDownTheRiver

This project is in conjunction with Norfolk State University. It is a database of enslaved people who have 
passed through Norfolk, Virginia. This system is being developed by students at Roadstead Montessori High School in Norfolk, Virginia.

Steps to get this installed

On the server side:
1) Download and install NodeJS v18.14.2 
Windows) https://nodejs.org/download/release/v18.14.2/node-v18.14.2-x64.msi
Mac) https://nodejs.org/download/release/v18.14.2/node-v18.14.2.pkg

2) Install npm  v8.7.0
In the command line run this:
```npm install -g npm@8.7.0```

In the command terminal if you type in: node --version it should say v18.14.2
In the command terminal if you type in: npm --version it should say 8.7.0 

3) Install python v3.11.2
Windows) https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe
Mac) https://www.python.org/ftp/python/3.11.2/python-3.11.2-macos11.pkg

In the command terminal if you type in: npm --version it should say 8.7.0 

4) install the latest version of pip
```python.exe -m pip install --upgrade pip```

5) Install flask
```
cd ./Server
pip install flask
```

6) install cors and pymysql
```
pip install flask-cors
pip install pymysql
```

7) Create a user named ```developer``` with the password ```developer```

8) Open two terminal windows in VS Code. in the first window go to the /Client folder so do ```cd Client``` Then turn on the svelte development server with: ```npm run dev```
In the second terminal window in VS code go to the /Server folder so do: ```cd Server``` Then turn on the python development server with: ```flask run --host=0.0.0.0 --port=```
