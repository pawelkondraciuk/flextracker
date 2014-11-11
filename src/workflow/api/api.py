from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions

from projects.models import Project
from workflow.api.serializers import WorkflowSerializer, StatusSerializer, CreateStatusSerializer
from workflow.models import Workflow, Status


class WorkflowAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    model = Workflow


class WorkflowListAPIView(generics.ListAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Workflow.objects.filter(content_type=ContentType.objects.get_for_model(Project),
                                       object_id=self.kwargs.get('project_id'))


class CreateWorkflowAPIView(generics.CreateAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    model = Workflow


class BindWorkflowAPIView(generics.UpdateAPIView):
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    model = Workflow

    def pre_save(self, obj):
        super(BindWorkflowAPIView, self).pre_save(obj)
        obj.content_type = ContentType.objects.get_for_model(Project)
        obj.object_id = self.kwargs['project_id']


class CreateStatusAPIView(generics.CreateAPIView):
    serializer_class = CreateStatusSerializer
    permission_classes = (permissions.IsAuthenticated, )
    model = Status


class UpdateStatusAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = StatusSerializer
    permission_classes = (permissions.IsAuthenticated, )
    model = Status