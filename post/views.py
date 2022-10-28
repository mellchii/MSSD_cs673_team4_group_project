from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404, redirect
from pscmodels.models import User, Posts, Shared, Comments, Following, Archive, Vote
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect, JsonResponse
from .forms import ProjectForm, CommentForm
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib import messages

TAG_COUNT = 20

def addProjectToPSC(request):
    user = request.user
    if (user.is_authenticated):
        common_tags = Posts.tags.most_common()[:TAG_COUNT]
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            newProject = form.save(commit=False)
            newProject.creator = request.user
            newProject.slug = slugify(newProject.title)
            try:
                newProject.save()
                form.save_m2m()
                messages.success(request, ('New Project Created'))
                return redirect('home')
            except:
                messages.warning(request, ('Project title already in use, Please use another project title.'))
                return redirect('addProject')
                

        context = {
            'posts': Posts,
            'tags': common_tags,
            'form': form
        }

        return render(request, 'post/post.html', context)
    else:
        messages.warning(request, ('Login to create a new project.'))
        return redirect("login")


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post = Posts.objects.filter(tags=tag)
    pager = Paginator(post, 10)  # Show 10 posts per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)
    common_tags = Posts.tags.most_common()[:TAG_COUNT]

    context = {
        'tags': common_tags,
        "user": request.user,
        'posts': page
    }

    return render(request, 'post/index.html', context)


class updatePost(UpdateView):
    model = Posts
    template_name = 'post/updatePost.html'
    form_class = ProjectForm


# class deletePost(DeleteView):
#     model = Posts
#     template_name = 'post/deletePost.html'
#     success_url = reverse_lazy('home')

def deletePost(request, pk):
    post = Posts.objects.get(pk = pk)
    if (str(request.user.username) == str(post.creator)):
        post.delete()
        messages.success(request, "Post '"+ post.title +"' is deleted") 
        return redirect('home')  

    else:
        messages.warning(request,('Permission Denied'))
        return redirect("home")


def favoritePost(request, pk):

    post = get_object_or_404(Posts, pk=pk)
    
    if post.favorites.filter(id=request.user.id).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
        

def editComment(request, pk, id):
    post = get_object_or_404(Posts, pk=pk)
    user = get_object_or_404(Comments, id=id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=user)
        if comment_form.is_valid():
            comment_form.save()

            return redirect(postDetailComment, pk)
        else:

            messages.warning(request, ('Sorry we were unable to update your review for {post.name}, please try again.'))

    else:
        comment_form = CommentForm(instance=user)

    template = 'post/editComment.html'
    context = {
        'post': post,
        'comment_form': comment_form
    }

    return render(request, template, context)


def deleteComment(request, pk, id):
    # post = get_object_or_404(Posts, pk=pk)
    comment = get_object_or_404(Comments, id=id)
    if request.user.id == comment.creator.id:
        Comments.objects.get(id=id).delete()

    return redirect(postDetailComment, pk)


def postDetailComment(request, pk):
    # post = Posts.objects.all()
    post = get_object_or_404(Posts, pk=pk)
    template_name = 'post/postDetail.html'
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comments(creator=request.user, post=post,
                               comment=request.POST["comment"])
            comment.save()
            return HttpResponseRedirect(str(post.id))
        else:
            messages.warning(request, ('Please login to make a comment'))
            return redirect("login")

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'pk': post.id,
                                           'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def search(request):
    # tags
    common_tags = Posts.tags.most_common()[:TAG_COUNT]

    if request.method == 'GET':
        search_terms = request.GET.get("search")
        posts = Posts.objects.filter(Q(title__icontains=search_terms) | Q(content__icontains=search_terms) | Q(
            category__icontains=search_terms) | Q(tags__name__icontains=search_terms) | Q(
            creator__username__icontains=search_terms)).distinct()
            
    if not posts:
        messages.warning(request,('No results found.'))
        posts = Posts.objects.all()

    return render(request, "post/index.html", {
        "posts": posts,
        "user": request.user,
        "tags": common_tags,
    })


def index(request):
    post = Posts.objects.all()
    pager = Paginator(post, 5)  # Show 5 posts per page.
    page_number = request.GET.get('page', 1)
    page = pager.page(page_number)

    # tags
    common_tags = Posts.tags.most_common()[:TAG_COUNT]

    if request.user.is_authenticated:
        upvotes = Vote.objects.filter(creator=request.user)

        ids = []
        for l in upvotes:
            ids.append(l.post.id)

        return render(request, "post/index.html", {
            "posts": page,
            "user": request.user,
            "ids": ids,
            "tags": common_tags,
        })
    return render(request, "post/index.html", {
            "posts": page,
            "user": request.user,
            "tags": common_tags,
        })




def vote(request):
    if request.POST.get('action') == 'vote':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Posts.objects.get(id=id)

        if update.votes.filter(id=request.user.id).exists():

            # Get the users current vote (True/False)
            q = Vote.objects.get(
                Q(post_id=id) & Q(creator_id=request.user.id))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed

                if button == 'thumbsup':
                    update.upvotes = F('upvotes') - 1
                    update.votes.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.upvotes
                    down = update.downvotes
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none', 'post_object': update.id})

                if button == 'thumbsdown':
                    # Change vote in Post
                    update.upvotes = F('upvotes') - 1
                    update.downvotes = F('downvotes') + 1
                    update.save()

                    # Update Vote

                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.upvotes
                    down = update.downvotes

                    return JsonResponse({'up': up, 'down': down, 'post_object': update.id})

            pass

            if evote == False:

                if button == 'thumbsup':
                    # Change vote in Post
                    update.upvotes = F('upvotes') + 1
                    update.downvotes = F('downvotes') - 1
                    update.save()

                    # Update Vote

                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.upvotes
                    down = update.downvotes

                    return JsonResponse({'up': up, 'down': down, 'post_object': update.id})

                if button == 'thumbsdown':
                    update.downvotes = F('downvotes') - 1
                    update.votes.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.upvotes
                    down = update.downvotes
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none', 'post_object': update.id})

        else:  # New selection

            if button == 'thumbsup':
                update.upvotes = F('upvotes') + 1
                update.votes.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post=update, creator=request.user, vote=True)
                new.save()
            else:
                # Add vote down
                update.downvotes = F('downvotes') + 1
                update.votes.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post=update, creator=request.user, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.upvotes
            down = update.downvotes

            return JsonResponse({'up': up, 'down': down, 'post_object': update.id})
    pass
