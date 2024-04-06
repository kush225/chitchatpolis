# ChitChatPolis

Description of your project.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kush225/chitchatpolis
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

1. Run migrations:

```bash
python manage.py migrate
```

2. Start the development server:

```bash
python manage.py runserver
```

### Using Docker

1. Build the Docker image:

```bash
docker build -t chitchatpolis:v1 .
```

2. Run the Docker container:

```bash
docker run -d -p 8000:8000  chitchatpolis:v1
```

### Using Docker Compose

1. Start the Docker Compose services:

```bash
docker-compose up -d
```

## Testing

1. Install Postman (if not already installed).
2. Import the Postman collection `Chitchatpolis.postman_collection.json` located in the root directory.
3. Run the imported collection to test the endpoints.
