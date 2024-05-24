document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    const genre = document.getElementById('genre').value;
    if (!genre) {
        event.preventDefault();
        document.getElementById('alert').classList.remove('d-none');
    }
});
