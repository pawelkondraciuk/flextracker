from rest_framework import serializers
from workflow.models import Workflow, Status

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'name', 'type', 'available_states')

class WorkflowSerializer(serializers.ModelSerializer):

    states = StatusSerializer()

    class Meta:
        model = Workflow
        fields = ('id', 'name', 'states')