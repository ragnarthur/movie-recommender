# CineTop - Movie Recommendations

CineTop is a Flask web application that provides movie recommendations using the TMDb API. Users can filter movies by genre and year, and the application displays the top-rated movies based on the selected criteria.

## Features

- Movie recommendations based on genre and year
- Responsive design for various devices (mobile, tablet, desktop)
- Modern and elegant UI using Bootstrap
- Carousel display for movie recommendations
- Option to save favorite movies (future implementation)

## Screenshots

![Home Page](screenshots/home.jpeg)
![Recommendations Page](screenshots/recommendations.jpeg)   

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/cinetop.git
    cd cinetop
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**

    Create a `.env` file in the root directory and add your TMDb API key:
    ```env
    TMDB_API_KEY=your_tmdb_api_key
    ```

5. **Run the application**
    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

1. Open the application in your web browser.
2. Select a genre and/or year to filter the movie recommendations.
3. Click on "Get Recommendations" to see the top-rated movies based on your selection.
4. Use the carousel controls to navigate through the movie recommendations.
5. Click the "Save Favorites" button to save movies (future implementation).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
