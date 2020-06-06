from rest_framework.serializers import ModelSerializer

from problems.models import Problem


class ProblemListSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name')


class ProblemDetailsSerializer(ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('input_file', 'output_file')