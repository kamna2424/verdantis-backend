from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Plant, SensorData
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    SensorDataSerializer
)


# -----------------------------
# USER REGISTRATION
# -----------------------------
class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=201)

        return Response(serializer.errors, status=400)


# -----------------------------
# USER LOGIN
# -----------------------------
class LoginUser(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


# -----------------------------
# PLANT SUGGESTION ENGINE
# -----------------------------
class SuggestPlant(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        moisture = request.data.get("moisture")
        temperature = request.data.get("temperature")
        humidity = request.data.get("humidity")

        if moisture is None or temperature is None or humidity is None:
            return Response({"error": "Missing sensor values"}, status=400)

        best_plant = None
        best_score = -9999

        for plant in Plant.objects.all():
            score = 0

            # Moisture score
            if plant.ideal_moisture_min <= moisture <= plant.ideal_moisture_max:
                score += 2
            else:
                score -= 1

            # Temperature score
            if plant.ideal_temp_min <= temperature <= plant.ideal_temp_max:
                score += 2
            else:
                score -= 1

            # Humidity score
            if plant.ideal_humidity_min <= humidity <= plant.ideal_humidity_max:
                score += 2
            else:
                score -= 1

            # Pick highest-scoring plant
            if score > best_score:
                best_score = score
                best_plant = plant

        if best_plant is None:
            return Response({"error": "No suitable plant found"}, status=404)

        return Response({
            "suggested_plant": {
                "name": best_plant.name,
                "description": best_plant.description,
                "image_url": best_plant.image_url,
                "score": best_score
            }
        })


# -----------------------------
# SENSOR DATA API (ESP32 uses this)
# -----------------------------
class SensorDataView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sensor data saved"}, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        data = SensorData.objects.order_by("-timestamp")[:20]
        serializer = SensorDataSerializer(data, many=True)
        return Response(serializer.data)
