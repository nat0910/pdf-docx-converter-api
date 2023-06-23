from fastapi import FastAPI,UploadFile,File
from fastapi.responses import FileResponse

from pdf2docx import Converter
from docx2pdf import convert

from starlette.background import BackgroundTask

import os



app = FastAPI()

base_path = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(base_path,"upload")
export_path = os.path.join(base_path,'export')


@app.get('/')
async def starting():
    return {
        "msg":"This API is for Converting your PDF to WORD or WORD to PDF !! "
    }

@app.post('/convert-pdf-docx')
async def set_user(q:UploadFile):

    upload_file_path = os.path.join(upload_path,q.filename)
    export_file_path = os.path.join(export_path,q.filename.split('.')[0]+".docx")

    def cleanupFunction():
        os.remove(upload_file_path)
        os.remove(export_file_path)

    with open(upload_file_path,'wb') as file:
        file.write(q.file.read())

    file_cv = Converter(upload_file_path)
    file_cv.convert(export_file_path)
    file_cv.close()
    return FileResponse(filename=q.filename.split('.')[0],path=export_file_path,media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',background=BackgroundTask(cleanupFunction))

@app.post('/convert-docx-pdf')
async def set_user(q:UploadFile):

    upload_file_path = os.path.join(upload_path,q.filename)
    export_file_path = os.path.join(export_path,q.filename.split('.')[0]+".pdf")

    def cleanupFunction():
        os.remove(upload_file_path)
        os.remove(export_file_path)

    with open(upload_file_path,'wb') as file:
        file.write(q.file.read())

    convert(upload_file_path,export_file_path)
    
    return FileResponse(filename=q.filename.split('.')[0],path=export_file_path,media_type='application/pdf',background=BackgroundTask(cleanupFunction))