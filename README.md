# Song Summary API

An intelligent API that fetches song lyrics, summarizes them, and extracts countries mentioned within the lyrics. Powered by Django, Musixmatch API, and OpenAI GPT.

## Features
- Fetch lyrics based on artist and title.
- Summarize song lyrics in one sentence.
- Extract countries mentioned within the lyrics.
- Robust error handling and logging.

## Getting Started

### Prerequisites
- Python 3.11+
- Poetry (Dependency Management)
- Git (Version Control)
- API keys for:
  - Musixmatch: [Get your API key](https://developer.musixmatch.com/)
  - OpenAI: [Get your API key](https://platform.openai.com/signup/)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/username/song_summary.git
    cd song_summary
    ```

2. **Install Poetry if not already installed:**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. **Install dependencies:**
    ```bash
    poetry install
    ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
    ```env
    MUSIXMATCH_API_KEY=your_musixmatch_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run database migrations:**
    ```bash
    poetry run python manage.py migrate
    ```

6. **Start the development server:**
    ```bash
    poetry run python manage.py runserver
    ```
    Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### Add a Song

**POST** `/songs/add/`

- **Request Body:**
    ```json
    {
      "artist_name": "Adele",
      "song_title": "Hello"
    }
    ```
- **Response:**
    ```json
    {
      "id": 1,
      "artist_name": "Adele",
      "song_title": "Hello",
      "lyrics": "Hello, it's me, I was wondering...",
      "summary": "A heartfelt message about longing.",
      "countries": "USA, Canada"
    }
    ```

## Testing

1. **Run unit tests:**
    ```bash
    poetry run pytest
    ```

2. **Run tests with coverage:**
    ```bash
    poetry run pytest --cov=app --cov-report=html
    ```

3. **View the coverage report:**
   Open `htmlcov/index.html` in your browser.

## Deployment

### Deploy to Heroku

1. **Install Heroku CLI:**
    ```bash
    brew tap heroku/brew && brew install heroku
    ```

2. **Create a Heroku app:**
    ```bash
    heroku create
    ```

3. **Push to Heroku:**
    ```bash
    git push heroku main
    ```

4. **Set environment variables:**
    ```bash
    heroku config:set MUSIXMATCH_API_KEY=your_key
    heroku config:set OPENAI_API_KEY=your_key
    ```

5. **Open your app:**
    ```bash
    heroku open
    ```

## Project Structure

```plaintext
song_summary/
├── app/
│   ├── models.py
│   ├── utils.py
│   ├── serializers.py
│   ├── views.py
├── manage.py
├── tests/
│   ├── test_utils.py
├── .env
├── pyproject.toml
├── README.md
```

## License

This project is licensed under the MIT License.

## Feedback

Contributions, feedback, and suggestions are welcome. Open an issue or create a pull request to contribute!