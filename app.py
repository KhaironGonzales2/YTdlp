from flask import Flask, render_template, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")
    as_mp3 = data.get("mp3", False)

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")
        cmd = ["yt-dlp", url, "-o", output_path, "--cookies", "cookies.txt"]

        if as_mp3:
            cmd += ["-x", "--audio-format", "mp3"]

        try:
            subprocess.run(cmd, check=True)
            return jsonify({"message": "Download started"})
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Download failed", "details": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render sets the PORT variable
    app.run(host="0.0.0.0", port=port)

