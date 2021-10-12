from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from functools import reduce
import requests
import datetime
import operator
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from deliveryapp.serializers import AddressSerializer
from deliveryapp.serializers import TimeslotSerializer
from deliveryapp.serializers import DeliverySerializer
from deliveryapp.models import Address
from deliveryapp.models import Timeslot
from deliveryapp.models import Delivery

GEOCODING_URL_BASE = "https://maps.googleapis.com/maps/api/geocode/json?address="


def index(request):
    return HttpResponse("deliveryapp index")


@csrf_exempt  # just some request testing
def resolve_address(request):
    search_term = ""
    if request.POST:
        search_term = request.POST.get("searchTerm")
        search_term = search_term.strip().replace(" ", "+")
        res = requests.get(GEOCODING_URL_BASE+search_term +
                           "&key="+settings.API_KEY)

    return HttpResponse(res.text)


class ResolveAddress(APIView):
    def post(self, request, format=None):
        search_term = request.data["searchTerm"]
        search_term = search_term.strip().replace(" ", "+")
        # prepare the search term to appropriate format

        res = requests.get(GEOCODING_URL_BASE+search_term +
                           "&key="+settings.API_KEY)
        res = res.json()["results"][0]  # get the data
        # return HttpResponse(str(res["results"][0]["formatted_address"]))

        addresses = Address.objects.filter(place_id=res["place_id"])
        # if the place with the same place_id already exist, don't add it
        if (len(addresses) > 0):
            return Response({'error': "address already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        type_array = res["types"]
        type_of_address = ",".join(type_array)

        address_serializer = AddressSerializer(data={
            "formatted_address": res["formatted_address"],
            "place_id": res["place_id"],
            "type_of_address": type_of_address
        })  # serialize dict

        if (address_serializer.is_valid()):
            address_serializer.save()
            return Response(address_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': address_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class BookDelivery(APIView):
    def post(self, request, format=None):
        # get data from request
        user = request.data["user"]
        timeslot = request.data["timeslotId"]

        # check if there are already 2 deliveries for one timeslot
        same_timeslots = Delivery.objects.filter(timeslot=timeslot)
        if (len(same_timeslots) >= 2):
            return Response({'error': "too many deliveries for the same timeslot"},
                            status=status.HTTP_400_BAD_REQUEST)

        # serialize
        delivery_serializer = DeliverySerializer(data={
            "user": user,
            "timeslot": timeslot,
            "status": "ordered"
        })

        if (delivery_serializer.is_valid()):
            delivery_serializer.save()
            return Response(delivery_serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': delivery_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class GetDailyDeliveries(APIView):
    def get(self, request, format=None):
        today = datetime.date.today()

        # filter deliveries for today
        deliveries_for_today = Delivery.objects.filter(
            timeslot__start_time__year=today.year,
            timeslot__start_time__month=today.month,
            timeslot__start_time__day=today.day
        )
        delivery_serializer = DeliverySerializer(
            deliveries_for_today, many=True)
        return Response({"items": delivery_serializer.data})


class GetWeeklyDeliveries(APIView):
    def get(self, request, format=None):
        today = datetime.date.today()

        # filter deliveries for current week
        # subtract from current date current day of the week to get monday
        start_week = today - datetime.timedelta(today.weekday())
        # add 7 days to get end of the week
        end_week = start_week + datetime.timedelta(7)
        deliveries_this_week = Delivery.objects.filter(
            timeslot__start_time__range=[start_week, end_week])
        delivery_serializer = DeliverySerializer(
            deliveries_this_week, many=True)
        return Response({"items": delivery_serializer.data})


class CompleteDelivery(APIView):
    def post(self, request, pk, format=None):
        the_delivery = Delivery.objects.get(id=pk)
        the_delivery.status = "complete"
        the_delivery.save()
        return Response({"message": "updated"}, status=status.HTTP_200_OK)


class CancelDelivery(APIView):
    def delete(self, request, pk, format=None):
        the_delivery = Delivery.objects.get(id=pk)
        the_delivery.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)


class GetTimeslotsForAddress(APIView):
    def post(self, request, format=None):
        address = request.data["address"]
        address = address.strip().replace(" ", "+")

        res = requests.get(GEOCODING_URL_BASE+address +
                           "&key="+settings.API_KEY)
        res = res.json()["results"][0]

        address_types = res["types"]

        queryset = Timeslot.objects.all()
        # get tineslots if it has any type from the array of types for formatted address
        queryset = queryset.filter(reduce(operator.and_, (Q(
            type_of_address__contains=a_type) for a_type in address_types)))

        serilized_timeslots = TimeslotSerializer(queryset, many=True)

        return Response(serilized_timeslots.data, status=status.HTTP_200_OK)
