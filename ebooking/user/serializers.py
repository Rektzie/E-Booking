from rest_framework  import serializers
from .models import Room
class RoomSerializer(serializers.Serializer):
    id = serializers.AutoField(primary_key=True)
    name = serializers.CharField(max_length=255)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    capacity = serializers.IntegerField()
    room_type = serializers.ForeignKey(Room_type, on_delete=models.CASCADE)