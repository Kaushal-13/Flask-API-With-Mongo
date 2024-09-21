
# Flask API with MongoDB and Rate Limiting

This project is a simple REST API built using Flask and MongoDB (Atlas or local), with functionality to manage user data. The API includes rate limiting, pagination, and validation using `marshmallow`. 

## Features
- **CRUD Operations**: Add, retrieve, update, and delete users.
- **Rate Limiting**: Limits requests to protect the API from abuse.
- **Pagination**: Retrieve users in paginated form.
- **Input Validation**: Ensures proper user data format using `marshmallow`.
- **MongoDB**: Stores user data in MongoDB.

## Requirements

Make sure you have the following installed on your machine:

- **Python 3.x**
- **Flask**: A web framework for building the API.
- **MongoDB**: Either a local MongoDB instance or a MongoDB Atlas cluster.
- **Docker**: (Optional) You can use Docker to containerize the app.
- **Other Libraries**: Specified in `requirements.txt`

## Setup Instructions

### 1. Clone the repository
```bash
git clone git@github.com:Kaushal-13/Flask-API-With-Mongo.git
cd your-repo
```

### 2. Install dependencies
First, create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root of your project and add the following:
```
MONGO_URI=mongodb://localhost:27017/mydatabase  # or your MongoDB Atlas connection string
```

### 4. Run the Flask API
To start the Flask application, simply run:
```bash
python app.py
```

The API will now be available at `http://127.0.0.1:5000`.

### 5. Using Docker (Optional)
### Docker Setup

To run the project using Docker, you need to have Docker and Docker Compose installed on your machine.

#### Build and Run the Docker Container

To start your Flask application in a Docker container, follow these steps:

1. **Create a `.env` file** in the root directory (if you haven't done so already) and add your MongoDB connection string:
    ```
    MONGO_URI=mongodb://localhost:27017/mydatabase  # or your MongoDB Atlas connection string
    ```

2. **Run Docker Compose**:
   In the root of your project, execute:
   ```bash
   docker-compose up --build


The application should now be accessible at `http://localhost:5000`.

## API Endpoints

### GET /
- **Description**: Welcome route.
- **Response**: `200 OK`
```json
{
  "message": "MongoDB Atlas + Flask API"
}
```

### GET /users
- **Description**: Get paginated list of users.
- **Query Params**: 
  - `page` (optional): Page number (default 1)
  - `limit` (optional): Number of users per page (default 10)
- **Rate Limit**: 5 requests per minute.
- **Response**: `200 OK`
```json
{
  "users": [...],
  "total_users": 100,
  "page": 1,
  "total_pages": 10
}
```

### GET /users/<int:id>
- **Description**: Get a single user by ID.
- **Response**: `200 OK` if the user exists, or `404 Not Found` if the user does not exist.
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### POST /users
- **Description**: Add a new user.
- **Body**: JSON object with `id`, `name`, `email`, `password`.
- **Response**: `201 Created` if successful, or `400 Bad Request` for validation errors.
```json
{
  "message": "Document added",
  "id": "60b6cdd8e4b0d430544a6a1b"
}
```

### PUT /users/<int:id>
- **Description**: Update an existing user by ID.
- **Body**: JSON object with user fields to update.
- **Response**: `200 OK` if successful, or `400 Bad Request` for validation errors.
```json
{
  "message": "USER updated successfully"
}
```

### DELETE /delete/<int:id>
- **Description**: Delete a user by ID.
- **Response**: `200 OK` if the user is successfully deleted, or `404 Not Found` if the user does not exist.
```json
{
  "message": "Document deleted successfully"
}
```

## Rate Limiting

This API applies rate limiting with a limit of **5 requests per minute** per IP address. If the rate limit is exceeded, the following response is returned:
```json
{
  "error": "rate limit exceeded",
  "description": "429 Too Many Requests: Rate limit exceeded."
}
```

## Error Handling
- **400 Bad Request**: Returned for validation errors or missing/invalid parameters.
- **404 Not Found**: Returned if a resource (like a user) is not found.
- **429 Too Many Requests**: Returned when the rate limit is exceeded.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
