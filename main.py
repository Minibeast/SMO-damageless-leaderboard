from flask import Flask, render_template
import generate

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("./index.html", return_list=generate.main())


@app.route("/json")
def json():
    return { "data": generate.main() }


if __name__ == '__main__':
    app.run(host="localhost", port=2096)
