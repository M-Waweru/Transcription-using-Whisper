from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from an environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the home page route
@app.route("/")
def index():
    return render_template("index.html")

# Define the route for handling file uploads
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["audio"]
    filename = file.filename
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    # with open(filepath, "rb") as f:
    #     audio = f.read()

    audio = open(filepath, "rb")
    transcript = openai.Audio.transcribe(model="whisper-1", file=audio, result_format="text", prompt="In English, transcribe the recording on AI, consciousness and humanity")

    print(transcript)

    text = transcript.text

    print(text)

    # Save the transcribed text to a file
    with open(f"transcripts/{filename}.txt", "w") as f:
        f.write(text)

    # Return a download link to the transcribed text file
    return f'<a href="transcripts/{filename}" download>Download Transcription</a>'

if __name__ == "__main__":
    app.run(debug=True)