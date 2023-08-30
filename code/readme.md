# **Automation KSC Through KlAkOAPI**
***
![Picture](https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Kaspersky_logo.svg/1280px-Kaspersky_logo.svg.png)
> KlAkOAPI Python package presents a wrapper library for interacting Kaspersky Security Center server via KSC Open API. With this package calls to KSC server can be performed as calls for methods of provided classes. Params datatype is also represented as a class, along with methods for parsing, composing and re-composing its contents. KlAkOAPI package requires Python 3.6 and higher.
> 
**Note:** Python 3 must be installed on your system to execute these scripts.<br />
1. It is necessary to download all the files within this repository<br />
2. Must set up a Python virtual environment
```
python3 -m venv klakoapi-env
```
3. And then activate it
```
.\klakoapi-env\Scripts\activate
```
4. Utilized the previously created Python environment file, find yourself within an environment:
```
(klakoapi-env)
```
5. Subsequently, Install KlAkOAPI package and which already had the KlAkOAPI package installed.
```
(klakoapi-env) pip install KlAkOAPI.tar.gz
```
***
> The script is compatible with the same KSC server in one stack
>
## **Version 1.0**<br />
Currently featuring only one capability, with more features planned for the future<br />
1. Generate additional users by utilizing a CSV file<br />
```
python createUsers.py 
```
! Please adhere to the provided CSV format example within this repository. !<br />
!! Adding users in the next rows !!
JSON output example following script execution
From This:
![sampleData](.\images\sampleDataCSV.png)
To This:
```
[{
      "Row":2,
      "ID":20,
      "Status":"Username Lucas Successfull Added"
   },{
      "Row":3,
      "Status":"Username Sahar Already Exists"
   },{
      "Row":4,
      "Error":"User Samad Error Missing Password Special Characters"
   },{
      "Row":5,
      "Status":"userPassword is Missing"
   },{
      "Row":6,
      "Error":"User KAKAKA Must Password 8-16 Characters, No Spaces"
   }]
```
