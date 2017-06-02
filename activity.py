import fitbit
import time
from datetime import timedelta, date, datetime
import json
from convertor import Convertor

class FitbitActivity(object):
	"""Fitbit Activity class"""

	def __init__(self, client_id, client_secret, access_token, refresh_token, types=['Run']):
		self.fitbit_client = fitbit.Fitbit(client_id, client_secret, access_token=access_token, 
			refresh_token=refresh_token)
		self.activity_types = types

	def get_activity_distances(self, dist_data, start_date=None, callurl=None):
		"""
		Get distances from activities data starting from a given day from Fitbit

		dist_data -- known distance so far (all zeros initially)
		start_date -- timestamp in yyyy-mm-dd format of the start day
		callurl -- url to fetch activities from (optional)
		"""
		# Fitbit activities list endpoint is in beta stage. It may break in the future and not directly supported
		# by the python client library.
		if not callurl:
			callurl = '{}/user/-/activities/list.json?afterDate={}&sort=asc&offset=0&limit=20' \
							.format('https://api.fitbit.com/1', start_date)
		activities_raw = self.fitbit_client.make_request(callurl)
		activities = activities_raw['activities']

		for activity in activities:
			# Only interested in activities of certain types
			if activity['activityName'] not in self.activity_types: 
				continue

			# get distance for a particular day since start
			days_since = self.convertor.daysSinceStart(activity['startTime'][:10])
			day_km_dist = self.convertor.distance_in_kms(activity['distance'], 
				activity['distanceUnit'])
			dist_data[days_since] += day_km_dist

		if activities_raw['pagination']['next'] != '':
		 	return self.get_activity_distances(dist_data, 
		 		callurl=activities_raw['pagination']['next'])
		return dist_data

	def get_distances(self, start_date='2017-01-01'):
		"""
		Get distances since the given start date.
		"""
		self.convertor = Convertor(start_date)
		# Init expected steps per day and actual steps to 0 (updated later)
		dist_data = []
		for single_date in self.convertor.daterange():
			dist_data.insert(self.convertor.daysSinceStart(single_date), 0)

		# Get distance data in kms for each day since start date
		dist_data = self.get_activity_distances(dist_data, start_date=start_date)

		# find cummulative distances now
		cumm_dist_data = dist_data
		cumm_val = 0
		for i,dist in enumerate(cumm_dist_data):
			cumm_val += dist
			cumm_dist_data[i] = cumm_val
		return cumm_dist_data

	def access_token(self):
		"""
		Fitbit library takes care of updating access_token based on expiry. This returns the new
		access_token value.
		"""
		return self.fitbit_client.client.session.token['access_token']

	def refresh_token(self):
		"""
		Fitbit library takes care of updating access_token based on expiry. This returns the new
		access_token value.
		"""
		return self.fitbit_client.client.session.token['refresh_token']

