from django.http import HttpResponse
from django.shortcuts import redirect, render
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
# html pages
def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is homePage')

def about(request):
    # messages.success(request, "This is About.")
    # messages.success(request, "This is About1.")
    # messages.success(request, "This is About2.")\
    # messages.success(request, "This is About3.")
    return render(request, 'home/about.html')
    # return HttpResponse('This is AboutPage')

def contact(request):
    # messages.error(request, "Welcome to Contact.")
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly!")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent successfully")
    return render(request, 'home/contact.html')
    # return HttpResponse('This is ContactPage')

def search(request):
    query = request.GET['query']
    # allPosts = Post.objects.all()
    if len(query) > 74:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = { 'allPosts' : allPosts, 'query' : query }
    return render(request, 'home/search.html', params)
    # return HttpResponse("This is search")

# authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        # Username should be under 10 characters
        if len(username) < 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        
        # Username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username must contain only numbers and letters")
            return redirect('home')
        
        # Passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created!")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Get POST parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(request, username = loginusername, password = loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return redirect('home')
    return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
    # return HttpResponse("handleLogout")