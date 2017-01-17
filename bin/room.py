#!/usr/bin/python3

class Room:

  def __init__(self, params = {}):
    self.params = {
      'Room Reference Number': params['Room Reference Number'],
      'Room Type': params['Room Type'],
      'Price': params['Price'],
      'Available': params['Available']
    }

  def get_field_names(self):
    return ['Room Reference Number', 'Room Type', 'Price', 'Available']
