from rest_framework import serializers
import subprocess
import os

from problems.models import Problem
from problems.utils import run_code


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name')


class ProblemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('input_file', 'output_file')


class PlaygroundSerializer(serializers.Serializer):
    source_code = serializers.CharField(
        style={'base_template': 'textarea.html'}, write_only=True)
    is_custom_input = serializers.BooleanField(write_only=True)
    custom_input = serializers.CharField(
        allow_blank=True,
        style={'base_template': 'textarea.html'}, write_only=True)
    stdout = serializers.CharField(read_only=True)
    stderr = serializers.CharField(read_only=True)
    return_code = serializers.IntegerField(read_only=True)
    time = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        user = self.context.get('request').user
        filepath = f'files/problems/{user.username}/playground.py'
        input_path = f'files/problems/{user.username}/playground.in'
        with open(filepath, 'w') as file:
            file.write(validated_data['source_code'])

        if not validated_data['is_custom_input']:
            validated_data['custom_input'] = ''

        with open(input_path, 'w') as file:
            file.write(validated_data['custom_input'])

        with open(filepath, 'w') as file:
            file.write(validated_data['source_code'])

        runner, time = run_code(filepath, input_path)

        os.remove(filepath)
        os.remove(input_path)
        validated_data['stdout'] = runner.stdout.decode()
        validated_data['stderr'] = runner.stderr.decode()
        validated_data['return_code'] = runner.returncode
        validated_data['time'] = time

        return validated_data
