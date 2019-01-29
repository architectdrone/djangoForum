from django.shortcuts import render, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User as authUser
from django.contrib.auth import authenticate, login, logout
from .models import user, post, comment

# Create your views here.


def homeReDir(request):
    return HttpResponseRedirect('1')

#MAIN VIEWS
def home(request, page_number):
    #Get the posts to display
    lower_bound = 10*(page_number-1)
    upper_bound = 10*(page_number-1)+10
    allPosts = post.objects.order_by('-date')[lower_bound:upper_bound]
    
    context = {'to_display': allPosts, 'page_number': page_number}
    template = loader.get_template('forum/home.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def postView(request, post_pk, page_number):
    #Get the post itself
    the_post = post.objects.get(pk = post_pk)
    
    #Get the comments to display
    lower_bound = 10*(page_number-1)
    upper_bound = 10*(page_number-1)+10
    the_comments = the_post.replies.order_by('date')[lower_bound:upper_bound]
    
    context = {'page_number': page_number, 'post': the_post, 'comments': the_comments}
    template = loader.get_template('forum/post.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def userView(request, user_pk):
    #Get the user, all comments he has made, and all posts he has made.
    the_user = user.objects.get(pk = user_pk)
    the_posts = the_user.posts_made.all()
    the_comments = the_user.comments_made.all()
    context = {'userToShow': the_user, 'posts': the_posts, 'comments': the_comments}
    template = loader.get_template('forum/user.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def submitComment(request, post_pk):
    #Get the post we are replying to.
    the_post = post.objects.get(pk = post_pk)
    
    context = {'post': the_post}
    template = loader.get_template('forum/submitComment.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def submitPost(request):
    context = {}
    template = loader.get_template('forum/submitPost.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def loginView(request):
    context = {}
    template = loader.get_template('forum/login.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def signup(request):
    context = {}
    template = loader.get_template('forum/signup.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))

def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/forum')

#Landings/Technical
def submitPostLanding(request):
    post_data = request.POST
##    #Old System, which didn't have consistent accounts.
##    try:
##        the_user = user.objects.get(name = post_data['name'])
##    except: #If the user does not yet exist.
##        the_user = user(name = post_data['name'])
##        the_user.save()

    try:
        the_user = user.objects.get(pk = request.session['user_pk'])
    except KeyError:
        #If the user is not logged in, there will be a KeyError, because user_pk will not exist yet.
        #In that case, we will prompt them to log in.
        context = {'error_message': "You are not logged in. Please log in and try again."}
        template = loader.get_template('forum/login.html')
        #Send information about the current user to the template.
        try:
            context['current_user'] = user.objects.get(pk = request.session['user_pk'])
        except:
           pass
        return HttpResponse(template.render(context, request))

    the_post = post(user = the_user, content = post_data['content'], subject = post_data['subject'])
    the_post.save()
    the_user.posts_made.add(the_post)
    the_user.save()

    return HttpResponseRedirect('/forum')

def submitCommentLanding(request, post_pk):
    post_data = request.POST
##    #Old System
##    try:
##        the_user = user.objects.get(name = post_data['name'])
##    except: #If the user does not yet exist.
##        the_user = user(name = post_data['name'])
##        the_user.save()
    
    try:
        the_user = user.objects.get(pk = request.session['user_pk'])
    except KeyError:
        #If the user is not logged in, there will be a KeyError, because user_pk will not exist yet.
        #In that case, we will prompt them to log in.
        context = {'error_message': "You are not logged in. Please log in and try again."}
        template = loader.get_template('forum/login.html')
        #Send information about the current user to the template.
        try:
            context['current_user'] = user.objects.get(pk = request.session['user_pk'])
        except:
           pass
        return HttpResponse(template.render(context, request))
    
    the_post = post.objects.get(pk = post_pk)
    the_comment = comment(user = the_user, content = post_data['comment'], post = the_post)
    the_comment.save()
    the_post.replies.add(the_comment)
    the_post.save()
    the_user.comments_made.add(the_comment)
    the_user.save()

    return HttpResponseRedirect(f'/forum/post/{post_pk}/1')

def loginLanding(request):
    post_data = request.POST

    #The authenticate function will return either an instance of authUser, or a NoneType if the credentials are wrong.
    userToAuth = authenticate(username=post_data['username'], password = post_data['password'])

    #If credentials were right
    if userToAuth is not None:
        login(request, userToAuth)
        the_user = user.objects.get(name=post_data['username'])
        request.session['user_pk'] = the_user.pk
        return HttpResponseRedirect("/forum")
    #If credentials were wrong
    else:
        error_message = f"Error Logging In."
        context = {'error_message': error_message}
        template = loader.get_template('forum/login.html')
        #Send information about the current user to the template.
        try:
            context['current_user'] = user.objects.get(pk = request.session['user_pk'])
        except:
           pass
        return HttpResponse(template.render(context, request))

def signupLanding(request):
    post_data = request.POST
    #Check to make sure the passwords match ;)
    if post_data['password'] != post_data['retype_password']:
        error_message = f"Passwords do not match."
        context = {'error_message':error_message}
        template = loader.get_template('forum/signup.html')
        #Send information about the current user to the template.
        try:
            context['current_user'] = user.objects.get(pk = request.session['user_pk'])
        except:
           pass
        return HttpResponse(template.render(context, request))

    #Create a new instance of authUser, which is exclusively for verifing passwords.
    new_user = authUser.objects.create_user(post_data['username'], password=post_data['password'])
    #Create a new instance of user, which is for storing data.
    new_forum_user = user(name=post_data['username'])
    new_forum_user.save()
    
    #Have the user sign in
    context = {}
    template = loader.get_template('forum/login.html')
    #Send information about the current user to the template.
    try:
        context['current_user'] = user.objects.get(pk = request.session['user_pk'])
    except:
       pass
    return HttpResponse(template.render(context, request))


