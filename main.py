from senryu import Senryu, SenryuImageOption, create_image
from image_process import save_image, image_base64_encode
from flask import Flask, request, send_file
import tempfile
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    if not request.args.get("first_sentence") or not request.args.get("second_sentence") or not request.args.get("third_sentence") or not request.args.get("author_name"):
        return "Missing parameters"

    first_sentence=request.args.get("first_sentence")
    second_sentence=request.args.get("second_sentence")
    third_sentence=request.args.get("third_sentence")
    author_name=request.args.get("author_name")

    senryu = Senryu(
        first_sentence=first_sentence,
        second_sentence=second_sentence,
        third_sentence=third_sentence,
        author_name=author_name
    )

    option = SenryuImageOption(
        service_name="",
        service_name_font_size=30.0
    )

    img = create_image(senryu, option)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_path = temp_file.name
        save_image(img, temp_path)

    return send_file(
        temp_path,
        mimetype="image/png",
        as_attachment=False
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
