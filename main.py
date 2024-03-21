from flask import Flask, request, jsonify
from PIL import Image
from flask_cors import CORS
from math import ceil
import io

app = Flask(__name__)

CORS(app)

@app.route("/compress/image/banner", methods = ["POST"])
def compress():
  if request.method == "POST":
    if 'file' not in request.files:
      print("Couldn't resolve file...!?")
      return jsonify({"message": "file not found"})
    try:
      file = request.files['file']
      img = Image.open(file)
      factor = 1.05
      resizedImg = img
      width, height = resizedImg.size

      maxSide = max(width, height)

      while maxSide > 1000:
        width, height = resizedImg.size
        maxSide = max(width, height)
        resizedImg = resizedImg.resize((int(width//factor), int(height//factor)))

      buffered = io.BytesIO()
      resizedImg.save(buffered, format="jpeg", quality=70)
      print("final filesize:", ceil(buffered.tell()/1024), "kb")
      print(buffered.getvalue())
      compImg = Image.open(buffered)

      compImg.save("compressed-" + file.filename)
      
      response = jsonify({"message": "Done"})
      print("Compressed Successfully : )")
      return response, 200
    
    except RuntimeError as e:
      response = jsonify({"message": "Something went wrong!"})
      return response, 500
  else:
      response = jsonify({"message": "Expected a POST request"})
      
      return response, 400



if __name__ == "__main__":
  app.run(debug=True)