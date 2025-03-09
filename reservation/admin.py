from django.contrib import admin
from .models import Service, TimeSlot, Reservation

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name', 'description')
    inlines = [TimeSlotInline]

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'service', 'is_available')
    list_filter = ('date', 'service', 'is_available')
    search_fields = ('service__name',)
    date_hierarchy = 'date'

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('预约信息', {
            'fields': ('id', 'service', 'time_slot', 'status')
        }),
        ('客户信息', {
            'fields': ('name', 'email', 'phone', 'notes')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
