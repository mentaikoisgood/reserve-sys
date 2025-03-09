from rest_framework import serializers
from .models import Service, TimeSlot, Reservation

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'date', 'start_time', 'end_time', 'service', 'service_name', 'is_available']

class ReservationSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    time_slot_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = ['id', 'service', 'service_name', 'time_slot', 'time_slot_display', 
                 'name', 'email', 'phone', 'notes', 'status', 'created_at']
        read_only_fields = ['id', 'created_at', 'status']
    
    def get_time_slot_display(self, obj):
        return f"{obj.time_slot.date} {obj.time_slot.start_time}-{obj.time_slot.end_time}"
    
    def validate(self, data):
        """
        检查时间段是否可用
        """
        time_slot = data.get('time_slot')
        if not time_slot.is_available:
            raise serializers.ValidationError("该时间段已被预约")
        return data 