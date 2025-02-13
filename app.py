# -*- coding: utf-8 -*-


from flask import Flask, render_template, request
from textSimilarity import get_text_similarity  # Import the similarity calculation function

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """
    Home route to render the main page with the text comparison form.
    """
    return render_template('index.html')

@app.route("/getSimilarity", methods=['POST'])
def get_similarity():
    """
    Route to handle form submission and calculate text similarity.
    """
    if request.method == 'POST':
        # Collect the texts from the form (only 2 texts now)
        texts = [
            request.form['text1'],
            request.form['text2']
        ]

        # Get the selected similarity method from the form
        method = request.form['similarity_method']

        # Check if stopwords should be excluded
        stopwords = False
        if 'stopwords' in request.form and request.form['stopwords'] == "yes":
            stopwords = True

        # Check if punctuation should be excluded
        punct = False
        if 'punctuation' in request.form and request.form['punctuation'] == "yes":
            punct = True

        # Calculate the similarity matrix using the imported function
        sim_matrix = get_text_similarity(texts, method, exclude_stopwords=stopwords, exclude_punctuation=punct)

        # Handle invalid input or calculation errors
        if sim_matrix is None:
            return render_template('index.html', prediction_texts="Sorry, please enter valid input!")
        else:
            # Render the result page with the similarity score
            return render_template(
                'index.html',
                similarity_score=f"{sim_matrix[0][1]:.4f}"  # Only one similarity score for 2 texts
            )
    else:
        # If the request method is not POST, render the form again
        return render_template('index.html')

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)  # Enable debug mode for development