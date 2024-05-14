from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import RealEstate
from .serializers import RealEstateSerializer

User = get_user_model()

# many=True needs to extract lists from serializer, otherwise serializer would expect a single value and get error
# Create your views here.
class RealEstateManageView(GenericAPIView):
    queryset = RealEstate
    serializer_class = RealEstateSerializer

    def get(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"message": "User must be realtor to retrieve realestate data"}, status=status.HTTP_403_FORBIDDEN)
            
            slug = request.query_params.get('slug')

            if not slug:
                realestate = RealEstate.objects.order_by('-created_at').filter(realtor=user.id)
                serializer = RealEstateSerializer(realestate, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            
            if not RealEstate.objects.filter(
                realtor=user.id,
                slug=slug
            ).exists():
                return Response({"message": "Realestate data are not found"}, status=status.HTTP_404_NOT_FOUND)
            
            realestate = RealEstate.objects.get(realtor=user.id, slug=slug)
            serializer = RealEstateSerializer(realestate)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "Something went wrong when retrieving realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"message": "User must be realtor to post realestate data"}, status=status.HTTP_403_FORBIDDEN)
            else:
                request.data["realtor"] = user.id
                data = RealEstateSerializer(data=request.data)
                if data.is_valid():
                    realestate = data.save()
                    return Response({"message": "Created successfully"}, status=status.HTTP_201_CREATED)
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong when posting realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"message": "User must be realtor to update realestate data"}, status=status.HTTP_403_FORBIDDEN)
            
            data = request.data
            data["realtor"] = user.id
            slug = data['slug']

            if not RealEstate.objects.filter(
                realtor=user.id,
                slug=slug
            ).exists():
                return Response({"message": "Realestate data are not found"}, status=status.HTTP_404_NOT_FOUND)

            realestate = RealEstate.objects.get(realtor=user.id, slug=slug)
            serializer = RealEstateSerializer(realestate, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong when updating realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"message": "User must be realtor to update realestate data"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                slug = request.query_params.get('slug')
            except:
                return Response({"message": "Slug is not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data
            is_published = data["is_published"]
            
            if not RealEstate.objects.filter(
                realtor=user.id,
                slug=slug
            ).exists():
                return Response({"message": "Realestate data are not found"}, status=status.HTTP_404_NOT_FOUND)
            
            RealEstate.objects.filter(realtor=user.id, slug=slug).update(is_published=is_published)

            return Response({"message": "Updated successfully"}, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response({"message": "Something went wrong when updating realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({"message": "User must be realtor to update realestate data"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                slug = request.query_params.get('slug')
            except:
                return Response({"message": "Slug is not provided"}, status=status.HTTP_400_BAD_REQUEST)

            if not RealEstate.objects.filter(
                realtor=user.id,
                slug=slug
            ).exists():
                return Response({"message": "Realestate data are not found"}, status=status.HTTP_404_NOT_FOUND)

            RealEstate.objects.filter(realtor=user.id, slug=slug).delete()

            if not RealEstate.objects.filter(
                realtor=user.id,
                slug=slug
            ).exists():
                return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Failed to delete"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"message": "Something went wrong when deleting realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RealEstateDetailView(GenericAPIView):
    queryset = RealEstate
    serializer_class = RealEstateSerializer

    def get(self, request, format=None):
        try:
            slug = request.query_params.get("slug")

            if not slug:
                return Response({"message": "Must provide slug"}, status=status.HTTP_400_BAD_REQUEST)
            
            if not RealEstate.objects.filter(slug=slug, is_published=True).exists():
                return Response({"message": "Published detail with provided slug does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            realestate = RealEstate.objects.get(slug=slug, is_published=True)
            serializer = RealEstateSerializer(realestate)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except:
            return Response({"message": "Something went wrong when retrieving realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RealEstateListView(GenericAPIView):
    queryset = RealEstate
    serializer_class = RealEstateSerializer
    permission_classes=[AllowAny]

    def get(self, request, format=None):
        try:
            if not RealEstate.objects.filter(is_published=True).exists():
                return Response({"message": "Published list does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            realestate = RealEstate.objects.order_by('-created_at').filter(is_published=True)
            serializer = RealEstateSerializer(realestate, many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        except:
            return Response({"message": "Something went wrong when retrieving realestate data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
