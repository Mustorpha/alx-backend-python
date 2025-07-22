from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(
        source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'phone_number', 'role', 'display_name']
        read_only_fields = ['id']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'body', 'sent_at', 'message_preview']
        read_only_fields = ['id', 'sent_at']

    def get_message_preview(self, obj):
        return obj.body[:30] + '...' if len(obj.body) > 30 else obj.body


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.IntegerField(
        source='participants.count', read_only=True)

    # Basic validation using ValidationError
    title = serializers.CharField(required=False)

    class Meta:
        model = Conversation
        fields = ['id', 'participant_count', 'created_at', 'messages', 'title']
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        if value and len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters.")
        return value