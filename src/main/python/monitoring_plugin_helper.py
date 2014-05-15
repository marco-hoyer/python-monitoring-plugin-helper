__author__ = 'mhoyer'

import sys
import numbers

class Metric(object):

    def __init__(self, label, value, uom, warn, crit, min, max):
        self.label = label
        self.value = value
        self.uom = uom
        self.warn = warn
        self.crit = crit
        self.min = min
        self.max = max
        self.validate()

    def __str__(self):
        return self.get_perfdata_string()

    @staticmethod
    def _validate_uom(uom):
        valid_uom = ['%', 's', 'ms', 'us', 'c', 'B', 'KB', 'MB', 'GB', 'TB']

        if uom:
            if not uom in valid_uom:
                raise ValueError("UOM is invalid, use one of: " + ', '.join(valid_uom))
        return True

    @staticmethod
    def _validate_numeric_value(value):
        if not isinstance(value, numbers.Number):
            raise ValueError("Value must be numeric, got " + str(value) + " (" + str(type(value)) + ")")
        return True

    @staticmethod
    def _validate_string(value):
        if not isinstance(value, basestring):
            raise ValueError("Value must be a string, got " + str(value) + " (" + str(type(value)) + ")")
        return True

    @classmethod
    def _validate_label(cls_obj, label):
        if not label:
            raise ValueError("Metric has no label")
        cls_obj._validate_string(label)
        return True

    @classmethod
    def _validate_value(cls_obj, value):
        if not value:
            raise ValueError("Metric has no value")
        cls_obj._validate_numeric_value(value)
        return True

    def validate(self):
        # mandatory params must be given
        self._validate_label(self.label)
        self._validate_value(self.value)

        self._validate_numeric_value(self.value)
        self._validate_uom(self.uom)

        # optional params
        if self.warn:
            self._validate_numeric_value(self.warn)
        if self.crit:
            self._validate_numeric_value(self.crit)
        if self.min:
            self._validate_numeric_value(self.min)
        if self.max:
            self._validate_numeric_value(self.max)

    def get_perfdata_string(self):
        return "'{0}'={1}{2};{3};{4};{5};{6}".format(self.label, self.value, self.uom or '', self.warn or '',
                                                                self.crit or '', self.min or '', self.max or '')


class Output(object):

    def exit_ok(message):
        print "OK: %s" % message
        sys.exit(0)

    def exit_warning(message, perfdata_string):
        print "Warning: %s" % message
        sys.exit(1)

    def exit_critical(message, perfdata_string):
        print "Critical: %s" % message
        sys.exit(2)

    def exit_unknown(message):
        print "Unknown: %s" % message
        sys.exit(3)

    @staticmethod
    def render_perfdata_string(metric_list):
        return ' '.join(str(metric) for metric in metric_list)