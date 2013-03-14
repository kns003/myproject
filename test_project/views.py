from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django import forms
import datetime, random, sha
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from test_project.forum.models import Thread, Comment
from test_project.forms import ThreadForm , UserRegisterForm, CommentForm,ThreadSearchForm
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
import logging
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


logger = logging.getLogger(__name__)

def home(request):
    
    if request.method=="POST":
        form=ThreadSearchForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            threads=Thread.objects.filter(title__icontains=title)
            context_variable=RequestContext(request)
            return render_to_response('home.html',locals(),context_variable)
        else:
            

            return HttpResponse("No such threads present.Please try again")
    else:    
        form=ThreadSearchForm()
        threads = Thread.objects.all()
        return render_to_response('home.html', locals())
    
@login_required

def add_thread(request):
	#logger.debug('add_thread')
	if request.method == 'POST':
		form=ThreadForm(request.POST)
		if form.is_valid():
		    #logger.debug('username' + str(form.cleaned_data['username']))
		    thread = Thread.objects.create(
		        thread_user = User.objects.get(pk = request.user.id),
                title = form.cleaned_data['title'],
				description = form.cleaned_data['description'],
			)
	       
	        
		return HttpResponseRedirect('/')
	else:	
		logger.debug('init form')
		form=ThreadForm()

	context=RequestContext(request,{'title':'Add Item','form':form})
	return render_to_response('addThread.html', locals())


def register_user(request):
    #logger.debug('register_user')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #logger.debug('username:' + str(form.cleaned_data['username']))
            user = User.objects.create(
                username = form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],            
            )
            user.set_password(str(form.cleaned_data['re_password']))
            user.save()
            #logger.debug('user is created.')
            return HttpResponseRedirect('/login/')
    else:
        form = UserRegisterForm()
        
    variables = RequestContext(request, {
        'form': form,
    })
    return render_to_response(
        'userRegister.html', locals()
    )



def login_user(request):
    #logger.debug('login_user')
    state = 'Plz do login.'
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        #logger.debug('user:' + str(user))
        if user is not None and user.is_active:            
            login(request, user)
            #logger.debug('i am logged in')
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')        
    return render_to_response('loginUser.html',{'state':state, 'username': username})

def logout_user(request):
    #logger.debug('logout_user')
    logout(request)
    return HttpResponseRedirect('/')

def thread_page(request,t_id):
    #logger.debug('request:' + str(request))
    #logger.debug('username:' + str(request.user.username))
    #logger.debug('is_authenticated:' + str(request.user.is_authenticated()))
    thread = Thread.objects.get(id = t_id)
    comments = Comment.objects.filter(thread__id = t_id)
    return render_to_response('threadPage.html', locals())
    
@login_required

def add_comment(request,thread_id):
    #logger.debug('username:' + str('username'))
    thread = Thread.objects.get(id=thread_id)
    
    if request.method=='POST':
        form=CommentForm(request.POST)
        
        if form.is_valid():    
            thread=Thread.objects.get(id = thread_id)
            comment = Comment.objects.create(
                commented_by = User.objects.get(pk = request.user.id),
                thread = thread,
                text = form.cleaned_data['text'],
                userUpVotes = 0,
                userDownVotes = 0,
                         )
            return HttpResponseRedirect('/thread/%s/' % thread.id)
    else:
        form=CommentForm()
        
    context_variables = RequestContext(request,{'form':form, 'thread': thread ,'threadname':thread.title})
    return render_to_response('addComment.html', locals())
    

@login_required
def vote(request,vote_type, comment_id):
    print "inside"
    if request.is_ajax():
        print("it's an ajax call")
        comment=Comment.objects.get(pk=comment_id)
        #t=request.META['REMOTE_ADDR']
        value = 0
        if vote_type == "up":
            comment.userUpVotes+=1
            value = comment.userUpVotes
        else :
            comment.userDownVotes+=1
            value = comment.userDownVotes
            
        comment.save()
        logger.debug('updating')#comment_details = {"up": comment.userUpVotes, "down": comment.userDownVotes}
        #if 'HTTP_REFERER' in request.META:
        #    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return HttpResponse (value)
    
@login_required
def delete_comment(request, comment_id):
    comment=Comment.objects.get(pk=comment_id)
    comment.delete()
    return HttpResponseRedirect('/thread/%s' % comment.thread.id)
    
@login_required
def delete_thread(request,thread_id):
    thread=Thread.objects.get(pk=thread_id)
    thread.delete()
    return HttpResponseRedirect('/')
    
@login_required
def edit_thread(request,thread_id):
    thread=Thread.objects.get(pk=thread_id)
    if request.method=='POST':
        form=ThreadForm(request.POST)
        if form.is_valid():
            thread.title=form.cleaned_data['title']
            thread.description=form.cleaned_data['description']
            thread.save()
            logger.debug("editing a form")
            return HttpResponseRedirect('/thread/%s/' % thread.id)
        
    else:
        form=ThreadForm()
        form.fields['title'].initial=thread.title
        form.fields['description'].initial=thread.description
    
    context=RequestContext(request,{'title':'Edit Item','form':form})
    return render_to_response('addThread.html', locals())
    
@login_required
def edit_comment(request,comment_id):
    comment=Comment.objects.get(pk=comment_id)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment.text=form.cleaned_data['text']
            comment.save()
            return HttpResponseRedirect('/thread/%s' % comment.thread.id)
    else:
        form=CommentForm()
        form.fields['text'].initial=comment.text
        
    context=RequestContext(request,{'title':'Edit Comment','form':form})
    return render_to_response('addComment.html',locals())
    

