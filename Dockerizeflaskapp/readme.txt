This code demonstrates the simple working of flask app as docker containers.
1. Create a project directory
2. Inside this directory, create a Python file named app.py with the following code in app.py 
3. Create a requirements.txt file in the same directory to list the dependencies
4. Create a dockerfile, as mentioned in Dockerfile
5. Build the Docker Image
   docker build -t flask-app .
6. Run the Flask App in a Docker Container
   docker run -p 5000:5000 flask-app




