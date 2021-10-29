import os
import json
from dotenv import load_dotenv
import rest_framework.status as status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from django.http.response import HttpResponse
from rest_framework.views import APIView
from app.forms import PostCreationForm
from .models import User, Post
from .serializers import PostSerializer, UserSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Inbox as InboxItem
from .models import Post, User
from .serializers import PostSerializer, UserSerializer

load_dotenv()
HOST_API_URL = os.getenv("HOST_API_URL")


@api_view(["GET", "POST"])
def author(request, author_id):
    authorModel = get_object_or_404(User, pk=author_id)

    if request.method == "GET":
        serializer = UserSerializer(authorModel)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UserSerializer(authorModel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def authors(request):
    paginator = PageNumberPaginationWithCount()
    query_params = request.query_params
    query_set = User.objects.all().filter(type="author")

    if query_params:
        size = query_params.get("size")
        if size:
            paginator.page_size = size
        authors = paginator.paginate_queryset(query_set, request)
    else:
        authors = query_set

    serializer = UserSerializer(authors, many=True)
    data = {"type": "authors", "items": serializer.data}

    return Response(data, status=status.HTTP_200_OK)

class PostAPI(APIView):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostCreationForm(
            instance=post, data=request.POST, id=post_id, published=post.published, user=post.author)
        if form.is_valid():
            form.save()
            return HttpResponse("Sucessfully edited post")
        return HttpResponse("Failed to edit post")
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        return HttpResponse("Successfully deleted")

class PageNumberPaginationWithCount(PageNumberPagination):
    # Q: https://stackoverflow.com/q/40985248 (Stupid.Fat.Cat)
    # A: https://stackoverflow.com/a/54843913 (Rashid Mahmood)
    # CC BY-SA 4.0
    def get_paginated_response(self, data):
        response = super(PageNumberPaginationWithCount,
                         self).get_paginated_response(data)
        response.data['total_pages'] = list(
            range(1, self.page.paginator.num_pages+1))
        if response.data['next']:
            response.data['next'] = response.data['next'].replace('api', 'app')
        if response.data['previous']:
            response.data['previous'] = response.data['previous'].replace(
                'api', 'app')
            if 'page' not in response.data['previous']:
                response.data['previous'] = response.data['previous'].replace(
                    '?', '?page=1&')  # need to correct route for front end pagination to work
        return response


class Inbox(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        paginator = PageNumberPaginationWithCount()
        author_id = self.kwargs.get('author_id')
        query_set = InboxItem.objects.filter(author_id=author_id)
        size = request.query_params.get('size', 10)
        page = request.query_params.get('page', 1)
        paginator.page = page
        paginator.page_size = size
        paginated_qs = paginator.paginate_queryset(query_set, request)

        items = []
        for item in paginated_qs:
            if item.content_type.name == 'post':
                s = PostSerializer(item.content_object)
                items.append(s.data)
            elif item.content_type.name == 'follow':
                # TODO: serialize follow objectrs
                pass
            elif item.content_type.name == 'like':
                # TODO: serialize like objectrs
                pass
        r = paginator.get_paginated_response(paginated_qs)
        data = {'type': 'inbox', 'author': HOST_API_URL +
                'author/'+author_id, 'next': r.data.get('next'),
                'prev': r.data.get('previous'), 'size': size,
                'page': paginator.get_page_number(request, paginated_qs),
                'total_pages': r.data.get('total_pages'),
                'items': items}

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, author_id, *args, **kwargs):
        try:
            content_type = request.data["content_type"]
            object_id = request.data["object_id"]
            if content_type == "post":
                content_object = Post.objects.get(id=object_id)
                author = User.objects.get(id=author_id)
                inbox = InboxItem.objects.create(author_id=author.id,
                                                 content_object=content_object)
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            author_id = self.kwargs.get('author_id')
            inbox = InboxItem.objects.filter(author_id=author_id)
            inbox.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
