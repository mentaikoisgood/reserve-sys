from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, TimeSlot, Reservation
from .serializers import ServiceSerializer, TimeSlotSerializer, ReservationSerializer
from django.core.mail import send_mail
from django.conf import settings
import datetime

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'service']
    ordering_fields = ['date', 'start_time']
    
    @action(detail=False, methods=['get'])
    def available_dates(self, request):
        """获取有可用时间段的日期列表"""
        service_id = request.query_params.get('service_id')
        
        # 获取今天及以后的日期
        today = datetime.date.today()
        
        # 基础查询集
        queryset = TimeSlot.objects.filter(date__gte=today, is_available=True)
        
        # 如果提供了服务ID，则按服务过滤
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        
        # 获取不重复的日期
        dates = queryset.values_list('date', flat=True).distinct().order_by('date')
        
        return Response(dates)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # 发送确认邮件
        reservation = serializer.instance
        self.send_confirmation_email(reservation)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def send_confirmation_email(self, reservation):
        """发送预约确认邮件"""
        subject = f'预约确认 - {reservation.service.name}'
        message = f"""
        尊敬的 {reservation.name}，

        感谢您的预约。以下是您的预约详情：

        服务：{reservation.service.name}
        日期：{reservation.time_slot.date}
        时间：{reservation.time_slot.start_time} - {reservation.time_slot.end_time}
        预约号：{reservation.id}

        如需更改或取消预约，请联系我们。

        谢谢！
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [reservation.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"发送邮件失败: {e}") 