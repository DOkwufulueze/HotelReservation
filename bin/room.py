#!/usr/bin/python3

class Room:

  def __init__(self, params = {}):
    # room parameters
    self.params = {
      'Room Reference Number': params['Room Reference Number'],
      'Room Type': params['Room Type'],
      'Price': params['Price'],
      'Available': params['Available']
    }

  # The CSV Header columns and keys for room
  def get_field_names(self):
    return ['Room Reference Number', 'Room Type', 'Price', 'Available']
