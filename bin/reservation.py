#!/usr/bin/python3

import csv

class Reservation:
  last_reference_number = 0

  def __init__(self, params = {}):
    self.reference_number = self.get_last_reference_number() + 1;
    self.customer_name = params.customer_name
    self.check_in_date = params.check_in_date
    self.check_out_date = params.check_out_date
    self.status = params.status
    self.room_size = params.room_size
    self.number_of_people = params.number_of_people
    self.price = params.price

  def get_last_reference_number(self):
    last_record = self.get_last_record();
    if last_record:
      return last_record
    else:
      self.last_reference_number += 1
      return (self.last_reference_number - 1)
    
  def get_last_record(self):
    with open('../csv/reservations.csv', 'a+') as csv_file:
      reader = csv.DictReader(csv_file)
      reservation = False
      for row in reader:
        reservation = row

      return reservation
    

  def get_field_names(self):
    return ['Reference Number', 'Customer Name', 'Check-in-date', 'Check-out-date', 'Status', 'Room Size', 'Number of people', 'price']
