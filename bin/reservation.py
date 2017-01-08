#!/usr/bin/python3

class Reservation:

  def __init__(self, params = {}):
    self.params = {
      'Reference Number': params['Reference Number'],
      'Customer Name': params['Customer Name'],
      'Check-in-date': params['Check-in-date'],
      'Check-out-date': params['Check-out-date'],
      'Status': params['Status'],
      'Room Size': params['Room Size'],
      'Number of people': params['Number of people'],
      'Price': params['Price']
    }    

  def get_field_names(self):
    return ['Reference Number', 'Customer Name', 'Check-in-date', 'Check-out-date', 'Status', 'Room Size', 'Number of people', 'Price']
