# sdx-menu-v2
Little mobile-friendly flask-app to see daily food menus
## Running
`pip install flask`
`pip install simplecache`
`pip install flask_scss`

`./run_dev_server.sh`

## Running in Docker container
Build image:
`docker build -t sdxmenu .`
Run container:
`docker run -p 5000:5000 -it sdxmenu`
Application runs now in port 5000 and it is accessible also outside localhost