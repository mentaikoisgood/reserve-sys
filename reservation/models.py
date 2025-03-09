from django.db import models
from django.utils import timezone
import uuid

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="服务时长（分钟）")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='time_slots')
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time} ({self.service.name})"
    
    class Meta:
        ordering = ['date', 'start_time']

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.service.name} ({self.time_slot})"
    
    def save(self, *args, **kwargs):
        # 当预约被创建或状态改变时，更新时间段的可用性
        if self.status in ['confirmed', 'pending']:
            self.time_slot.is_available = False
        else:
            self.time_slot.is_available = True
        self.time_slot.save()
        super().save(*args, **kwargs) 