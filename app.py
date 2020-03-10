from flask import Flask, request
import keywords_tools
app = Flask(__name__)

@app.route('/')
def all_file_names():
    scel_names = keywords_tools.getAllFileNames()
    return "\n".join(list(scel_names))

@app.route("/keywords", methods=['GET'])
def get_keywords():
    number = request.args.get('number', 3)
    print(number)
    keywords = keywords_tools.getKeywords(number)
    print(keywords)
    return ",".join(keywords)