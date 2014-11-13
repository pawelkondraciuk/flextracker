from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import DeleteView
from comments.models import Comment


class DeleteComment(DeleteView):
    template_name = 'comments/delete.html'
    model = Comment

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()