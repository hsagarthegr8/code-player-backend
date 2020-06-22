from contest.models import Problem, Contest
from django.http import Http404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView


from .serializers import (ProblemListSerializer, ProblemDetailsSerializer,
                          PlaygroundSerializer, ContestListSerializer, ContestDetailsSerializer)


class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestListSerializer

    def __init__(self, *args, **kwargs):
        super(ContestViewSet, self).__init__(*args, **kwargs)

        self.serializer_action_classes = {
            'list': ContestListSerializer,
            'retrieve': ContestDetailsSerializer
        }

    def get_serializer_class(self, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ContestViewSet, self).get_serializer_class()


class ProblemViewSet(ModelViewSet):
    serializer_class = ProblemListSerializer

    def get_queryset(self):
        try:
            contest_code = self.kwargs.get('contest')
            return Contest.objects.get(contest_code=contest_code).problems.all()
        except:
            raise Http404

    def __init__(self, *args, **kwargs):
        super(ProblemViewSet, self).__init__(*args, **kwargs)

        self.serializer_action_classes = {
            'list': ProblemListSerializer,
            'retrieve': ProblemDetailsSerializer,
            'create': ProblemDetailsSerializer
        }

    def get_serializer_class(self, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ProblemViewSet, self).get_serializer_class()


class Playground(CreateAPIView):
    '''
    Api to support the code playground in the UI.   
    It generally takes `sourceCode` and `customInput` based on the `isCustomInput` flag.  
    It runs the source code and return `stderr`, `stdout`, `returnCode` and `time` to execute the code.
    '''
    serializer_class = PlaygroundSerializer
