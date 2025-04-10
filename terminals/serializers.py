from rest_framework import serializers
from .models import Terminal

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')
