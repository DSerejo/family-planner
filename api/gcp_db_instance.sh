#let's create a db instance using compute enginge free tier
#probably it is easier to install docker and run the db instance inside the virtual machine
#then we can use the db instance as a service
#the commands should include networking so that we can expose port 3306

# gcloud compute instances create instance-20240717-163651 \
#     --project=serene-smoke-429712-n5 \
#     --zone=us-west1-b \
#     --machine-type=e2-micro \
#     --network-interface=network-tier=STANDARD,stack-type=IPV4_ONLY,subnet=default \
#     --maintenance-policy=MIGRATE \
#     --provisioning-model=STANDARD \
#     --service-account=971229859505-compute@developer.gserviceaccount.com \
#     --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append \
#     --create-disk=auto-delete=yes,boot=yes,device-name=instance-20240717-163651,image=projects/cos-cloud/global/images/cos-stable-113-18244-85-54,mode=rw,size=10,type=projects/serene-smoke-429712-n5/zones/us-west1-b/diskTypes/pd-balanced \
#     --no-shielded-secure-boot \
#     --shielded-vtpm \
#     --shielded-integrity-monitoring \
#     --labels=goog-ec-src=vm_add-gcloud \
#     --tags=mysql-server \
#     --reservation-affinity=any

# Open port 3306 for MySQL
# gcloud compute firewall-rules create allow-mysql \
#     --allow tcp:3306 \
#     --source-ranges 0.0.0.0/0 \
#     --target-tags=mysql-server

# Connect to the instance and install Docker
# gcloud compute ssh family-planner-db --command "
    sudo docker run -d -p 3306:3306 --name mysql-db -e MYSQL_ROOT_PASSWORD=root -v mysql-db-volume:/var/lib/mysql --restart always mysql:8 
# "