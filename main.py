from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", result="")

@app.route("/process", methods=["POST"])
def process():
    text = request.form.get("input_text", "")
    result = f"受け取ったテキスト: {text}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
