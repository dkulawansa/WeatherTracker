from __future__ import unicode_literals
from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from .views import WeatherTracker, WeatherTrackerDetail
import json


class WeatherTrackerTest1(TestCase):
    """This class defines the test suite for the WeatherTracker view"""

    def setUp(self):
        # Every test needs access to the request factory.
        #load some initial data
        self.view = WeatherTracker.as_view()
        self.factory = APIRequestFactory()
        listData = [{"timestamp": "2019-07-19T18:20:00.000Z", "metrics": [{"temperature": 28.5}, {"dewPoint": 18.6}, {"precipitation": 80.0}]},
                    ]

        for data in listData:
            request = self.factory.post('/measurements', json.dumps(data), content_type='application/json')
            response = self.view(request)

    def test_post_measurements_happy_path(self):

        data = {"timestamp": "2015-09-01T16:00:00.000Z", "metrics":[{"temperature":28.5}, {"dewPoint":18.6}, {"precipitation":80.0}]}
        request = self.factory.post('/measurements', json.dumps(data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_post_measurements_no_timestamp_in_input_data(self):
        data = {"metrics":[{"temperature":28.5}, {"dewPoint":18.6}, {"precipitation":80.0}]}
        request = self.factory.post('/measurements', json.dumps(data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_post_measurements_with_invalid_data_input(self):

        data = {"metrics":[{"temperature":'xx.xx'}, {"dewPoint":18.6}, {"precipitation":80.0}]}
        request = self.factory.post('/measurements', json.dumps(data), content_type='application/json')
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_get_measurements_happy_path(self):
        view = WeatherTrackerDetail.as_view()
        factory = APIRequestFactory()
        expected = [{'timestamp': '2019-07-19T18:20:00.000Z'}, {'temperature': 28.5}, {'dewPoint': 18.6},
                    {'precipitation': 80.0}]
        request = factory.get('/measurements/2019-07-19T18:20:00.000Z')
        response = view(request, '2019-07-19T18:20:00.000Z')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    def test_get_measurements_for_non_exist_measurement(self):
        view = WeatherTrackerDetail.as_view()
        factory = APIRequestFactory()
        request = factory.get('/measurements/2015-09-01T16:50:00.000Z')
        response = view(request, '2015-09-01T16:50:00.000Z')
        self.assertEqual(response.status_code, 404)

class WeatherTrackerTest2(TestCase):
    """This class defines the test suite for the WeatherTracker view"""

    def setUp(self):
        # Every test needs access to the request factory.
        #load some initial data
        self.view = WeatherTracker.as_view()
        self.factory = APIRequestFactory()

        listData = [{"timestamp": "2015-09-01T16:00:00.000Z",
                     "metrics": [{"temperature": 27.1}, {"dewPoint": 16.9}]},
                    {"timestamp": "2015-09-01T16:10:00.000Z",
                     "metrics": [{"temperature": 27.3}]},
                    {"timestamp": "2015-09-01T16:20:00.000Z",
                     "metrics": [{"temperature": 27.5}, {"dewPoint": 17.1}]},
                    {"timestamp": "2015-09-01T16:30:00.000Z",
                     "metrics": [{"temperature": 27.4}, {"dewPoint": 17.3}]},
                    {"timestamp": "2015-09-01T16:40:00.000Z",
                     "metrics": [{"temperature": 27.2}]},
                    {"timestamp": "2015-09-01T17:00:00.000Z",
                     "metrics": [{"temperature": 28.1}, {"dewPoint": 18.3}]},
                    ]

        for data in listData:
            request = self.factory.post('/measurements', json.dumps(data), content_type='application/json')
            response = self.view(request)

    def test_get_stats_for_well_reported_metric(self):
        """        
        | param | value |
        | stat | min |
        | stat | max |
        | stat | average |
        | metric | temperature |
        | fromDateTime | 2015-09-01T16: 00:00.000Z |
        | toDateTime | 2015-09-01T17: 00:00.000Z |

        """
        request = self.factory.get('/stats/min,max,average/temperature/2015-09-01T16:00:00.000Z/2015-09-01T17:00:00.000Z')
        data = {'stat':'min,max,average', 'metric':'temperature', 'fromDateTime':'2015-09-01T16:00:00.000Z', 'toDateTime':'2015-09-01T17:00:00.000Z'}
        response = self.view(request, data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_stats_for_sparsely_reported_metric(self):
        """
        Scenario: Get stats for a sparsely reported metric
        GET /stats?<params...> When I get
        stats with parameters:
            | param | value |
            | stat | min |
            | stat | max |
            | stat | average |
            | metric | dewPoint |
            | fromDateTime | 2015- 09 - 01 T16: 00:00.000 Z |
            | toDateTime | 2015 - 09 - 01 T17: 00:00.000Z |

      #             | "dewPoint" | "min"     | 16.9  |
      # | "dewPoint" | "max"     | 17.3  |
      # | "dewPoint" | "average" | 17.1  |

         """
        request = self.factory.get('/stats/min,max,average/dewPoint/2015-09-01T16:00:00.000Z/2015-09-01T17:00:00.000Z')
        data = {'stat': 'min,max,average', 'metric': 'dewPoint', 'fromDateTime': '2015-09-01T16:00:00.000Z',
                'toDateTime': '2015-09-01T17:00:00.000Z'}
        response = self.view(request, data=data)
        print(response.data)
        self.assertEqual(response.status_code, 200)


    def test_get_stats_for_a_metric_that_has_never_been_reported(self):
        '''
        Scenario: Get stats for a metric that has never been reported
        # GET /stats?<params...> When I get stats
        with parameters:
            | param | value |
            | stat | min |
            | stat | max |
            | stat | average |
            | metric | precipitation |
            | fromDateTime |2015-09 - 01 T16: 00:00.000 Z|
            | toDateTime | 2015-09-01T17:00:00.000Z |
        '''
        request = self.factory.get('/stats/min,max,average/precipitation/2015-09-01T16:00:00.000Z/2015-09-01T17:00:00.000Z')
        data = {'stat': 'min,max,average', 'metric': 'dewPoint', 'fromDateTime': '2015-09-01T16:00:00.000Z','toDateTime': '2015-09-01T17:00:00.000Z'}
        response = self.view(request, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_stats_for_more_than_one_metric(self):
        """
        Get stats for more than one metric # GET /stats?<params...>
        When I get stats
        with parameters:
            | param | value |
            | stat | min |
            | stat | max |
            | stat | average |
            | metric | temperature |
            | metric | dewPoint |
            | metric | precipitation |
            | fromDateTime | 2015-09-01 T16: 00:00.000Z |
            | toDateTime | 2015-09-01  T17: 00:00.000Z |
        """
        request = self.factory.get('/stats/min,max,average/temperature,dewPoint,precipitation/2015-09-01T16:00:00.000Z/2015-09-01T17:00:00.000Z')
        data = {'stat':'min,max,average', 'metric': 'temperature,dewPoint,precipitation', 'fromDateTime': '2015-09-01T16:00:00.000Z','toDateTime':'2015-09-01T17:00:00.000Z'}

        response = self.view(request, data=data)
        self.assertEqual(response.status_code, 200)
