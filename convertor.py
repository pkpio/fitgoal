#!/usr/bin/env python3
"""
__author__ = "Praveen Kumar Pendyala"
__email__ = "mail@pkp.io"
"""
import datetime
import time
import dateutil.parser
from datetime import timedelta, date
import parsedatetime as pdt

class Convertor:
	"""Methods for data type conversions."""

	# Unit conversion constants
	KMS_PER_MILE = 1.60934

	def __init__(self, start_date):
		self.start_date = start_date

	def parseHumanReadableDate(self,datestr):
		"""Parses a human-readable date string to python's date object"""
		cal = pdt.Calendar()
		now = datetime.datetime.now()
		return cal.parseDT(str(datestr), now)[0].date()

	def daysSinceStart(self,given_date):
		gdate = self.parseHumanReadableDate(given_date)
		sdate = self.parseHumanReadableDate(self.start_date)
		return (gdate-sdate).days

	def daterange(self, start_date=None, end_date=None, step=1):
		""" returns a generator that iterates from start_date to end_date. 
		Start and end dates included.

		step -- number of days to skip between each generated day time stamp.
		"""
		if not start_date:
			start_date = self.parseHumanReadableDate(self.start_date)
		if not end_date:
			end_date = self.parseHumanReadableDate('today')
		for n in range(0, int((end_date - start_date).days + 1), step):
			yield start_date + timedelta(n)

	def distance_in_kms(self, val, unit):
		if unit == 'Mile':
			return val * self.KMS_PER_MILE
		elif unit == 'Kilometer':
			return val

