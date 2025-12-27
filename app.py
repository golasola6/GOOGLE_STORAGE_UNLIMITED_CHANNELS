from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'LazyDeveloper@Koyeb-server-Testing-done-✅'


if __name__ == "__main__":
    app.run()

