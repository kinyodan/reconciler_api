# Reconciler-api application ( FastApi application) 

A Fast API  application in Python .

## Preconditions:

- Python 3

## git clone or download as zip and  extract from zip file find folder named credrails 


### Install dependencies

 CD into the credrails_api directory and run
```
pip install -r requirements.txt;
```

### Run server

```
uvicorn app.main:app --reload
```

# ## Run test

 requires Pytest (inluded in requirements.txt);

 cd into application credrails folder and run;

```
pytest 
```

this will run the test_main.py file 

# ## You can generate larger csv files for testing the application.

When application server is up and runnig make a "Get" api call to </br>
"/genarate_test_csv_files" path an dit will generate test csvs files  </br> for source and target csv that are as large as you want  </br>
the  default is 10000 records  </br>and the files will be found inside the root folder in folder named "test_csv_files"





