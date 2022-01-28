# *******to run python in docker
docker run -it python:3.9

# *******to build and execute a dockerfile in this directory to build the python image with pandas
docker build -t test:pandas .


# ******to run postgres in docker
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
postgres:13

# ******to run postgres in cli and start the pg database to write sql queries
pgcli -h localhost -p 5432 -u root -d ny_taxi

# *******get pgadmin using docker
docker run -it -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=root" -p 5050:80 dpage/pgadmin4

# ******we need to connect the pgadmin to the pg database created by putting the 2 containers into the same network connection
# stop all running docker container first

docker network create pg-network

docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13

docker run -it -e "PGADMIN_DEFAULT_EMAIL=admin@admin.com" -e "PGADMIN_DEFAULT_PASSWORD=root" -p 5050:80 --network=pg-network \
--name pgadmin dpage/pgadmin4

# to remove already created container in docker

docker ps -a

docker rm cranky_goldstine

# to link the database container to the pgadmin container
set name as preferred (Docker Localhost)
Go to connections (Set name as name of host as pg-database, username=root, password=root) and save.


# convert jupyter notebook file to script
jupyter nbconvert --to=script Import-Data.ipynb

# *******add it to a docker compose file
URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

# arg parameters to run the script
python ingest_data.py --username=root --password=root --host=localhost --port=5432 \
--db_name=ny_taxi --table_name=yellow_taxi_trips --url=${URL}

# ******edit the docker file to dockerize the pipeline (v001 = version 1)
docker build -t taxi_ingest_data:v002 .

# to run the docker file
URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
docker run -it --network=pg-network taxi_ingest_data:v002 --username=root --password=root --host=pg-database --port=5432 --db_name=ny_taxi --table_name=yellow_taxi_trips --url=${URL}

# Configure GCP to connect with local terminal

- Download the gcp sdk package
- Unzip the tar file for mac (tar xopf tarfile)
- cd into the google cloud sdk directory
- ./install.sh
- gcloud auth login
- select default account
- select default project from command prompt or enter the project ID if requested
- export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

# Refresh token, and verify authentication
- gcloud auth application-default login

Setup for Access
IAM Roles for Service account:

Go to the IAM section of IAM & Admin https://console.cloud.google.com/iam-admin/iam
Click the Edit principal icon for your service account.
Add these roles in addition to Viewer : Storage Admin + Storage Object Admin + BigQuery Admin
Enable these APIs for your project:

https://console.cloud.google.com/apis/library/iam.googleapis.com
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

{# Terraform
Set up terraform

- create and edit main.tf file
- create and edit variable.tf file
- terraform init
- terraform plan to pass in the required variables e.g project-ID from GCP project
- terraform apply
- Go to GCP console to check if google big query & Cloud Storage is created}

{# Setting Up GCP Environment on Google Cloud (Cloud VM + SSH Access)
 - Go to compute engine on the drop-down and select VM instances
 - Create SSH key to log in to instance (before creating instance)
 https://cloud.google.com/compute/docs/instances/connecting-advanced#provide-key}

{#Generate ssh key
https://cloud.google.com/compute/docs/connect/create-ssh-keys
cd .ssh/
ssh-keygen -t rsa -f ~/.ssh/gcp -C haykayGCP -b 2048
No passphrase (leave blank)
One private key created & One public key created & one publicAdd public key to google cloud
# Add generated ssh key
- https://cloud.google.com/compute/docs/connect/add-ssh-keys
- cat gcp.pub => copy key to SSH key on GCP
- Compute Engine->Setting->Metadata->SSH keys}

{Go to VM instances and create instance
Edit Name, Region, Machine Configuration & Boot Disk}

{Go to local terminal to connect VM to local machine via terminal
➜  .ssh git:(main) ✗ cd ~
➜  ~ git:(main) ✗ ssh -i ~/.ssh/gcp haykayGCP@34.76.7.158

Download Anaconda on VM
- wget (Anaconda linux download link) - to install python
- Click Enter to accept license terms and services
-}

{Create Config file to configure access to the ssh to the VM server
- Open new terminal
- cd .ssh/
- touch config
- Edit Config file below:
Host de-zoomcamp (Name of VM)
    HostName 34.76.7.158 (External IP of VM)
    User haykayGCP (Username of VM)
    IdentityFile /Users/haykay14/.ssh/gcp (Absolute path directory of the gcp private key connected to the VM)

➜  .ssh git:(main) ✗ cd ~
(To login to the gcp VM)
➜  ~ git:(main) ✗ ssh de-zoomcamp}

{# Download Docker
sudo apt-get update
sudo apt-get install docker.io
Try docker hello-world (Permissions denied)
https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
Logout and Log in to activate

# Install docker-compose
https://github.com/docker/compose/releases
(base) haykayGCP@de-zoomcamp:~$ mkdir bin
(base) haykayGCP@de-zoomcamp:~$ cd bin/
(base) haykayGCP@de-zoomcamp:~/bin$ wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose
(base) haykayGCP@de-zoomcamp:~/bin$ chmod +x docker-compose (this makes the docker compose executable)
cd ..
vi .bashrc (Add this variable to use the docker compose)
export PATH="${HOME}/bin:${PATH}"

(base) haykayGCP@de-zoomcamp:~$ source .bashrc ( To logout and login to activate the changes)
}

# Download VSCode
Install remote ssh extension on VSCode
Select the remote ssh available
Clone the Repository from github

