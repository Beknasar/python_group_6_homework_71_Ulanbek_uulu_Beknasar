from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
import json
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from api_v1.serializers import ProductSerializer, UserSerializer, OrderSerializer
from webapp.models import Product, Order


@ ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


# class OrderListView(View):
#     def get(self, request, *args, **kwargs):
#         objects = Order.objects.all()
#         slr = OrderSerializer(objects, many=True)
#         return JsonResponse(slr.data, safe=False)
#
#
# class OrderCreateView(View):
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         slr =OrderSerializer(data=data)
#         if slr.is_valid():
#             order = slr.save()
#             return JsonResponse(slr.data, safe=False)
#         else:
#             response = JsonResponse(slr.errors, safe=False)
#             response.status_code = 400
#             return response
class OrderViewSet(ViewSet):
   queryset = Order.objects.all()

   def list(self, request):
       objects = Order.objects.all()
       slr = OrderSerializer(objects, many=True, context={'request': request})
       return Response(slr.data)

   def create(self, request):
       slr = OrderSerializer(data=request.data, context={'request': request})
       if slr.is_valid():
           order = slr.save()
           return Response(slr.data)
       else:
           return Response(slr.errors, status=400)


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def list(self, request):
        objects = Product.objects.all()
        slr = ProductSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = ProductSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(product, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        slr = ProductSerializer(data=request.data, instance=product, context={'request': request})
        if slr.is_valid():
            product = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'pk': pk})


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer