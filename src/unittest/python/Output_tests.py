__author__ = 'mhoyer'

import unittest2
from monitoring_plugin_helper import Output, Metric


class TestMetric(unittest2.TestCase):

    def test_render_simple_perfdata_string_with_empty_metric_list(self):
        metric_list = []
        self.assertEqual("", Output.render_perfdata_string(metric_list))

    def test_render_simple_perfdata_string_with_single_metric(self):
        metric_list = []
        metric_list.append(Metric("label1", 1, "%", None, None, None, None))
        self.assertEqual("'label1'=1%;;;;", Output.render_perfdata_string(metric_list))

    def test_render_simple_perfdata_string_with_multiple_metrics(self):
        metric_list = []
        metric_list.append(Metric("label1", 1, "%", None, None, None, None))
        metric_list.append(Metric("label2", 2, "%", None, None, None, None))
        metric_list.append(Metric("label3", 3, "%", None, None, None, None))
        self.assertEqual("'label1'=1%;;;; 'label2'=2%;;;; 'label3'=3%;;;;", Output.render_perfdata_string(metric_list))

    def test_exit_ok(self):
        with self.assertRaises(SystemExit) as cm:
            Output.exit_ok("Test")
        self.assertEqual(cm.exception, 0)

    def test_exit_warning(self):
        with self.assertRaises(SystemExit) as cm:
            Output.exit_warning("Test")
        self.assertEqual(cm.exception, 1)

    def test_exit_critical(self):
        with self.assertRaises(SystemExit) as cm:
            Output.exit_critical("Test")
        self.assertEqual(cm.exception, 2)

    def test_exit_unknown(self):
        with self.assertRaises(SystemExit) as cm:
            Output.exit_unknown("Test")
        self.assertEqual(cm.exception, 3)