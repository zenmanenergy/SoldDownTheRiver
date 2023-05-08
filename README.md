# SoldDownTheRiver

This project is in conjunction with Norfolk State University. It is a database of enslaved people who have 
passed through Norfolk, Virginia. This system is being developed by students at Roadstead Montessori High School in Norfolk, Virginia.

The system contains two different codebases that work together. The first is the client interface that is written using: HTML, JS, CSS and Svelte. The second codebase is a server interface using Python and MySQL. All requests from the client interface through the server interface are done through fetch() commands pulling in JSON datasets from the python server.

Steps to get this installed
The exact version numbers listed below may not be overly important, but if you struggle to get the system working, try matching the version numbers with what is below.

On your development computer:
1.	Download and install NodeJS v18.14.2
	- Windows: https://nodejs.org/download/release/v18.14.2/node-v18.14.2-x64.msi
	- Mac: https://nodejs.org/download/release/v18.14.2/node-v18.14.2.pkg

2. Install npm  v8.7.0
In the command line run this:
```npm install -g npm@8.7.0```

	In the command terminal if you type in: node --version it should say v18.14.2
	In the command terminal if you type in: npm --version it should say 8.7.0 

3.	Install python v3.11.2
	- Windows: https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe
	- Mac: https://www.python.org/ftp/python/3.11.2/python-3.11.2-macos11.pkg

	In the command terminal if you type in: `npm --version` it should say 8.7.0 

4. install the latest version of pip `python.exe -m pip install --upgrade pip`

5. Install flask
	```
	cd ./Server
	pip install flask
	```

6. Install cors and pymysql
	```
	pip install flask-cors
	pip install pymysql
	pip install pytz
	```

7. Open two terminal windows in VS Code.
	In the first terminal window go to the /Client folder so do `cd Client` Then turn on the svelte development server with: `npm run dev`
	In the second terminal window go to the /Server folder so do: `cd Server` Then turn on the python development server with: `flask run --host=0.0.0.0 --port=80`
	

Once you have all of this code installed, 
you will need to:

1. Fork this repository (button in the upper right corner of this web page)

2. Clone this repository onto your laptop

3. Find an issue to work on (look at the issues link on this oage)

4. Work and test the issue on your laptop.

5. As you make changes to the code you will commit and push the code to your forked version of the code

6. Once the code is working correctly you will issue a pull request

7. I will accept or reject the changes, merging your code into the main codebase
