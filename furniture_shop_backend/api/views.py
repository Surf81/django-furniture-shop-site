from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .authentication import AdvancedBasicAuthentication, IsStaffOrReadOnly
from main.models import Product, Comment
from .serializers import (ProductSerializer, 
                          ProductDetailSerializer, 
                          CommentSerializer
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_active__exact=True)
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    authentication_classes = [SessionAuthentication, AdvancedBasicAuthentication]


class ProductMoreDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, AdvancedBasicAuthentication])
@permission_classes((IsAuthenticatedOrReadOnly,))
def comment_CR_api(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments = Comment.objects.filter(is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)