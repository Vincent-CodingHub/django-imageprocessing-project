from distutils.log import warn
from django.shortcuts import render
from .utils import get_plot, get_prediction

# Create your views here.
def index(request):
  return render(request, 'main_app/main1.html')

def information(request):
  return render(request, 'main_app/main2.html')

def predictImage(request):
    # fileObj=request.FILES['filePath']

    fileObj = request.FILES.get('filePath', False)

    if fileObj != False:
      context = get_prediction(fileObj)
      return render(request,'main_app/main1.html',context)
    else:
      return render(request,'main_app/main1.html')
