from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Item
from .serializers import ItemSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import redis
import json
import logging
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
logger = logging.getLogger(__name__)


class CreateItemView(APIView):
    '''Create Item API'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                if Item.objects.filter(name=serializer.validated_data['name']).exists():
                    logger.error(f"Item with name {serializer.validated_data['name']} already exists.")
                    return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)

                item = serializer.save(created_by=request.user)
                logger.info(f"Item {serializer.validated_data['name']} created by {request.user}.")
                return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)

            logger.error(f"Invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReadItemView(APIView):
    '''get details of an item by id'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        try:
            cache_key = f'item_{item_id}'
            cached_item = redis_client.get(cache_key)

            if cached_item:
                logger.info(f"Cache hit for item ID: {item_id}")
                return Response(json.loads(cached_item), status=status.HTTP_200_OK)

            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item)
            redis_client.set(cache_key, json.dumps(serializer.data), ex=60*10)
            logger.info(f"Cache miss for item ID: {item_id}. Data cached.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error reading item {item_id}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update item view
class UpdateItemView(APIView):
    '''This API updates the item data'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)

            if item.created_by != request.user:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                redis_client.delete(f'item_{item_id}')
                logger.info(f"Item {item_id} updated by {request.user}.")
                return Response(serializer.data, status=status.HTTP_200_OK)

            logger.error(f"Invalid data for item {item_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete item view
class DeleteItemView(APIView):
    '''This API deletes an item by id'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = get_object_or_404(Item, id=item_id)

            if item.created_by != request.user:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            item.delete()
            redis_client.delete(f'item_{item_id}')
            logger.info(f"Item {item_id} deleted by {request.user}.")
            return Response({"success": "Item deleted."}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
