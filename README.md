# WeatherTracker
REST API to read weather data and return weather weather metrics. The objective is to implement the service interfaces provided that support the HTTP bindings.

Sarah is interested in tracking weather conditions in her garden. To accomplish this, she has set up some weather instruments connected to a Raspberry Pi that makes HTTP calls from time to time with various metrics.

Assumptions
Because the server and the Raspberry Pi are on Sarah's home network, assume that the callers are authorized implicitly; you don't need to worry about users, passwords, or authentication of any kind.

When your server starts, it must have a clean state with no measurements in it. All data it records must reside solely in your server's process memory and will be lost when it is terminated.

HTTP bindings and models have been implemented for you. No additional changes to them are necessary, though you are free to make them.

Metrics
As time goes on, Sarah will buy new instruments to plug into her Raspberry Pi. Furthermore, some of the instruments she has already installed sometimes malfunction and stop reporting metrics! To handle this, Sarah has programmed her Raspberry Pi to be very fault-tolerant and send a measurement whether or not a given instrument has reported a metric. Her code will always report the time accurately and at proper intervals, but the other metrics may not always be reported.

The instruments plugged into the Raspberry Pi will always report their metrics as floating-point numbers. This includes instruments that have not been plugged in yet.

On day one, Sarah has installed instruments that report the following metrics. Keep in mind that she may install new ones in the future.

Metric Name	    Type	     Example	Notes
timestamp	    DateTime	"2015-09-01T16:00:00.000Z"	Always sent as an ISO-8061 string in UTC
temperature	    float	     22.4	in ° C
dewPoint	    float	     18.6	in ° C
precipitation	float	     142.2	in mm
...etc	float	1234.56	     Interpretation depends on instrument
REST API
The following is an overview of the REST endpoints your solution must expose.

Method	Path	Request Body	Response Body
POST	/measurements	Measurement	(none)
GET	/measurements/:timestamp	(none)	Measurement
GET	/stats 1	(none)	Statistic[]

1 The /stats endpoint accepts query parameters for its request. These parameters are:

Parameter	Indicates	Notes
stat	which statistic to compute	can be repeated for more than one statistic
metric	which metric to compute the statistics for	can be repeated for more than one metric
fromDateTime	the inclusive minimum date and time of the range	in UTC, ISO-8061 format
toDateTime	the exclusive maximum date and time of the range	in UTC, ISO-8061 format

