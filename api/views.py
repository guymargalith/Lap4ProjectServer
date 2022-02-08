from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import CompetitionSerializer, ScoreSerializer, LeaderboardSerializer, UserCompsSerializer
from users.serializers import UserSerializer
from .models import User, Competition, Score
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# Create your views here.

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes=[AllowAny]

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     id = self["id"]
    #     user = get_object_or_404(User, id=id)
    #     user.delete()
    #     return Response(status=204)


    

class CompetitionView(viewsets.ModelViewSet):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    @action(detail=False, methods=['post'] )
    def user_comps(self, request):
        print(request)
        competitions=Competition.objects.filter(scores__user_id= request.data.get('user_id'))

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
        competitions = Competition.objects.filter(type_of_competition = 2)
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


    # @action(detail=False, methods=['post'])
    # def get_leaderboard(self, request):
    #     leaderboard = Score.objects.filter(competition_id = request.data['competition_id']).order_by('-score')
    #     page = self.paginate_queryset(leaderboard)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(leaderboard, many=True)
    #     return Response(serializer.data)

