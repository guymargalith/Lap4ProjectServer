from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import CompetitionSerializer, ScoreSerializer, LeaderboardSerializer, UserCompsSerializer
from users.serializers import UserSerializer
from .models import User, Competition, Score
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes=[AllowAny]
   

class CompetitionView(viewsets.ModelViewSet):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    @action(detail=False, methods=['post'] )
    def user_comps(self, request):
        print(request)
        competitions=Competition.objects.filter(scores__user_id= request.data.get('user_id')).order_by('-scores__last_updated')

        print(competitions)
        page = self.paginate_queryset(competitions)
        if page is not None:
            serializer = UserCompsSerializer(page, many=True, context={"user_id": request.data.get('user_id')})
            print(serializer.data)
            return self.get_paginated_response(serializer.data)

            
        serializer = UserCompsSerializer(competitions, many=True, context={"user_id": request.data.get('user_id')})
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def get_leaderboard(self, request, pk=None):
        competition=Competition.objects.get(id=pk)
        print(competition)
        page = self.paginate_queryset(competition)
        print(page)
        if page is not None:
            serializer = LeaderboardSerializer(page, many=True)
            print(serializer.data)
            return self.get_paginated_response(serializer.data)

            
        serializer = LeaderboardSerializer(competition)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public(self, request):
        competitions = Competition.objects.filter(type_of_competition = 2).order_by('-id')
        page = self.paginate_queryset(competitions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer.data)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(competitions, many=True)
        return Response(serializer.data)


class ScoreView(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    queryset = Score.objects.all()
    permission_classes=[AllowAny]

