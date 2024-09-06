from flask import Flask, request 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form method="post" action="/upload" enctype="multipart/form-data"> 
        <label for="username">User Name:</label>
        <input type="text" id="username" name="username"><br>
        <label for="useremailid">Email ID:</label>
        <input type="email" id="useremailid" name="useremailid">
        <label for="file">Choose a file:</label>
        <input type="file" id="file" name="file" accept=".pdf">
        <input type="submit">

    </form>
</body>
</html>'''

@app.route("/upload", methods=['POST'])
def uploaded_file():
    name=request.form.get('username')
    email=request.form.get('useremailid')
    file=request.files.get('file')
    filename=f"{name}_{email}.pdf"
    if file:
       file.save(f"uploads_file/{filename}")
    print("Name: ", name)
    print("Email: ", email)
    return "Done"
