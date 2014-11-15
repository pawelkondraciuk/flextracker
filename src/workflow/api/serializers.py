from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from projects.models import Project
from workflow.models import Workflow, Status


class ReadNestedWriteFlatMixin(object):
    """
    Mixin that sets the depth of the serializer to 0 (flat) for writing operations.
    For all other operations it keeps the depth specified in the serializer_class
    """

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super(ReadNestedWriteFlatMixin, self).get_serializer_class(*args, **kwargs)
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            serializer_class.Meta.depth = 0
        return serializer_class


class CreateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('name', 'type', 'id', 'available_states', 'workflow', 'verb')
        depth = 0


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name', 'type', 'available_states', 'workflow', 'verb')
        read_only_fields = ('workflow',)
        depth = 0


class WorkflowSerializer(serializers.ModelSerializer):
    states = StatusSerializer(many=True, required=False, allow_add_remove=True, read_only=False)

    class Meta:
        model = Workflow
        fields = ('id', 'name', 'states')

    def save_object(self, obj, **kwargs):
        if not obj.pk:
            obj.content_type = ContentType.objects.get_for_model(Project)

        return super(WorkflowSerializer, self).save_object(obj, **kwargs)