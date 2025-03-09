from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from reservation.models import Service, TimeSlot, Reservation
from django.utils import timezone
import datetime
import uuid

class ServiceAPITestCase(TestCase):
    """测试服务API端点"""
    
    def setUp(self):
        """测试前创建测试数据"""
        self.client = APIClient()
        self.service = Service.objects.create(
            name="测试服务",
            description="这是一个测试服务",
            duration=60,
            price=299.99
        )
        
    def test_get_all_services(self):
        """测试获取所有服务列表"""
        url = reverse('service-list')  # 确保URL名称与你的urls.py中定义的一致
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "测试服务")

class TimeSlotAPITestCase(TestCase):
    """测试时间段API端点"""
    
    def setUp(self):
        """测试前创建测试数据"""
        self.client = APIClient()
        self.service = Service.objects.create(
            name="测试服务",
            description="这是一个测试服务",
            duration=60,
            price=299.99
        )
        
        # 创建今天和明天的时间段
        today = timezone.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        
        self.time_slot_today = TimeSlot.objects.create(
            service=self.service,
            date=today,
            start_time="10:00:00",
            end_time="11:00:00",
            is_available=True
        )
        
        self.time_slot_tomorrow = TimeSlot.objects.create(
            service=self.service,
            date=tomorrow,
            start_time="14:00:00",
            end_time="15:00:00",
            is_available=True
        )
        
    def test_get_available_dates(self):
        """测试获取可用日期列表"""
        url = reverse('timeslot-available-dates')  # 确保URL名称与你的urls.py中定义的一致
        response = self.client.get(f"{url}?service_id={self.service.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 应该有两个日期（今天和明天）
        
    def test_get_time_slots_by_date(self):
        """测试按日期获取时间段"""
        url = reverse('timeslot-list')  # 确保URL名称与你的urls.py中定义的一致
        today = timezone.now().date()
        response = self.client.get(f"{url}?service={self.service.id}&date={today}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['start_time'], "10:00:00")

class ReservationAPITestCase(TestCase):
    """测试预约API端点"""
    
    def setUp(self):
        """测试前创建测试数据"""
        self.client = APIClient()
        self.service = Service.objects.create(
            name="测试服务",
            description="这是一个测试服务",
            duration=60,
            price=299.99
        )
        
        today = timezone.now().date()
        self.time_slot = TimeSlot.objects.create(
            service=self.service,
            date=today,
            start_time="10:00:00",
            end_time="11:00:00",
            is_available=True
        )
        
    def test_create_reservation(self):
        """测试创建预约"""
        url = reverse('reservation-list')  # 确保URL名称与你的urls.py中定义的一致
        data = {
            'service': self.service.id,
            'time_slot': self.time_slot.id,
            'name': '测试用户',
            'email': 'test@example.com',
            'phone': '13800138000',
            'notes': '这是一个测试预约'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().name, '测试用户')
        
        # 检查时间段是否被标记为不可用
        self.time_slot.refresh_from_db()
        self.assertFalse(self.time_slot.is_available)
        
    def test_get_reservation_detail(self):
        """测试获取预约详情"""
        reservation = Reservation.objects.create(
            id=uuid.uuid4(),
            service=self.service,
            time_slot=self.time_slot,
            name='测试用户',
            email='test@example.com',
            phone='13800138000',
            notes='这是一个测试预约',
            status='pending'
        )
        
        url = reverse('reservation-detail', args=[reservation.id])  # 确保URL名称与你的urls.py中定义的一致
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], '测试用户')
        self.assertEqual(response.data['status'], 'pending')
