# Backend_DynamicTests



## Docker
- Build the Docker container
- `docker build -t backend-dyntest .`
- Run the Docker container
- `docker run -it --rm --name capstone-backend-dyntest --network host backend-dyntest:latest`
- or
- `docker run -it --rm --name capstone-backend-dyntest --network host -v $PWD/downloads_folder:/app/downloads_folder:rw backend-dyntest:latest`
- access via `http://127.0.0.1:7077/`

## Access
- - Test GET request
    - GET `http://127.0.0.1:7077/`
    - `curl --request GET 'http://127.0.0.1:7077/'`
- Upload image request
    - POST `http://127.0.0.1:7077/upload_url` with url
    - `curl --location --request POST 'http://127.0.0.1:7077/upload_url' --form 'url=www.google.com'`
