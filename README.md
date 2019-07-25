# Deploying a Flask Application to AWS Elastic Beanstalk

Clone the repository
```
git clone https://github.com/stahlmatias/aws-eb.git
```
Create and activate a virtual environment named venv:
```
~/aws-eb$ virtualenv venv
~$ source venv/bin/activate
(venv) ~/aws-eb$
```
Install Flask, SQLAlchemy, PyMySQL with `pip install`:
```
(venv)~/aws-eb$ pip install flask
(venv)~/aws-eb$ pip install flask-sqlalchemy
(venv)~/aws-eb$ pip install PyMySQL
```
Save the output from `pip freeze` to a file named `requirements.txt`.
```
(venv)~/aws-eb$ pip freeze > requirements.txt
```
Set up AWS Elastic Beanstalk Environment
```
(venv) aws-eb$ sudo pip install awsebcli --upgrade --user
(venv) aws-eb$ export PATH=~/.local/bin:$PATH
(venv) aws-eb$ eb init
(venv) aws-eb$ eb create eb-aws1
```
Configure a MySQL database in your Elastic Beanstalk Environment
1. Open the Elastic Beanstalk console.
2. Select the environment you just created.
3. Choose Datatabase and click Modidy.
4. In the Retention box choose Delete.
5. Click Apply.

Make sure the Availability is set to Low (One AZ). This will keep us in the Free Tier.

Go to your AWS console, RDS, and click on DB Instances. Copy the Endpoint string, this is the URL to your AWS DB.

Back to your code, modify `application.py` and paste the endpoint of your database.
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<db_user>:<db_password>@<endpoint>/<db_url>'
```
Modify the permissions on your DB
1. Open the RDS console.
2. Click Security Groups.
3. Edit Type CIDR/IP - Inbound
4. Modify who can access your DB. I let everyone access it (0.0.0.0).

Add tables to your DB instance

```
(venv) aws-eb$ python
>> from application import db
>> from application import Todos
>> db.create_all()
```
Run `application.py` with Python: 
```
(venv) aws-eb$ python application.py
```
Check the server log to see the output from your request. You can stop the web server and return to your virtual environment by typing `Ctrl+C`.

If you got debug output instead, fix the errors and make sure the application is running locally before configuring it for Elastic Beanstalk. 

You've added everything you need to deploy your application on Elastic Beanstalk. Your project directory should now look like this:
```
~/eb-aws/
|-- env
|-- application.py
|-- requirements.txt
```
The venv folder, however, is not required for the application to run on Elastic Beanstalk. When you deploy, Elastic Beanstalk creates a new virtual environment on the server instances and installs the libraries listed in `requirements.txt`. To minimize the size of the source bundle that you upload during deployment, add an `.ebignore` file that tells the EB CLI to leave out the virt folder.

Example 
```
~/eb-aws/.ebignore

venv
```
Deploy Your Site With the EB CLI

```
(venv) ~/eb-aws$ eb status
(venv) ~/eb-aws$ eb deploy
```
Cleanup

When you finish working with Elastic Beanstalk, you can terminate your environment. Elastic Beanstalk terminates all AWS resources associated with your environment, such as Amazon EC2 instances, database instances, load balancers, security groups, and alarms. 
```
(venv) ~/eb-aws$ eb terminate eb-aws1
```
