from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from requests import request as rq
from matplotlib import pyplot as plt
from .models import User
from .form import ConfigForm
from .serializers import UserSerializer


def home(request):
	
	return render(request, 'routes/home.html')
	
	
	
def login(request):
	
	return render(request, "routes/login.html")



def configs(request):

	if request.method == "POST":
		
		form = ConfigForm(request.POST)

		print(form)

		if form.is_valid() and request.COOKIES.get("access"):

			try:

				token = AccessToken(request.COOKIES.get("access"))

				user = User.objects.get(id=token.payload.get("id"))

				username = form.data.get("username")
				email = form.data.get("email")
				password = form.data.get("password")

				user.username = username if username else user.username
				user.email = email if email else user.email
				

				if password:
					user.set_password(password)

				user.save()
			
			except:pass

			print("oi")

		return redirect("/")

	return render(request, "routes/configs.html")


@api_view(["GET"])
def get_csrf(request):

	if request.headers.get("Origin"): return Response({"csrf":get_token(request)})
	else: return None



@api_view(["GET"])
def get_user(request):

	if request.COOKIES.get("access"):

		try:

			access = AccessToken(request.COOKIES.get("access"))

			user = User.objects.get(id=access.payload.get("id"))

			serializer = UserSerializer(user)
			serializer = serializer.data
			serializer.pop("id")

			return Response({"current_user":serializer})

		except: return Response(None)
	
	elif request.COOKIES.get("refresh"):

		refresh = RefreshToken(request.COOKIES.get("refresh"))

		user = User.objects.get(id=refresh.payload.get("id"))

		serializer = UserSerializer(user)
		serializer = serializer.data
		serializer.pop("id")

		response = Response({"current_user":serializer})
		response.set_cookie("access",refresh.access_token,httponly=True,max_age=refresh.access_token.lifetime)

		return response
	else:
		return Response(None)

# Create your views here.
