import unittest
from converter import UnitConverter


class TestUnitConverter(unittest.TestCase):
    def setUp(self):
        self.converter = UnitConverter()
    
    def test_weight_conversion_kg_to_g(self):
        result = self.converter.convert_weight(1, 'kg', 'g')
        self.assertEqual(result, 1000)
    
    def test_weight_conversion_g_to_kg(self):
        result = self.converter.convert_weight(1000, 'g', 'kg')
        self.assertEqual(result, 1)
    
    def test_weight_conversion_lb_to_kg(self):
        result = self.converter.convert_weight(1, 'lb', 'kg')
        self.assertAlmostEqual(result, 0.453592, places=5)
    
    def test_length_conversion_m_to_cm(self):
        result = self.converter.convert_length(1, 'm', 'cm')
        self.assertEqual(result, 100)
    
    def test_length_conversion_km_to_m(self):
        result = self.converter.convert_length(1, 'km', 'm')
        self.assertEqual(result, 1000)
    
    def test_length_conversion_ft_to_m(self):
        result = self.converter.convert_length(1, 'ft', 'm')
        self.assertAlmostEqual(result, 0.3048, places=4)
    
    def test_invalid_weight_unit(self):
        with self.assertRaises(ValueError):
            self.converter.convert_weight(1, 'invalid', 'kg')
    
    def test_invalid_length_unit(self):
        with self.assertRaises(ValueError):
            self.converter.convert_length(1, 'invalid', 'm')
    
    def test_get_available_weight_units(self):
        units = self.converter.get_available_weight_units()
        self.assertIn('kg', units)
        self.assertIn('g', units)
        self.assertIn('lb', units)
    
    def test_get_available_length_units(self):
        units = self.converter.get_available_length_units()
        self.assertIn('m', units)
        self.assertIn('cm', units)
        self.assertIn('ft', units)


if __name__ == '__main__':
    unittest.main()