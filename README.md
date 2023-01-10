# Patchmatch flask demo

The demo introductory video is at this site:https://www.youtube.com/watch?v=47UOe0_-WE0

## Required software environment

python、mysql、nodejs

## startup

>Start by importing the data.sql file into MySQL.

data.sql is located at https://drive.google.com/file/d/1CX1lxH5SZ3NhGpolkuO-vgW-UzEeetFf/view , you need to download it first. Because of the visual interface I use with navicat, I am not clear how to import sql file into MySQL on the command line, you could search for this on the Internet. After a successful import, you can see some tables like all_cve, cve, etc.in the database, in the cve table, a data is deleted in advance, so you can use the model to try.

Also, due to different database Settings on your personal computer, you need to change the SQLALCHEMY_DATABASE_URI parameter in manage.py to adjust it to the corresponding database information on your computer.

> Second, prepare the environment required for python

The main libraries you need are listed in requirements.txt and it can be adjusted according to your computer configuration. You can use pip or conda to install them. For one-click installation, the pip command is as follows:

```python
activate (yourenv)#Enter the specified virtual environment on your computer
(yourenv)pip install -r requirements.txt
```

But I don't recommend it, because different computers have different configurations and may not be compatible with versions of these libraries.

> Then use the npm command to build the required front-end environment
```python
npm install
```
After using this command, nodejs automatically configures the environment based on the package.json file.

> After all environments are set up, you can run the following command to start the program.
```python
python manage.py #startup the back-end service

npm run dev#startup the front-end service
```

After startup, wait for the browser to open the website http://localhost:8080 automatically.

#### ps.

The above npm and python commands can be used only in the patchmatch-main path.

Since everyone's computer environment is different, using the above steps may not be able to properly launch the application, you can leave a comment on GitHub or ask for help on Stack Overflow.
