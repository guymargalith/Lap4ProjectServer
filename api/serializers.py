from rest_framework import serializers
from .models import Competition, Score
from django.contrib.auth.models import User
from users.serializers import UserSerializer

class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    
    def get_user(self,obj):
        print(obj.user_id)
        user = User.objects.get(username=obj.user_id)
        print(user)
        return UserSerializer(user).data
    
    class Meta:
        model = Score
        fields = ('id', 'competition_id', 'user_id', 'score', 'last_updated', 'user')

# class UserSerializer(serializers.ModelSerializer):
#     scores_user = ScoreSerializer(many=True, required=False)
#     class Meta:
#         model = User
#         fields = ('id', 'user_name', 'email','is_active', 'account_type', 'scores_user')

class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'units', 'frequency','type_of_competition', 'end_date', 'host_id', 'completed')


class LeaderboardSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField(method_name='get_scores')

    def get_scores(self, obj):
        qset = Score.objects.filter(competition_id = obj.id).order_by('-score')
        return ScoreSerializer(qset, many=True, required=False).data
    
    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'units', 'frequency','type_of_competition', 'end_date', 'host_id', 'completed', 'scores') 

class UserCompsSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField(method_name='get_score')

    def get_score(self, obj):
        print(self.context.get('user_id'))
        qset = Score.objects.filter(competition_id = obj.id, user_id = self.context.get('user_id'))
        print(qset)
        return ScoreSerializer(qset[0], required=False).data
    
    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'units', 'frequency','type_of_competition', 'end_date', 'host_id', 'completed', 'score') 

