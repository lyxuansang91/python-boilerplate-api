# FastAPI Project - Backend

## Requirements

* [Docker](https://www.docker.com/)
* [poetry](https://python-poetry.org/) for Python package and environment management

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/lyxuansang91/python-boilerplate-api.git
    cd python-boilerplate-api
    ```

2. Install dependencies using poetry:
    ```sh
    poetry install
    ```

3. Start the application using Docker:
    ```sh
    docker-compose up --build
    ```

## Running the Application

After starting the application, you can access the API documentation at:
```
http://localhost:8000/docs
```

## Running Tests

To run tests, use the following command:
```sh
poetry run pytest
```

## Project Structure

```
python-boilerplate-api/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── ...
├── tests/
│   ├── ...
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

