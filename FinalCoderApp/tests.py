from django.test import TestCase
from .models import *

# Create your tests here.
class DeportesTest(TestCase):
    
    def setUp(self):
        Deporte.objects.create(deporte="Hockey", profesor="Amalia Serrano", horario="Lun y Mie 18hs")
        
    def test_deporte_nombre(self):
        deportes = Deporte.objects.get(profesor="Amalia Serrano", horario="Lun y Mie 18hs")
        self.assertEqual(deportes.deporte, "Hockey")
        
class DeporteTest(TestCase):
    
    def setUp(self):
        Deporte.delete(id=1, deporte="Tenis", profesor="Romina Palacios")