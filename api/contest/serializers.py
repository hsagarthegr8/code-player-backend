from rest_framework import serializers
import subprocess
import os

from contest.models import Problem, Contest
from contest.utils import run_code, ensure_dir


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('problem_code', 'name', 'accuracy',
                  'total_submissions', 'successful_submissions')


class ProblemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('input_file', 'output_file')
        extra_kwargs = {
            'contest': {'read_only': True},
            'problem_setter': {'read_only': True}
        }

    def create(self, validated_data):
        contest = self.context.get('view').kwargs.get('contest')
        user = self.context.get('request').user
        validated_data['contest'] = Contest.objects.get(pk=contest)
        validated_data['problem_setter'] = user
        return super(ProblemDetailsSerializer, self).create(validated_data)


class ContestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('name', 'contest_code', 'start_date', 'end_date')


class ContestDetailsSerializer(serializers.ModelSerializer):
    problems = ProblemListSerializer(read_only=True, many=True)

    class Meta:
        model = Contest
        fields = ('name', 'contest_code', 'start_date', 'end_date', 'problems')


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
        directory = 'files/PLAYGROUND'
        ensure_dir(directory)
        source_file = f'{user.username}.py'
        input_file = f'{user.username}.in'

        filepath = os.path.join(directory, source_file)
        input_path = os.path.join(directory, input_file)

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
