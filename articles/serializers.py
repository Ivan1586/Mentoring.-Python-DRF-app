from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from articles.models import Article


User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('username', 'bio', 'image', 'following')
        
    def get_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.followers.filter(pk=user.id).exists()
        return False

    
class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    description = serializers.CharField(source='summary')
    content = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    favorites = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'content', 'created',
                  'updated', 'favorites', 'favorites_count', 'author']
        read_only_fields = ['slug', 'created', 'updated', 'author']
    
    def get_author(self, obj):
        request = self.context.get('request') 
        # serializer = AuthorSerializer(request.user, context={'request': request})
        serializer = AuthorSerializer(obj.author, context={'request': request})
        return serializer.data
    
    def get_favorites(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return instance.favorites.filter(pk=request.user.pk).exists()
        return False
    
    def get_favorites_count(self, instance):
        return instance.favorites.count()
       
    def create(self, validated_data):
        # tags = validated_data.pop('tags')
        article = Article(
            author=self.context['request'].user,
            **validated_data
        )
        article.save()
        # article.tags.add(*tags)
        return article
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        instance.tags.clear()
        instance.tags.add(*tags)
        
        return instance
    
    
class TagSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.CharField()
    )
        