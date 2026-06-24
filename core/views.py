from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from reviews_app.models import Reviews
from offers_app.models import Offers
from django.contrib.auth import get_user_model
from django.db.models import Avg
User = get_user_model()


class CountStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reviews = Reviews.objects.all().count()

        average_rating = Reviews.objects.aggregate(Avg('rating'))
        business_profile_count = User.objects.filter(type='business').count()
        offer_count = Offers.objects.all().count()

        if average_rating['rating__avg'] is not None:
            self.responsed_data = {
                "review_count": reviews,
                "average_rating": round(average_rating['rating__avg'], 1),
                "business_profile_count": business_profile_count,
                "offer_count": offer_count
            }
        else:
            self.responsed_data = {
                "review_count": reviews,
                "average_rating": 0,
                "business_profile_count": business_profile_count,
                "offer_count": offer_count
            }
        return Response(self.responsed_data, status=status.HTTP_200_OK)
