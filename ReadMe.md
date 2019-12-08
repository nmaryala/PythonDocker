## Run the following instructions for hosting server container
1. Building Image: sudo docker build -t python-classify .
2. Running Image: sudo docker run python-classify
3. Getting docker instance ID: sudo docker ps -a
4. Getting IP Address: sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'  <InstanceId>
5. Sending image request to container: curl -F "file=@persian.jpg" http://172.17.0.2:5000/upload
