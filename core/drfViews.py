from django.contrib.auth.models import User, Group

from rest_framework import permissions, generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import *
from .filters import OrderFilter


class UserList(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FreelancerList(generics.ListAPIView):
    queryset = Freelancer.objects.all().order_by('id')
    serializer_class = FreelancerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nickname']
    filterset_fields = ['work_type', 'work_category', 'lessons', 'languages']


class ClientList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class FreelancerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]


class OrdersList(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']
    filterset_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, client=self.request.user.client, in_auction=True)

    
class OrderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnlyClient]


class AcceptedOrdersList(generics.ListCreateAPIView):
    queryset = AcceptedOrder.objects.all().order_by('id')
    serializer_class = AcceptedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=serializer.validated_data['order'].user, freelancer=self.request.user.freelancer)


# ONLY FREELANCER SHOULD BE ABLE TO ADD FILES AND OWNER TO VIEW WHEN paid=True
# Think of something with update method or passing giving access to the serializer to the request with __init__ or somehow else
# class AcceptedOrderDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AcceptedOrder.objects.all().order_by('id')
#     serializer_class = AcceptedOrderSerializer
#     permission_classes = [permissions.IsAuthenticated]
from rest_framework.exceptions import PermissionDenied


class AcceptedOrderDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcceptedOrder.objects.all().order_by('id')
    serializer_class = AcceptedOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # think of smth here...
    # nobody can do anything if paid=False, rn.
    # also check permissions. might help.
    def perform_update(self, serializer):
        accepted_order = self.get_object()
        if accepted_order.paied:
            if self.request.user.groups.filter(name='freelancer').exists():
                serializer.save(freelancer=self.request.user.freelancer)
            elif self.request.user == accepted_order.user:
                serializer.save(user=self.request.user)
            else:
                raise PermissionDenied("You are not authorized to perform this action.")
        else:
            raise PermissionDenied("You can perform this action after the order is paid")



class WorkTypesList(viewsets.ReadOnlyModelViewSet):
    queryset = Work_Type.objects.all().order_by('id')
    serializer_class = WorkTypeSerializer


class WorkCategoriesList(viewsets.ReadOnlyModelViewSet):
    queryset = Work_Category.objects.all().order_by('id')
    serializer_class = WorkCategorySerializer


class LanguagesList(viewsets.ReadOnlyModelViewSet):
    queryset = Language.objects.all().order_by('id')
    serializer_class = LanguageSerializer


class FeedbacksList(viewsets.ReadOnlyModelViewSet):
    queryset = Feedback.objects.all().order_by('id')
    serializer_class = FeedbackSerializer