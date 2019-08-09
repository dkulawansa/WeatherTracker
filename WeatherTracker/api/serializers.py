from rest_framework import serializers, fields

from rest_framework import serializers


class MeasurementsSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField(required=True)
    #timestamp = fields.DateTimeField(input_formats=[%Y-%m-%dT%H:%M:%S.%fZ], required=True)
    metrics = fields.ListField(
        child=fields.DictField(child=fields.FloatField()),
        help_text='Any matric field like temperature, dew point, precipitation or can be added new one in the future',
    )
