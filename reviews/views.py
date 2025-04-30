from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from .pagination import ReviewPagination
from rest_framework.permissions import AllowAny
from core.permissions import IsReviewOwner, IsReviewOwnerOrAdmin, IsEnrolledAndCompleted, IsOwnerOrAdmin


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_permissions(self):
        if self.action == 'create':
            return [IsEnrolledAndCompleted()]
        elif self.action == 'update':
            return [IsReviewOwner()]
        elif self.action == 'destroy':
            return [IsReviewOwnerOrAdmin()]
        elif self.action == 'course_reviews':
            return [AllowAny()]
        elif self.action == 'user_reviews':
            return [IsOwnerOrAdmin()]
        return [AllowAny()]

    @action(detail=False, methods=['get'], url_path='course/(?P<course_id>[^/.]+)', name='course_reviews')
    def course_reviews(self, request, course_id=None):
        reviews = Review.objects.filter(course_id=course_id)
        if not reviews.exists():
            return Response({"detail": "No reviews found."}, status=404)

        self.check_object_permissions(request, reviews.first())
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)', name='user_reviews')
    def user_reviews(self, request, user_id=None):
        reviews = Review.objects.filter(user_id=user_id)
        if not reviews.exists():
            return Response({"detail": "No reviews found."}, status=404)

        self.check_object_permissions(request, reviews.first())
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
