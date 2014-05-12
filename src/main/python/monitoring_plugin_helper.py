__author__ = 'mhoyer'

import sys
import numbers

class Metric():

    def __init__(self, label, value, uom, warn, crit, min, max):
        self.label = label
        self.value = value
        self.uom = uom
        self.warn = warn
        self.crit = crit
        self.min = min
        self.max = max
        self.validate()

    @staticmethod
    def validate_uom(uom):
        valid_uom = ['%', 's', 'ms', 'us', 'c', 'B', 'KB', 'MB', 'GB', 'TB']

        if uom:
            if not uom in valid_uom:
                raise ValueError("UOM is invalid, use one of: " + ', '.join(valid_uom))
        return True

    @staticmethod
    def validate_numeric_value(value):
        if not isinstance(value, numbers.Number):
            raise ValueError("Value must be numeric, got " + str(value) + " (" + str(type(value)) + ")")
        return True

    @staticmethod
    def validate_string(value):
        if not isinstance(value, basestring):
            raise ValueError("Value must be a string, got " + str(value) + " (" + str(type(value)) + ")")
        return True

    def validate(self):
        # mandatory params must be given
        if not self.label:
            raise ValueError("Metric has no label")
        if not self.value:
            raise ValueError("Metric has no value")

        self.validate_numeric_value(self.value)
        self.validate_uom(self.uom)

        # optional params
        if self.warn:
            self.validate_numeric_value(self.warn)
        if self.crit:
            self.validate_numeric_value(self.crit)
        if self.min:
            self.validate_numeric_value(self.min)
        if self.max:
            self.validate_numeric_value(self.max)

    def get_perfdata_string(self):

        perfdata_string = "'{0}'={1}".format(self.label, self.value)
        if self.uom:
            perfdata_string += self.uom
        if self.warn:
            perfdata_string += ';' + str(self.warn) + ';'
        if self.crit:
            perfdata_string += str(self.crit) + ';'
        if self.min:
            perfdata_string += str(self.min) + ';'
        if self.max:
            perfdata_string += str(self.max)
        return perfdata_string


class Output():

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

    def get_perfdata_string(perfdata_list):
        for item in perfdata_list:
            item