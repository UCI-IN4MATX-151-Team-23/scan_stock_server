import base64
import io
import json
import qrcode
import qrcode.image.svg
from barcode import Code128
from barcode.writer import SVGWriter
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from web.models import Item, ItemTemplate, Tag

from web.serializers import ItemSerializer, ItemTemplateSerializer, UserSerializer

@api_view(['POST'])
def create_user(request):
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    if User.objects.filter(email=email).count() != 0 or User.objects.filter(username=username).count() != 0:
        return Response({'error': 'A user with the given username and/or email already exist.'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username, email, password)
    return Response(UserSerializer(user).data)


def vertify_user(request, user_id):
    result = User.objects.filter(id=user_id)
    if result.count() == 0:
        return Response({'error': 'A user with the given id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    user = result.first()
    if user.id != request.user.id:
        return Response({'error': "You don't have access to the info of the user with given id."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    vertify_result = vertify_user(request, user_id)
    if(vertify_result):
        return vertify_result
    return Response(UserSerializer(request.user).data)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_items_by_id(request, user_id):
    vertify_result = vertify_user(request, user_id)
    if(vertify_result):
        return vertify_result
    return Response(ItemSerializer(request.user.item_set.all(), many=True).data)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    return Response(UserSerializer(request.user).data)

def set_item_attrs_and_tags(request, item):
    if 'attrs' in request.data:
        item.attrs = json.dumps(request.data['attrs'])
    if 'tags' in request.data:
        tags = request.data['tags']
        existing_tags = set(x.tag for x in Tag.objects.filter(tag__in = tags))
        Tag.objects.bulk_create([Tag(tag=x) for x in (set(tags) - existing_tags)])
        item.tags.set(Tag.objects.filter(tag__in = tags))
    item.save()

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_item(request):
    item = Item(creator=request.user)
    item.save()
    set_item_attrs_and_tags(request, item)
    tmp_stream = io.BytesIO()
    img = qrcode.make(str(item.id), image_factory=qrcode.image.svg.SvgImage)
    img.save(tmp_stream)
    item.qrcode = base64.b64encode(tmp_stream.getvalue()).decode('ascii')
    tmp_stream = io.BytesIO()
    Code128(str(item.id), SVGWriter()).write(tmp_stream)
    item.barcode = base64.b64encode(tmp_stream.getvalue()).decode('ascii')
    item.save()
    return Response(ItemSerializer(item).data)

class ItemView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,item_id,  format=None):
        item = Item.objects.filter(id=item_id).first()
        if(not item):
            return Response({'error': 'An item with the given id does not eixst'}, status=status.HTTP_404_NOT_FOUND)
        verify_result = vertify_user(request, item.creator.id)
        if(verify_result):
            return verify_result
        return Response(ItemSerializer(item).data)

    def put(self, request, item_id, format=None):
            item = Item.objects.filter(id=item_id).first()
            if(not item):
                return Response({'error': 'An item with the given id does not eixst'}, status=status.HTTP_404_NOT_FOUND)
            verify_result = vertify_user(request, item.creator.id)
            if(verify_result):
                return verify_result
            set_item_attrs_and_tags(request, item)
            return Response()

    

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_item_templates(_):
    item_templates = ItemTemplate.objects.all()
    return Response(ItemTemplateSerializer(item_templates, many=True).data)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_item_template_by_id(_, item_template_id):
    item_template = ItemTemplate.objects.filter(id=item_template_id)
    if(not item_template):
        return Response({'error': 'An item template with the given id does not eixst'}, status=status.HTTP_404_NOT_FOUND)
    return Response(ItemTemplateSerializer(item_template).data)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def fuzzy_search_by_keywords(request):
    keywords = request.query_params.get("keywords")
    # TODO: implement fuzzy search
    return Response()
