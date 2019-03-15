from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Container, Pull, Request, User
from .serializers import ContainerSerializer, PullSerializer, RequestSerializer, UserSerializer


class ContainerViewSet(ModelViewSet):
    model = Container
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()


class PullViewSet(ModelViewSet):
    model = Pull
    serializer_class = PullSerializer
    queryset = Pull.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            new_pull = Pull.objects.create()
            containers = request.data.get('containers')
            for c in containers:
                container = Container.objects.get(pk=c)
                container.pull = new_pull
                container.save()
                container_request = container.request
                container_request.status = Request.IN_PROGRESS
                container_request.save()
                new_pull.total_space += container.size
            new_pull.save()
            serializer = PullSerializer(new_pull, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)


class RequestViewSet(ModelViewSet):
    model = Request
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def exceeds_capacity():
        request_size = sum([c['size'] for c in self.containers])
        if request_size > self.user.available_space:
            return True
        return False

    def create(self, request, *args, **kwargs):
        try:
            self.containers = request.data.get('containers')
            self.user = User.objects.get(pk=request.data.get('user'))
            if self.exceeds_capacity():
                raise Exception("Request exceeds user capacity")
            new_request = Request.objects.create(
                user=self.user,
            )
            for c in self.containers:
                container = Container.objects.get(pk=c)
                container.request = new_request
                container.save()
                new_request.total_space += container.size
            new_request.save()
            serializer = RequestSerializer(new_request, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)


class UserViewSet(ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()


class QueueView(TemplateView):
    template_name = 'transactions/main.html'
