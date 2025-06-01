from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import EmailStr
from database import Database
from pydantic import BaseModel
from readpdf import ReadPDF
from wordlist import get_wordlist
import random
import uvicorn


'''Lemmatization'''
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('wordnet')


app = FastAPI()

class User(BaseModel):
    email: EmailStr = "example@example.com"
    name: str = "example"
    phone: int = 1234567890
    filePath: str = "./Files/example.pdf"
    fileName: str = "example.pdf"

class ReturnStatus(BaseModel):
    status: int = 200
    message: str = "success"
    data: dict = {}

class Report(BaseModel):
    file_id: str = "000000000"

db = Database()
db.create_table()

@app.get("/")
def read_root():
    return FileResponse("./Static/index.html")

@app.post("/addUser")
def add_user(userDetails: User):
    db.insert(
        userDetails.email,
        userDetails.name,
        userDetails.phone,
        userDetails.filePath,
        userDetails.fileName
    )
    return ReturnStatus(status=200, message="User added successfully")

@app.get("/report")
def report():
    return FileResponse("./Static/search.html")


# get the wordlist
wordlist = get_wordlist()
# print(wordlist)
@app.post("/getReport")
def get_report(file_id: Report):
    user = db.getFiles(file_id.file_id)
    emailID = user[1]
    name = user[2]
    phone = user[3]
    file_path = user[4]
    file_name = user[5]

    # pdfReader
    pdf = ReadPDF(file_path)
    text = pdf.read()
    cleaned_text = pdf.clean_text(text)

    # lemmatization
    temp = "".join(
        letter for letter in cleaned_text if (
            letter.isalnum() or letter.isspace() or letter == "."
        )
    )
    temp = " ".join(temp.split())

    # remove numbres from the text
    temp = "".join(
        letter for letter in temp if not letter.isdigit() or letter == " " or letter == "."
    )
    temp = " ".join(temp.split())

    # convert to lowercase
    temp = temp.lower()

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    temp_word = ""
    for word in word_tokenize(temp):
        temp_word += lemmatizer.lemmatize(word) + " "
    temp = temp_word

    # get important words
    sentences = temp.split(".")
    important_words = []
    for i in sentences:
        words = i.split(" ")
        ptr_1 = 0
        ptr_2 = 0
        n = len(words)
        while ptr_2 < n:
            if words[ptr_2] in wordlist:
                if ptr_1 != ptr_2:
                    important_words.append(" ".join(words[ptr_1:ptr_2]))
                ptr_1 = ptr_2 + 1
            ptr_2 += 1
        if ptr_1 != ptr_2:
            important_words.append(" ".join(words[ptr_1:ptr_2]))

    important_words = list(set(important_words))
    return {
        "email": emailID,
        "name": name,
        "phone": phone,
        "file_path": file_path,
        "file_name": file_name,
        "report": important_words
    }




@app.post("/upload")
async def upload_file(
    emailaddress: str = Form(...),
    users_name: str = Form(...),
    users_phone: int = Form(...),
    upload_pdf: UploadFile = File(...)
):
    random_file_id = str(random.randint(100000000, 999999999))
    random_file_name = f"{random_file_id}.pdf"
    file_location = f"./Files/{random_file_name}"
    with open(file_location, "wb") as file_object:
        file_object.write(upload_pdf.file.read())
    db.insert(emailaddress, users_name, users_phone, file_location, random_file_name)

    html_content = r"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>File Upload Success</title>
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet"
        />
        <style>
          body,
          html {
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f8f9fa;
          }
          .card {
            padding: 30px;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <div class="card shadow">
          <h2 class="text-success mb-4">File Successfully Uploaded!</h2>
          <p class="lead">Your file ID is: <strong>"""+random_file_id+r"""</strong></p>
          <p id="countdown" class="lead">
            Redirecting to the main page in 3 seconds...
          </p>
        </div>

        <script>
          let count = 10;
          const countdownElement = document.getElementById("countdown");

          const countdownInterval = setInterval(() => {{
            count--;
            if (count >= 0) {{
              countdownElement.textContent = `Redirecting to the main page in ${count} seconds...`;
            }}
            if (count === 0) {{
              clearInterval(countdownInterval);
              window.location.href = "/"; // Replace with your main page URL
            }}
          }}, 1000);
        </script>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)


def __main__():
    uvicorn.run(app, host="0.0.0.0", port=8000)

__main__()
