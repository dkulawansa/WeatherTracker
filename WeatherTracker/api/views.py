from .serializers import MeasurementsSerializer
import json
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from functools import reduce

from collections import defaultdict

mesurements_store = defaultdict(lambda: defaultdict(dict))


class WeatherTracker(APIView):
    """
    Calculate stats, or create a new measurements.
    """
    def get(self, request, format=None, **kwargs):

        if kwargs.get('data'):
            kwargs = kwargs.get('data')
        stats = [x.strip() for x in kwargs['stat'].split(',')]
        metrics = [x.strip() for x in (kwargs['metric']).split(',')]
        fromDT = kwargs['fromDateTime']
        toDT = kwargs['toDateTime']
        temperatures = []
        dewPoints = []
        precipitations = []
        Statistics =[]
        for metric in metrics:
            i = metrics.index(metric)
            for date_time, data in mesurements_store.items():
                if not isinstance(date_time, str):
                    continue
                if not data:
                    continue
                if not len(data) > i:
                    continue
                if date_time >= fromDT and date_time <= toDT:
                    if metric == 'temperature':
                        temperatures.append(data[i].get(metric))
                    elif metric == 'precipitation':
                        precipitations.append(data[i].get(metric))
                    elif metric == 'dewPoint':
                        if not data[i].get(metric) == None:
                            dewPoints.append(data[i].get(metric))
        for stat in stats:
            if stat == 'average':
                if temperatures:
                    average_temperature = reduce(lambda x, y: x+y, temperatures)/ len(temperatures)
                    Statistics.append( ('avg_temperature', average_temperature))
                if precipitations:
                    average_precipitations = reduce(lambda x, y: x + y, precipitations) / len(precipitations)
                    Statistics.append(('avg_precipitations', average_precipitations))
                if dewPoints:
                    average_dewPoints = reduce(lambda x, y: x + y, dewPoints) / len(dewPoints)
                    Statistics.append(('average_dewPoints', average_dewPoints))
            elif stat == 'max':
                if temperatures:
                    max_temperature = reduce(lambda a, b: a if (a>b) else b, temperatures)
                    Statistics.append(('max_temperature', max_temperature))
                if precipitations:
                    max_precipitations = reduce(lambda a, b: a if (a>b) else b, precipitations)
                    Statistics.append(('max_precipitations', max_precipitations))
                if dewPoints:
                    max_dewPoints = reduce(lambda a, b: a if (a>b) else b, dewPoints)
                    Statistics.append(('max_dewPoints', max_dewPoints))
            elif stat == 'min':
                if temperatures:
                    min_temperature = reduce(lambda a, b: b if (a>b) else a, temperatures)
                    Statistics.append(('min_temperature', min_temperature))
                if precipitations:
                    min_precipitations = reduce(lambda a, b: b if (a>b) else a, precipitations)
                    Statistics.append(('min_precipitations', min_precipitations))
                if dewPoints:
                    min_dewPoints = reduce(lambda a, b: b if (a>b) else a, dewPoints)
                    Statistics.append(('min_dewPoints', min_dewPoints))
        for lst in Statistics:
            if not lst:
                Statistics.pop(lst)
        return Response(Statistics, status=200)

    def post(self, request, format=None):
        """
        Create measurement instance in memory
        """
        serializer = MeasurementsSerializer(data=request.data)
        if serializer.is_valid():
            timestamp = serializer.data['timestamp']
            metrics = serializer.data['metrics']
            mesurements_store[timestamp] = metrics
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class WeatherTrackerDetail(APIView):
    """
    Retrieve an specifiv metric instance.
    """
    def get(self, request, pk, format=None):
        new_pk = pk[:-5] + 'Z'
        measurements = mesurements_store[new_pk]
        if measurements:
            measurements.insert(0, {'timestamp': pk})
            data = json.dumps(measurements)
            return Response(measurements, status=200)
        else:
            return Response(status=404)


def convertStrToDateTime(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')