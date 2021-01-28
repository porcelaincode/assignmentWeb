from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime

from .forms import FileForm
from .main import make_assignment


def home(request):
    date_ = datetime.now().strftime("%d%m%y%H%M%S")
    context = {}
    if request.method == 'POST':
        font = request.POST["fonts"]
        page_type = request.POST["page_type"]
        try:
            fileData = request.FILES["uploaded_file"].read().decode('ascii')
            fileData = fileData.replace("\r","")
            context["file_content"] = fileData
            
            img_path_array = make_assignment(fileData, date_, font, page_type)
            context["paths"] = img_path_array
            context["date"] = date_
        except Exception as e:
            context["error"] = e
    else:
        print("Didnt get anything...")
    print(context)
    return render(request, 'assignmentApp/home.html', context)
