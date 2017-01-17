#!/usr/bin/python3

from reservation import Reservation
from room import Room
import sys
import csv
import re
import time
import os.path

class Hotel:
  dictionary = {
    'reservations': {},
    'rooms': {}
  }
  are_hash_objects_loaded = {
    'reservations': False,
    'rooms': False
  }

  def get_max_reference_number(self, for_name):
    max_reference_number = max(self.dictionary[for_name]) if len(self.dictionary[for_name]) > 0 else 0
    return max_reference_number

  def go_back_to_menu(self):
    self.welcome()

  def validate_date(self, stringObject):
    return re.match(r'\d{1,2}/\d{1,2}/\d{4}', stringObject)

  def welcome(self):
    if not(self.are_hash_objects_loaded['reservations']): self.load_hash_object('reservations', 'Reference Number')
    if not(self.are_hash_objects_loaded['rooms']): self.load_hash_object('rooms', 'Room Reference Number')
    print ("\n================================================================================\n")
    print ('Welcome to A.A. Hotel Inn.\nHotel Reservation System\n\n')
    print ('Please select an option from the menu below:')
    choice = input ("1: Add a reservation\n2: Modify existing reservation\n3: Delete reservation\n4: View all reservation records in the system\n5: Save current records (Reservations and Rooms) to files\n6: Load all reservation records from a saved file\n7: View all reservation records of all the amounts made\n================================================================================\na: Add Room\nb: Modify Existing Room\nc: View all room records in the system\nd: Delete Room\ne: Load all rooms from a saved file\nf: View Available Rooms\n8: Go back to menu\n9: Exit application\n================================================================================\n\n")
    self.decision(choice)

  def continue_or_stop(self):
    choice = input ('\n\nEnter 8 to continue, 9 to exit application:\n')
    if choice == '8':
      self.go_back_to_menu()
    elif choice == '9':
      print ('Good bye...\n================================================================================\n')
      sys.exit()
    else:
      self.go_back_to_menu()

  def update_value(self, input_prompt, old_value):
    input_value = input(input_prompt)
    if input_value.strip() == '':
      return old_value
    else:
      return input_value      

  def update_record(self, for_name):
    reference_number = input('Enter reference number: ')
    if reference_number:
      reference_number = int(reference_number)
      try:
        if for_name == 'reservations' and self.dictionary[for_name][reference_number]:
          self.update_reservation(reference_number)
        elif for_name == 'rooms' and self.dictionary[for_name][reference_number]:
          self.update_room(reference_number)
        else:
          print (for_name[0:(len(for_name) - 1)].capitalize() + ' not found\n================================================================================\n')
      except KeyError:
        print ('No ' + for_name[0:(len(for_name) - 1)].capitalize() + ' with input Reference Number\n================================================================================\n')

    self.continue_or_stop()

  def update_room(self, reference_number):
    self.dictionary['rooms'][reference_number]['Room Type'] = self.update_value('Update Room Type: ', self.dictionary['rooms'][reference_number]['Room Type'])
    self.dictionary['rooms'][reference_number]['Price'] = self.update_value('Update Price: ', self.dictionary['rooms'][reference_number]['Price'])
    self.dictionary['rooms'][reference_number]['Available'] = self.update_value('Update Availability: ', self.dictionary['rooms'][reference_number]['Available'])
    print ('Room successfully updated.\n================================================================================\n')

  def delete_record(self, for_name):
    reference_number = input('Enter reference number: ')
    if reference_number:
      reference_number = int(reference_number)
      try:
        if self.dictionary[for_name][reference_number]:
          del self.dictionary[for_name][reference_number]
          print (for_name[0:(len(for_name) - 1)].capitalize() + ' successfully deleted.\n================================================================================\n')
        else:
          print (for_name[0:(len(for_name) - 1)].capitalize() + ' not found\n================================================================================\n')
      except KeyError:
        print ('No ' + for_name[0:(len(for_name) - 1)].capitalize() + ' with input Reference Number\n================================================================================\n')

    self.continue_or_stop()

  def view_all_records_in_system(self, for_name):
    if len(self.dictionary[for_name]) > 0:
      for record in self.dictionary[for_name]:
        print (self.record(for_name, self.dictionary[for_name][record]))

      print ('\n================================================================================\n');
    else:
      print ("No " + for_name[0:len(for_name) - 1].capitalize() + " in system at the moment.\n================================================================================\n")

    self.continue_or_stop()

  def save_records(self):
    for key_name in self.dictionary:
      if len(self.dictionary[key_name]) > 0:
        with open('../csv/' + key_name + '.csv', 'w+') as csv_file:
          writer = csv.DictWriter(csv_file, fieldnames = Reservation.get_field_names(self)) if key_name == 'reservations' else csv.DictWriter(csv_file, fieldnames = Room.get_field_names(self))
          writer.writeheader()
          for record in self.dictionary[key_name]:
            writer.writerow(self.rowDictionary(key_name, record))
        print (key_name[0:len(key_name) - 1].capitalize() + ' records saved successfully\n================================================================================\n')
      else:
        print ('No ' + key_name[0:len(key_name) - 1].capitalize() + ' to save at the moment\n================================================================================\n')

    self.continue_or_stop()

  def rowDictionary(self, for_name, record):
    if for_name == 'reservations':
      return { 'Reference Number': record, 'Customer Name': self.dictionary['reservations'][record]['Customer Name'], 'Check-in-date': self.dictionary['reservations'][record]['Check-in-date'], 'Check-out-date': self.dictionary['reservations'][record]['Check-out-date'], 'Status': self.dictionary['reservations'][record]['Status'], 'Room Reference Number': self.dictionary['reservations'][record]['Room Reference Number'], 'Room Type': self.dictionary['reservations'][record]['Room Type'], 'Number of people': self.dictionary['reservations'][record]['Number of people'], 'Price': self.dictionary['reservations'][record]['Price'] } 
    else:
      return { 'Room Reference Number': record, 'Room Type': self.dictionary['rooms'][record]['Room Type'], 'Price': self.dictionary['rooms'][record]['Price'], 'Available': self.dictionary['rooms'][record]['Available'] }

  def load_hash_object(self, csv_file_name, reference_title):
    if os.path.isfile('../csv/'+ csv_file_name + '.csv'):
      with open('../csv/'+ csv_file_name +'.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
          self.dictionary[csv_file_name][int(row[reference_title])] = row
    else:
      open('../csv/'+ csv_file_name +'.csv', 'a+')

    self.are_hash_objects_loaded[csv_file_name] = True

  def load_records_from_file(self, csv_file_name):
    count = 0
    with open('../csv/' + csv_file_name + '.csv') as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        print (self.record(csv_file_name, row))
        count += 1

    if count == 0:
      print ('No ' + csv_file_name[0:len(csv_file_name) - 1].capitalize() + ' in CSV file.\n================================================================================\n')
    else:
      print ('\n================================================================================\n');

    self.continue_or_stop()

  def record(self, for_name, row):
    record = "Reference Number:\t%s\nCustomer Name:\t%s\nCheck-in-date:\t%s\nCheck-out-date:\t%s\nStatus:\t%s\nRoom Reference Number:\t%s\nRoom Type:\t%s\nNumber of people:\t%s\nPrice:\t%s\n" % (row['Reference Number'], row['Customer Name'], row['Check-in-date'], row['Check-out-date'], row['Status'], row['Room Reference Number'], row['Room Type'], row['Number of people'], row['Price']) if for_name == 'reservations' else "Room Reference Number:\t%s\nRoom Type:\t%s\nPrice:\t%s\nAvailable:\t%s\n" % (row['Room Reference Number'], row['Room Type'], row['Price'], row['Available'])
    return record

  def view_records_for_paid(self, for_name):
    count = 0
    if len(self.dictionary[for_name]) > 0:
      for record in self.dictionary[for_name]:
        if self.dictionary[for_name][record]['Status'].lower() == 'y':
          print (self.record(for_name, self.dictionary[for_name][record]));
          count += 1
        
      if count == 0:
        print ('No ' + for_name[0:len(for_name) - 1].capitalize() + ' for Paid.\n================================================================================\n')
      else:
        print ('\n================================================================================\n');
    else:
      print ('No ' + for_name[0:len(for_name) - 1].capitalize() + ' found.\n================================================================================\n')

    self.continue_or_stop()

  def view_available_rooms(self):
    count = 0
    if len(self.dictionary['rooms']) > 0:
      for record in self.dictionary['rooms']:
        if self.dictionary['rooms'][record]['Available'].lower() == '1':
          print (self.record('rooms', self.dictionary['rooms'][record]));
          count += 1
        
      if count == 0:
        print ('No Available' + 'rooms'[0:len('rooms') - 1].capitalize() + ' for now.\n================================================================================\n')
      else:
        print ('\n================================================================================\n');
    else:
      print ('No ' + 'rooms'[0:len('rooms') - 1].capitalize() + ' found.\n================================================================================\n')

    self.continue_or_stop()

  def decision(self, choice):
    if choice == '1':
      self.add_reservation()
    elif choice == '2':
      self.update_record('reservations')
    elif choice == '3':
      self.delete_record('reservations')
    elif choice == '4':
      self.view_all_records_in_system('reservations')
    elif choice == '5':
      self.save_records()
    elif choice == '6':
      self.load_records_from_file('reservations')
    elif choice == '7':
      self.view_records_for_paid('reservations')
    elif choice == '8':
      self.go_back_to_menu()
    elif choice == '9':
      print ('Good bye...\n================================================================================\n')
      sys.exit()
    elif choice == 'a':
      self.add_room()
    elif choice == 'b':
      self.update_record('rooms')
    elif choice == 'c':
      self.view_all_records_in_system('rooms')
    elif choice == 'd':
      self.delete_record('rooms')
    elif choice == 'e':
      self.load_records_from_file('rooms')
    elif choice == 'f':
      self.view_available_rooms()
    else:
      self.go_back_to_menu()

  def add_reservation(self):
    room_reference_number = input('Enter room reference number: ')
    if room_reference_number:
      if int(room_reference_number) in self.dictionary['rooms']:
        if not (self.dictionary['rooms'][int(room_reference_number)]['Available'] == '1'):
          print ('\n================================================================================\nRoom ' + room_reference_number + ' (' + self.dictionary['rooms'][int(room_reference_number)]['Room Type'] + ') is not Available')
        else:
          customer_name = input('Enter customer name: ')
          check_in_date = input('Enter check-in-date (d/m/yyyy or dd/mm/yyyy): ')
          check_out_date = input('Enter check-out-date (d/m/yyyy or dd/mm/yyyy): ')
          status = input('Has customer paid? (y/n): ')
          number_of_people = input('Enter number of people in a room: ')
          price = self.dictionary['rooms'][int(room_reference_number)]['Price']
          room_type = self.dictionary['rooms'][int(room_reference_number)]['Room Type']
          if self.validate_date(check_in_date) and self.validate_date(check_out_date):
            check_in = time.strptime(check_in_date, "%d/%m/%Y")
            check_out = time.strptime(check_out_date, "%d/%m/%Y")
            params = {
              'Reference Number': self.get_max_reference_number('reservations') + 1,
              'Customer Name': customer_name,
              'Check-in-date': str(check_in.tm_mday) + "/" + str(check_in.tm_mon) + "/" + str(check_in.tm_year),
              'Check-out-date': str(check_out.tm_mday) + "/" + str(check_out.tm_mon) + "/" + str(check_out.tm_year),
              'Status': status,
              'Room Reference Number': int(room_reference_number),
              'Room Type': room_type,
              'Number of people': number_of_people,
              'Price': price
            }

            reservation_object = Reservation(params)
            self.dictionary['reservations'][reservation_object.params['Reference Number']] = reservation_object.params
            print ('\n================================================================================\nReservation with Reference Number %d added succesfully\n================================================================================\n' % reservation_object.params['Reference Number'])
          else:
            print ('\n================================================================================\nWrong Date Format')
      else:
        print ('\n================================================================================\nRoom reference number (' + room_reference_number + ') does not exist')
    self.continue_or_stop()

  def add_room(self):
    room_type = input('Enter room type (Double Room, Master Room...): ')
    price = input('Enter price: ')
    available = input('Available? (1: Available, 0: Not Available): ')
    params = {
      'Room Reference Number': self.get_max_reference_number('rooms') + 1,
      'Room Type': room_type,
      'Price': price,
      'Available': available,
    }
    room_object = Room(params)
    self.dictionary['rooms'][room_object.params['Room Reference Number']] = room_object.params
    print ('\n================================================================================\nRoom with Reference Number %d added succesfully\n================================================================================\n' % room_object.params['Room Reference Number'])
    self.continue_or_stop()

  def update_reservation(self, reference_number):
    self.dictionary['reservations'][reference_number]['Customer Name'] = self.update_value('Update customer name: ', self.dictionary['reservations'][reference_number]['Customer Name'])
    self.dictionary['reservations'][reference_number]['Check-in-date'] = self.update_value('Update check-in-date: ', self.dictionary['reservations'][reference_number]['Check-in-date'])
    self.dictionary['reservations'][reference_number]['Check-out-date'] = self.update_value('Update check-out-date: ', self.dictionary['reservations'][reference_number]['Check-out-date'])
    self.dictionary['reservations'][reference_number]['Status'] = self.update_value('Has customer paid? (Y/N): ', self.dictionary['reservations'][reference_number]['Status'])
    self.dictionary['reservations'][reference_number]['Number of people'] = self.update_value('Update number of people in a room: ', self.dictionary['reservations'][reference_number]['Number of people'])
    print ('Reservation successfully updated.\n================================================================================\n')
