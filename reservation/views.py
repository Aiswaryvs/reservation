from django.shortcuts import render
from reservation.models import *
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . serializers import *
import datetime
from datetime import datetime

# Create your views here.

#0) user
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    # permission_classes = (AllowAny, )
    def get(self,request,*args,**kwargs):
        user11=User.objects.all()
        serializer=UserRegistrationSerializer(user11,many=1)
        return Response(serializer.data)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            return Response(response, status=status_code)
    
#0.1) crud operations for user
class UserdetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except UserdetailView.DoesNotExist:
            raise Http404  
    def get(self, request, pk, format=None):
        user1 = self.get_object(pk)
        serializer = UserRegistrationSerializer(user1)
        return Response(serializer.data)  
    def put(self, request, pk, format=None):
        user2 = self.get_object(pk)
        serializer = UserRegistrationSerializer(user2, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        user3 = self.get_object(pk)
        user3.delete()
        return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
    

#1) view for roomtype [get and post]
class RoomtypeView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        roomtype1=Roomtype.objects.all()
        serializer=Roomtype_serializer(roomtype1,many=1)
        return Response(serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=Roomtype_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
   
       
       


#1.1) other crud operations   
class RoomtypedetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Roomtype.objects.get(pk=pk)
        except RoomtypedetailView.DoesNotExist:
            raise Http404  

    def get(self, request, pk, format=None):
        roomtype1 = self.get_object(pk)
        serializer = Roomtype_serializer(roomtype1)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        roomtype2 = self.get_object(pk)
        serializer = Roomtype_serializer(roomtype2, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        roomtype3 = self.get_object(pk)
        roomtype3.delete()
        return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
               

# 2) view for rooms [get and post]
class RoomsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        rooms1=Rooms.objects.all()
        serializer=Rooms_serializer(rooms1,many=1)
        return Response(serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=Rooms_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    

#2.1) other crud operations
class Roomdetailview(APIView):
    def get_object(self,pk):
        try:
            return Rooms.objects.get(pk=pk)
        except Roomdetailview.DoesNotExist:
            raise Http404 
    def get(self,request,pk,format=None):
        room1 = self.get_object(pk)
        serializer = Rooms_serializer(room1)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        room2=self.get_object(pk=pk) 
        
        serializer= Rooms_serializer(room2,data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        room3=self.get_object(pk)
        room3.delete()   
        return Response({'message':'Sucessfully Deleted'},status=status.HTTP_204_NO_CONTENT) 

#3) Booking
class BookingView(APIView):
    def get(self,request,*args,**kwargs):
        booking1=Booking.objects.all()
        serializer=Booking_serializer(booking1,many=1)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        try:
            serializer=Booking_serializer(data=request.data) 
            room_id=request.data["room"]
            seats=Rooms.objects.get(id=room_id)
            # rs = kwargs.get("id") 
            # instance = Booking.objects.get(id=rs)
            c_in = request.data["check_in"]
            c_out = request.data["check_out"]
            rm_no= seats.roomno
            print(rm_no)
            print(c_in)
            print(c_out)
            
            print("hello:",seats.room_type.available_rooms)
            # msg1 = f"Your booking for room number{rm_no}from {c_in} to{c_out} has been reserved."
            # print(msg1)
            response={"status":status.HTTP_400_BAD_REQUEST,"message":"Room Reservation Failed"}
            if seats.room_type.available_rooms<=seats.room_type.total_rooms and seats.room_type.available_rooms!=0:
                id = request.data["user"]
                user_email = User.objects.get(id=id)
                email = user_email.email
                if serializer.is_valid():
                    print("hai")
                    serializer.save()
                    seats.room_type.available_rooms= seats.room_type.available_rooms-1
                    print("new seats",seats.room_type.available_rooms)
                    msg1 = f"Your booking for room number{rm_no}from {c_in} to{c_out} has been reserved."
                    print(msg1)
                    seats.room_type.save()
                    send_mail_task.delay(email,msg)
                    response["status"] = status.HTTP_201_CREATED
                    response["message"] = "Reservation Successfull"
                    response["data"] = serializer.data
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "Rooms are unavailable"})
        except Exception:
            return Response(response,status=status.HTTP_400_BAD_REQUEST)     


    # def post(self,request,*args,**kwargs):
    #     try:
    #         serializer=Booking_serializer(data=request.data) 
    #         room_id=request.data["room"]
    #         seats=Rooms.objects.get(id=room_id)
    #         # instance = Booking.objects.get(id=rs)      #for getting date
    #         # check_in1=instance.check_in
    #         # check_in2=instance.check_out
    #         print("check1:")
    #         print("hello12")
    #         print("hello:",seats.room_type.available_rooms)
    #         response={"status":status.HTTP_400_BAD_REQUEST,"message":"Room Reservation Failed"}
    #         if seats.room_type.available_rooms<=seats.room_type.total_rooms and seats.room_type.available_rooms!=0:
    #             id = request.data["user"]
    #             user_email = User.objects.get(id=id)
    #             email = user_email.email
    #             if serializer.is_valid():
    #                 print("hai")
    #                 serializer.save()
    #                 seats.room_type.available_rooms= seats.room_type.available_rooms-1
    #                 print("new seats",seats.room_type.available_rooms)
    #                 #for celery
    #                 # msg1 = f"Your booking for hotel from {place} to {to} on date {date} has been reserved."


    #                 seats.room_type.save()
    #                 response["status"] = status.HTTP_201_CREATED
    #                 response["message"] = "Reservation Successfull"
    #                 response["data"] = serializer.data
    #                 return Response(response, status=status.HTTP_200_OK)
    #             else:
    #                 return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #                 # return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response({"msg": "Rooms are unavailable"})
    #     except Exception:
    #         return Response(response,status=status.HTTP_400_BAD_REQUEST)  



class Bookingdetailview(APIView):
    # def get_object(self,pk):
    #     try:
    #         return Booking.objects.get(pk=pk)
    #     except BookingView.DoesNotExist:
    #         raise Http404
    def get(self,request,**kwargs):
        room1 = kwargs.get("id")
        reservation = Booking.objects.get(id=room1)
        serializer = Booking_serializer(reservation)
        return Response(serializer.data)
    

    def put(self,request,*args,**kwargs):
        rs = kwargs.get("id") 
        print(rs)
        print("helooo")
        room_id=request.data["room"]
        print(room_id)
        seats=Rooms.objects.get(id=room_id)
        instance = Booking.objects.get(id=rs)
        print(instance)
        serializer= Booking_serializer(data=request.data, instance=instance)
        if serializer.is_valid():
            print("hai5")
            sts = serializer.validated_data.get("booking_sts")
            print(sts)
            print("hai 6:",instance.check_in)
            price1=seats.room_type.price

            #total_price calculations
            check_in1=instance.check_in
            check_in2=instance.check_out
            print("check1:",check_in1)
            checkin_object1 = datetime.strptime(instance.check_in, '%Y-%m-%d %H:%M:%S')
            print("aaa:",checkin_object1)
            # YY-MM-DD H:MI:SS
            checkout_object2 = datetime.strptime(check_in2, "%Y-%m-%d %H:%M:%S")
            s1=int(checkin_object1.day)
            print("dateeeee:",s1)
            s2=checkout_object2.day
            days1=abs(s1-s2)
            instance.total_amount=days1*price1
            print("total price:",instance.total_amount)

            instance.booking_sts = sts
            instance.save()
            print("hai7")
            if sts=="CANCELLD":
                seats.room_type.available_rooms = seats.room_type.available_rooms+1
                seats.room_type.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

    def delete(self,request,**kwargs):
        booking2=kwargs.get("id")
        reservation = Booking.objects.get(id=booking2)
        reservation.delete()
        return Response({'message':'Sucessfully Deleted'},status=status.HTTP_204_NO_CONTENT)            

