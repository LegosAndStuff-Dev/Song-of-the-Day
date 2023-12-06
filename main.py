from flask import Flask, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"Hello World": "Hello"}
    
api.add_resource(HelloWorld, "/hello")

@app.route("/")
@app.route("/home")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="192.168.4.44")
