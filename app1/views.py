from django.shortcuts import render
from app1.NaiveByes import *

obj = {
    'user' : False
}
def profile(request):
    username = ''
    quantity = 0
    if request.method == 'POST':
        username = request.POST['username']
        quantity = int(request.POST['quantity'])
        print('\n\n\n User Found With The USERNAME: ',username , '\n\n\n')
        global obj #            ------------------------------ Global 
        obj = callNaiveBayes(username, quantity)
        if obj['user']== False:
            errMsg = "No User Found With The USERNAME: {}".format(username)
            return render(request, 'errPage.html', {'errMsg' : errMsg})
        obj['page'] = 'page1'
        return render(request, 'profile.html', obj)
    if obj['user']:
        obj['page'] = 'page1'
        return render(request, 'profile.html', obj)
    errMsg = "Page Not Found !!!"
    return render(request, 'errPage.html', {'errMsg' : errMsg})
def chart(request):
    if obj['user']:
        obj['page'] = 'page3'
        return render(request, 'chart.html', obj)
    errMsg = "Page Not Found !!!"
    return render(request, 'errPage.html', {'errMsg' : errMsg})

    
def tweetSentiments(request):
    if obj['user']:
        obj['page'] = 'page2'
        return render(request, 'tweetSentiments.html', obj)
    errMsg = "Page Not Found !!!"
    return render(request, 'errPage.html', {'errMsg' : errMsg})


def getUser(request):
    return render(request, 'home.html')
