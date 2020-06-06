from rest_framework.viewsets import ModelViewSet

from .serializers import ProblemListSerializer, ProblemDetailsSerializer, Problem

class ProblemViewSet(ModelViewSet):
    queryset = Problem.objects.all()

    def __init__(self, *args, **kwargs):
        super(ProblemViewSet, self).__init__(*args, **kwargs)

        self.serializer_action_classes = {
            'list': ProblemListSerializer,
            'retrieve': ProblemDetailsSerializer
        }

    def get_serializer_class(self, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ProblemViewSet, self).get_serializer_class()
        
