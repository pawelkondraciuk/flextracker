from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from projects.models import Project
from workflow.api.serializers import WorkflowSerializer
from workflow.models import Workflow


class WorkflowAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )

class WorkflowListAPIView(generics.ListAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Workflow.objects.filter(content_type=ContentType.objects.get_for_model(Project), object_id=self.kwargs.get('project_id'))

class CreateWorkflowAPIView(generics.CreateAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )