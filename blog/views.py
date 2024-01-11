from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from blog.models import Post
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q


# Create your views here.
class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(
            Q(approved=True) | Q(approved=False,
                                 name=request.user.username
                                 )).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        total_likes = post.total_likes()
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "total_likes": total_likes,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(
            Q(approved=True) | Q(name=request.user)).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comments = list(comments) + [new_comment]
        else:
            comment_form = CommentForm()
            comments = post.comments.filter(Q(
                approved=True) | Q(approved=False,
                                   name=request.user.username)).order_by(
                                       "-created_on")

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentEdit(View):
    def get(self, request, slug, comment_id, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(post.comments, id=comment_id)
        if comment.approved:
            return HttpResponseForbidden(
                "You cannot edit an approved comment.")
        form = CommentForm(instance=comment)
        return render(request, 'edit_comment.html', {'form': form})

    def post(self, request, slug, comment_id, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(post.comments, id=comment_id)
        if comment.approved:
            return HttpResponseForbidden(
                "You cannot edit an approved comment.")
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug, ]))
        return render(request, 'edit_comment.html', {'form': form})


class CommentDelete(View):
    def post(self, request, slug, comment_id, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
