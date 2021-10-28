import os
from drf_yasg import openapi

import rest_framework.status as status
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inbox as InboxItem
from .models import Post, User
from .serializers import PostSerializer, UserSerializer, InboxSerializer

load_dotenv()
HOST_API_URL = os.getenv("HOST_API_URL")


class Author(APIView):
    """
    Endpoint for getting and updating author's on the server.
    """

    def get_author(self, author_id):
        return get_object_or_404(User, pk=author_id)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Author Found.", examples={"application/json": {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "exampleAuthor",
                "url": "http://127.0.0.1:8000/api/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                "github": "http://github.com/exampleAuthor"
            }}),
            404: openapi.Response(description="Author Not Found.", examples={"application/json": {'detail': 'Not Found.'}}),
            400: openapi.Response(description="Method Not Allowed.", examples={"application/json": {'detail': "Method \"PUT\" not allowed."}})
        }
    )
    def get(self, request, author_id):
        """
        GETs and returns an Author object with id {author_id}, if one exists.

        GETs and returns an Author object with id {author_id}, if one exists.
        """
        author_model = self.get_author(author_id)
        serializer = UserSerializer(author_model)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Author Updated Succesfully.", examples={"application/json": {
                "type": "author",
                "id": "http://127.0.0.1:8000/api/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                "host": "http://127.0.0.1:8000/api/",
                "displayName": "exampleAuthor",
                "url": "http://127.0.0.1:8000/api/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                "github": "http://github.com/exampleAuthor"
            }}),
            404: openapi.Response(description="Author Not Found.", examples={"application/json": {'detail': 'Not Found.'}}),
            400: openapi.Response(description="Method Not Allowed.", examples={"application/json": {'detail': "Method \"PUT\" not allowed."}})
        },
        request_body=UserSerializer
    )
    def post(self, request, author_id):
        """
        Updates and returns the updated Author object with id {author_id}, if the Author exists.

        Not all fields need to be sent in the request body.
        """
        author_model = self.get_author(author_id)
        serializer = UserSerializer(author_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(description="Success",
                              examples={"application/json": [{
                                  "type": "author",
                                  "id": "http://127.0.0.1:8000/api/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                  "host": "http://127.0.0.1:8000/api/",
                                  "displayName": "Bill",
                                  "url": "http://127.0.0.1:8000/api/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                  "github": "http://github.com/bill123"
                              },
                                  {
                                  "type": "author",
                                  "id": "http://127.0.0.1:8000/api/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                  "host": "http://127.0.0.1:8000/api/",
                                  "displayName": "Frank",
                                  "url": "http://127.0.0.1:8000/api/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                  "github": "http://github.com/FrankFrank"
                              }
                              ]}),
        400: openapi.Response(description="Method Not Allowed.", examples={"application/json": {'detail': "Method \"POST\" not allowed."}})
    },
    paginator_inspectors='d',
    tags=['author'],
    manual_parameters=[
        openapi.Parameter(
            'page', openapi.IN_QUERY, description='A page number within the paginated result set.', type=openapi.TYPE_INTEGER),
        openapi.Parameter(
            'size', openapi.IN_QUERY, description='The size of the page to be returned', type=openapi.TYPE_INTEGER)
    ])
@ api_view(["GET"])
def authors(request):
    """
    GETs and returns a paginated list of all Authors on the server. 

    Pagination settings are passed as url parameters: ~/inbox/?page=1&size=5
    """
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


@ api_view(["GET"])
def posts(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    serializer = PostSerializer(post)
    return Response(serializer.data)


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
    serializer_class = InboxSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response(description='Successfully get inbox items.',
                                         examples={"application/json":
                                                   {
                                                       "type": "inbox",
                                                       "author": "http://127.0.0.1:8000/api/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                                       "next": "http://127.0.0.1:8000/app/author/077d7a7e-304c-4f34-9d8f-d3c61e214b35/inbox/?page=2&size=5",
                                                       "prev": 'null',
                                                       "size": "5",
                                                       "page": "1",
                                                       "total_pages": [
                                                           1, 2
                                                       ],
                                                       "items": [
                                                           {
                                                               "type": "post",
                                                               "title": "Test",
                                                               "id": "5836ca64-16d5-4b69-872a-41ca3ec25bf9",
                                                               "source": "http://127.0.0.1:8000/api/posts/5836ca64-16d5-4b69-872a-41ca3ec25bf9",
                                                               "origin": "http://127.0.0.1:8000/api/posts/5836ca64-16d5-4b69-872a-41ca3ec25bf9",
                                                               "description": "Test: This is my post....",
                                                               "contentType": "text/plain",
                                                               "content": "This is my post.",
                                                               "author": "077d7a7e-304c-4f34-9d8f-d3c61e214b35",
                                                               "categories": [
                                                                   "New",
                                                                   " Post",
                                                                   " Test"
                                                               ],
                                                               "count": 0,
                                                               "size": 0,
                                                               "comment_page": "http://127.0.0.1:8000/api/posts/5836ca64-16d5-4b69-872a-41ca3ec25bf9/comments",
                                                               "published": "2021-10-20T14:06:58.121854-06:00",
                                                               "visibility": "public",
                                                               "unlisted": 'true'
                                                           }, '...'
                                                       ]
                                                   }
                                                   })},
        tags=['inbox'],
        manual_parameters=[
            openapi.Parameter(
                'size', openapi.IN_QUERY, description='The size of the page to be returned', type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a paginated list of {authord_id}'s inbox.

        Pagination settings are passed as url parameters: ~/author/{author_id}/inbox/?page=1&size=5
        """
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

    @swagger_auto_schema(
        responses={
            204: openapi.Response(description="Succesffuly POST an item to an author's inbox."),
        },
        tags=['inbox'])
    def post(self, request, author_id, *args, **kwargs):
        """
        Send an item to {author_id}'s inbox. For now, posts are the only accepted objects.

        'post' is the only content_type that is supported at this time.
        """
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

    @ swagger_auto_schema(
        responses={
            204: openapi.Response(description="Inbox successfully deleted."),
        },
        tags=['inbox'])
    def delete(self, request, *args, **kwargs):
        """
        Delete all items in {author_id}'s Inbox.
        """
        try:
            author_id = self.kwargs.get('author_id')
            inbox = InboxItem.objects.filter(author_id=author_id)
            inbox.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
