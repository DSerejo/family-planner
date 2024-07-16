# Family Planner and Tracker App - API


## Getting Started

### Prerequisites
- Python 3.8+
- Docker (optional, for containerization)

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd family-planner-tracker/api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    cp .env.example .env
    ```

### Running the App

1. Start the application:
    ```bash
    python app/main.py
    ```

2. (Optional) Run with Docker:
    ```bash
    docker-compose up --build
    ```

### Running Tests

1. Run the tests:
    ```bash
    pytest
    ```

## Contributing
Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.