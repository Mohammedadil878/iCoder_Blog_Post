from django.shortcuts import render, redirect, HttpResponse
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = { 'allPosts' : allPosts }
    return render(request, 'blog/blogHome.html', context)
    # return HttpResponse('This is blogHome, We will keep all the blog Post here')

def blogPost(request, slug):
    post = Post.objects.filter(slug = slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post = post, parent = None)
    replies = BlogComment.objects.filter(post = post).exclude(parent = None)
    replyDict = {}
    for reply in replies:
        if reply.parent.slno not in replyDict.keys():
            replyDict[reply.parent.slno] = [reply]
        else:
            replyDict[reply.parent.slno].append(reply)

    # print(comments, replies)
    # print(replyDict)
    context = { 'post' : post, 'comments' : comments, 'user' : request.user, 'replyDict' : replyDict }
    return render(request, 'blog/blogPost.html', context )

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        # post = Post.objects.filter(slno = postSno).first()
        post = Post.objects.get(slno = postSno)
        parentslno = request.POST.get('parentslno')
        if parentslno == "":
            comment = BlogComment(comment = comment, user = user, post = post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully.")
        else:
            parent = BlogComment.objects.get(slno = parentslno)
            comment = BlogComment(comment = comment, user = user, post = post, parent = parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully.")

    return redirect(f'/blog/{post.slug}')