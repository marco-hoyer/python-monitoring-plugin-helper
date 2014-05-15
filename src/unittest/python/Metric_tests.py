__author__ = 'mhoyer'

import unittest2
from monitoring_plugin_helper import Metric


class TestMetric(unittest2.TestCase):

    def test_validate_uom(self):

        self.assertTrue(Metric._validate_uom(None))
        self.assertTrue(Metric._validate_uom(''))
        self.assertTrue(Metric._validate_uom('%'))
        self.assertTrue(Metric._validate_uom('s'))
        self.assertTrue(Metric._validate_uom('us'))
        self.assertTrue(Metric._validate_uom('ms'))
        self.assertTrue(Metric._validate_uom('c'))
        self.assertTrue(Metric._validate_uom('B'))
        self.assertTrue(Metric._validate_uom('KB'))
        self.assertTrue(Metric._validate_uom('MB'))
        self.assertTrue(Metric._validate_uom('TB'))

        with self.assertRaises(ValueError):
            self.assertFalse(Metric._validate_uom('A'))
        with self.assertRaises(ValueError):
            self.assertFalse(Metric._validate_uom('Test'))
        with self.assertRaises(ValueError):
            self.assertFalse(Metric._validate_uom(2))

    def test_validate_numeric_value(self):

        self.assertTrue(Metric._validate_numeric_value(1.2))
        self.assertTrue(Metric._validate_numeric_value(100))

        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_numeric_value(None))
        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_numeric_value('A'))
        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_numeric_value("Test"))

    def test_validate_string(self):

        self.assertTrue(Metric._validate_string(""))
        self.assertTrue(Metric._validate_string('A'))
        self.assertTrue(Metric._validate_string("Test BB"))

        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_string(None))
        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_string(5))
        with self.assertRaises(ValueError):
            self.assertTrue(Metric._validate_string(5.1))

    def test_validate(self):

        metric = Metric("label", 1, "%", None, None, None, None)
        metric = Metric("label", 1, "%", 10, 20, 0, 3)
        with self.assertRaises(ValueError):
            Metric("label", "1", "%", None, None, None, None)
        with self.assertRaises(ValueError):
            Metric("label", 1, "%", None, None, 'A', None)

    def test_get_perfdata_string_with_minimum_values(self):

        metric = Metric("My Service Metric", 20, None, None, None, None, None)
        reference_string = "'My Service Metric'=20;;;;"
        self.assertEqual(reference_string, metric.get_perfdata_string())

    def test_get_perfdata_string_with_min_max_only(self):

        metric = Metric("My Service Metric", 20, None, None, None, 4, 10)
        reference_string = "'My Service Metric'=20;;;4;10"
        self.assertEqual(reference_string, metric.get_perfdata_string())

    def test_get_perfdata_string_with_min_max_uom(self):

        metric = Metric("My Service Metric", 20, 's', None, None, 4, 10)
        reference_string = "'My Service Metric'=20s;;;4;10"
        self.assertEqual(reference_string, metric.get_perfdata_string())

    def test_get_perfdata_string_with_thresholds_only(self):

        metric = Metric("My Service Metric", 20, None, 4, 10, None, None)
        reference_string = "'My Service Metric'=20;4;10;;"
        self.assertEqual(reference_string, metric.get_perfdata_string())

    def test_get_perfdata_string(self):

        metric = Metric("My Service Metric", 2, '%', 20, 50, 1.2, 5)
        reference_string = "'My Service Metric'=2%;20;50;1.2;5"
        self.assertEqual(reference_string, metric.get_perfdata_string())