# Data-pirates-challenge

This project aims to solve the challenge of building a web scraper.

The application must collect zip code and location data, as well as assign a unique ID to each record.

# challenge details

- The application must fetch the data of two or more states directly from the web page.

- As the target system returns the information through the Cold Fusion Markup file, the solution adopted was a scraper.

![image](https://user-images.githubusercontent.com/12565936/163117711-a1504e57-7209-4f02-86f4-4388596c7bdf.png)

- The scraper scans the page tags and searches for the indicated elements.

- Once the desired element has been found, the information is stored in lists and later saved in files with the jsonl extension.

# Running the tests locally:
- First, clone the project to your local PC;
- After downloading, access the project's root directory using the IDE of your choice;
- Install all dependencies by running the command: `pip install -r requirements.txt`
- Assuming you have the python language installed, just run the command below;
- `python -m pytest`

<img src="https://user-images.githubusercontent.com/12565936/163117840-8c69ef43-5b13-472e-81cf-d167f36ae7c8.png" width="1200" height="200">

# Running project

- To run the application, run the command `python .\main.py` in the root directory.

- At the end of the execution, the files with the data will be saved in the root directory as shown below.

<img src="https://user-images.githubusercontent.com/12565936/163118647-2a1872a0-ed09-44c1-be6a-6b4b15e034de.png" width="500" height="500">

- File result example:

<img src="https://user-images.githubusercontent.com/12565936/164451921-dc081cd0-1eb5-4237-accc-d56dc8c5d741.png" width="500" height="300">

# PS
- Application has been developed and tested on a Windows PC
