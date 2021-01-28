from django.shortcuts import render
from django.http import HttpResponse

from .forms import FileForm
from .main import make_assignment


def home(request):
    context = {}
    if request.method == 'POST':
        fileData = request.FILES["uploaded_file"].read().decode('ascii')
        fileData = fileData.replace("\r","")
        context["file_content"] = fileData
        
        img_path_array = make_assignment(fileData)
        print(img_path_array)
            
    else:
        print("Didnt get anything...")
    print(context)
    return render(request, 'assignmentApp/home.html', context)
