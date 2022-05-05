from api.serializers import BookReviewSerializer
from books.models import BookReview
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets

class BookReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookReviewSerializer
    queryset = BookReview.objects.all().order_by('-created_at')
    lookup_field = 'pk'
    


# class BookReviewDetailAPIView(APIView):
    
#     # permission_classes = [IsAuthenticated]
    
#     # serializer_class = BookReviewSerializer
#     # queryset = BookReview.objects.all()
#     # lookup_field = 'pk'
    
    
    
#     def get(self, request, pk):
#         book_review = BookReview.objects.get(pk=pk)
        
#         serializer = BookReviewSerializer(book_review)
        
#         return Response(serializer.data)
#     def delete(self, request, pk):
#         book_review = BookReview.objects.get(pk=pk)
#         book_review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def put(self, request, pk):
#         book_review = BookReview.objects.get(pk=pk)
#         serializer = BookReviewSerializer(book_review, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def patch(self, request, pk):
#         book_review = BookReview.objects.get(pk=pk)
#         serializer = BookReviewSerializer(book_review, data=request.data,partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        
# class BookReviewListAPIView(APIView):
#     def get(self, request):
#         book_reviews = BookReview.objects.all().order_by('-created_at')
        
#         paginator = PageNumberPagination()
#         page_object = paginator.paginate_queryset(book_reviews, request)
        
#         serializer = BookReviewSerializer(page_object, many=True)
        
#         return paginator.get_paginated_response(serializer.data)
    
#     def post(self, request):
#         serializer = BookReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)