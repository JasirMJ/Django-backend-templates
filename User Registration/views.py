import json

from django.http import JsonResponse

from EcommerceSystem.global_variables import *
from EcommerceSystem.Imports import *
from users.serializers import *

def index(request):
    return HttpResponse('Welcome to Ecommerce , site is under developement')

class UsersView(ListAPIView):
    serializer_class = UserSerializers

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def post(self,request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(password=make_password(self.request.data['password']))
        print("user id or object : ",obj.id)

        return Response(
            {
                STATUS: True,
                MESSAGE:"User created "+str(obj.id)
            }
        )

    def put(self,request):
        id = self.request.POST.get("id")
        if not id or id =="":
            return Response({
                STATUS:False,
                MESSAGE:"Required product id as id"
            })

        serializer = UserSerializers(User.objects.filter(id=id).first(), data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        if self.request.POST.get('password'):
            serializer.save(password=make_password(self.request.data['password']))
        else:
            serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )



    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                User.objects.all().exclude(is_staff=True).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all users",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                User.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "users deleted having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )


class AdvancedUserView(ListAPIView):
    serializer_class = AdvancedUserSerializers

    def get_queryset(self):
        queryset = UserDetails.objects.all()
        return queryset

    def post(self, request):


        user_serializer = UserSerializers(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save(password=make_password(self.request.data['password']))

        advanced_user_serializer = AdvancedUserSerializers(data=request.data)
        advanced_user_serializer.is_valid(raise_exception=True)
        advanced_user_serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "User created"
            }
        )

    def put(self, request):
        id = self.request.POST.get("id")
        if not id or id == "":
            return Response({
                STATUS: False,
                MESSAGE: "Required product id as id"
            })

        serializer = AdvancedUserSerializers(User.objects.filter(id=id).first(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if self.request.POST.get('password'):
            serializer.save(password=make_password(self.request.data['password']))
        else:
            serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )

    def delete(self, request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                User.objects.all().exclude(is_staff=True).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all users",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                User.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "users deleted having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )


class UsersRoleView(ListAPIView):
    serializer_class = UserRolesSerializers

    def get_queryset(self):
        queryset = UserRoles.objects.all()
        return queryset

    def post(self,request):
        try:

            serializer = UserRolesSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            print("user id or object : ",obj.id)

            return Response(
                {
                    STATUS: True,
                    MESSAGE:"Role created "+str(obj.id)
                }
            )
        except Exception as e:
            printLineNo()
            return JsonResponse(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

    def put(self,request):
        id = self.request.POST.get("id")
        if not id or id =="":
            return Response({
                STATUS:False,
                MESSAGE:"Required product id as id"
            })

        serializer = UserRolesSerializers(UserRoles.objects.filter(id=id).first(), data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                STATUS: True,
                MESSAGE: "Data updated",
                # "Data": request.data
            }
        )

    def delete(self,request):
        try:
            id = self.request.POST.get('id', "")
            if id == "" or not id:
                UserRoles.objects.all().delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "Deleted all data",
                    }
                )
            else:
                id = json.loads(id)
                print(id)
                UserRoles.objects.filter(id__in=id).delete()
                return Response(
                    {
                        STATUS: True,
                        MESSAGE: "users deleted having id " + str(id),
                    }
                )
        except Exception as e:
            printLineNo()
            return Response(
                {
                    STATUS: False,
                    MESSAGE: str(e),
                    "line_no": printLineNo()
                }
            )

class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
