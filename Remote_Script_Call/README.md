# How to run

### Build a new image based on lab1 image provided by the professor
docker build -t image_name .

### Run the server
docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp image_name python3.6 server.py