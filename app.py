from flask import Flask, render_template, request, send_from_directory, url_for
import os
import qrcode

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
QR_FOLDER = "static/qr"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        return "No file selected."

    file = request.files["file"]

    if file.filename == "":
        return "Please choose a file."

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    # Link to open the uploaded file
    file_link = request.host_url + "file/" + filename

    # Generate QR Code
    qr = qrcode.make(file_link)

    qr_path = os.path.join(QR_FOLDER, "qr.png")
    qr.save(qr_path)

    return render_template(
        "result.html",
        filename=filename,
        file_link=file_link
    )


@app.route("/file/<filename>")
def file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)