------Environment Setup ------
1. Install python and flask
2. Check the version of python 
3. Install all the required Library using - pip install <library name>


--------- Creating Lambdas and API gatewaty -------------
1. Created lambdas (create function - function name,runtime - python ,execution role - Labrole  --> create function 
                    code source  & test )
        Created 6 lambdas - 
        1. Login lambda - to handle Login
        2. register lambda - to handle registration
        3. subscribeDetails lambda - to  get all the subscription details from the table 
        4. Query details - to query the music tables based on the input parameters in the form 
        5. subscribe lambda - to store the subscribed item to the  subscription table
        6. unsubscribe  lambda - to remove the unsubscribe  item from the subscription table

2.  Created 6 API gateway for all the lamda functions and deleted it to Production and tested using Postman -
        1. login-API - https://quh3mswgoc.execute-api.us-east-1.amazonaws.com/Production/login
        2. register-API - https://p413wciux5.execute-api.us-east-1.amazonaws.com/production/register
        3. queryDetails-API - https://wgyhr8r646.execute-api.us-east-1.amazonaws.com/Production/queryDetails
        4. subscribedDetails-API - https://ly5157l3s3.execute-api.us-east-1.amazonaws.com/Production/subscribedDetails
        5. subscribe-API - https://p09wm42tc4.execute-api.us-east-1.amazonaws.com/Production/subscribe
        6. unsubscribe-API - https://me0x9678th.execute-api.us-east-1.amazonaws.com/Production/unsubscribe


-----------Run Commands Locally ---------
python task1.py
python task2.py
python main.py

---------- install gunicorn to run in virtual env ------
1. create a wsgi.py file and  run  main from this 
2. Create the requirements.txt file in the code
3. ssh -i /Users/shilpapatel/Desktop/labsuser.pem ubuntu@<ipV4 address from ec2 instance>
4. sudo apt install python3-pip
5. pip --version 
6. sudo apt install python3-pip
7. sudo apt-get update
8. pip install virtualenv
9. pip  install -r requirements.txt
10. pip install flask gunicorn
11. pip install Flask
12. python3 -m venv env
13. cd s3858297/
14. source env/bin/activate
15. mkdir ~/.aws
16. vim ~/.aws/credentials
17. gunicorn --bind 0.0.0.0:8080 wsgi:app  --daemon
18. ps -ef | grep gunicon
19. kill -9 <PID>

--------------Install nginX -------------
## Ref: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
sudo nano /etc/nginx/sites-available/s3858297
nginx --version
sudo apt-get install nginx
sudo systemctl status nginx
cat /etc/nginx/nginx.conf 
cd /etc/nginx/sites-enabled/
ls -l
cat /etc/nginx/sites-available/default
cd ..
vim /etc/nginx/sites-available/myproject
sudo vim /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
sudo nginx -t 
sudo systemctl restart nginx


-------- Stpes to runs the code in ec2 instance  --------
1. Start and Login to instance
```
ssh -i /Users/shilpapatel/Desktop/labsuser.pem ubuntu@52.23.204.135
```
2. Add AWS credentials to ~/.aws/credentials file and save the file
   ```
   nano ~/.aws/credentials
   ```
3. cd ~/s3858297/
4. source env/bin/activate  --- (vitual env)
5. gunicorn --bind 0.0.0.0:8080 wsgi:app  --daemon

6. To verify: see if you are getting 200 code
```
curl -I http://0.0.0.0:8080
```
7. sudo nano /etc/nginx/sites-available/myproject
8. Verify nginx configuration 
```
sudo nginx -t 
```
9. sudo systemctl restart nginx 
10. sudo tail -f /var/log/nginx/*
 



