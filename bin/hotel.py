#!/usr/bin/python3

from reservation import Reservation
import sys
import csv
import re
import time

class Hotel:
  reservations = {}
  is_reservations_loaded = False

  def get_max_reference_number(self):
    max_reference_number = max(self.reservations) if len(self.reservations) > 0 else 0
    return max_reference_number

  def go_back_to_menu(self):
    self.welcome()

  def validate_date(self, stringObject):
    return re.match(r'\d{1,2}/\d{1,2}/\d{4}', stringObject)

  def welcome(self):
    if not(self.is_reservations_loaded): self.load_reservations_object()
    print ("\n================================================================================\n")
    print ('Welcome to A.A. Hotel Inn.\nHotel Reservation System\n\n')
    print ('Please select an option from the menu below:')
    choice = input ("1: Add a reservation\n2: Modify existing reservation\n3: Delete reservation\n4: View all reservation records in the system\n5: Save current records to a file\n6: Load all records from a saved file\n7: View all records of all the amounts made\n8: Go back to menu\n9: Exit application\n\n================================================================================\n")
    self.decision(choice)

  def decision(self, choice):
    if choice == '1':
      self.add_reservation()
    elif choice == '2':
      self.update_reservation()
    elif choice == '3':
      self.delete_reservation()
    elif choice == '4':
      self.view_all_reservations_in_system()
    elif choice == '5':
      self.save_reservations()
    elif choice == '6':
      self.load_reservations_from_file()
    elif choice == '7':
      self.view_reservations_for_paid()
    elif choice == '8':
      self.go_back_to_menu()
    elif choice == '9':
      print ('Good bye...\n================================================================================\n')
      sys.exit()
    else:
      self.go_back_to_menu()

  def continue_or_stop(self):
    choice = input ('\n\nEnter 8 to continue, 9 to exit application:\n')
    if choice == '8':
      self.go_back_to_menu()
    elif choice == '9':
      print ('Good bye...\n================================================================================\n')
      sys.exit()
    else:
      self.go_back_to_menu()

  def add_reservation(self):
    customer_name = input('Enter customer name: ')
    check_in_date = input('Enter check-in-date (d/m/yyyy or dd/mm/yyyy): ')
    check_out_date = input('Enter check-out-date (d/m/yyyy or dd/mm/yyyy): ')
    status = input('Has customer paid? (y/n): ')
    room_size = input('Enter room size: ')
    number_of_people = input('Enter number of people in a room: ')
    price = input('Enter price allocated to each customer: ')
    if self.validate_date(check_in_date) and self.validate_date(check_out_date):
      check_in = time.strptime(check_in_date, "%d/%m/%Y")
      check_out = time.strptime(check_out_date, "%d/%m/%Y")
      params = {
        'Reference Number': self.get_max_reference_number() + 1,
        'Customer Name': customer_name,
        'Check-in-date': str(check_in.tm_mday) + "/" + str(check_in.tm_mon) + "/" + str(check_in.tm_year),
        'Check-out-date': str(check_out.tm_mday) + "/" + str(check_out.tm_mon) + "/" + str(check_out.tm_year),
        'Status': status,
        'Room Size': room_size,
        'Number of people': number_of_people,
        'Price': price
      }

      reservation_object = Reservation(params)
      self.reservations[reservation_object.params['Reference Number']] = reservation_object.params
      print ('\n================================================================================\nReservation with Reference Number %d added succesfully\n================================================================================\n' % reservation_object.params['Reference Number'])
    else:
      print ('\n================================================================================\nWrong Date Format')
    self.continue_or_stop()

  def update_value(self, input_prompt, old_value):
    input_value = input(input_prompt)
    if input_value.strip() == '':
      return old_value
    else:
      return input_value      

  def update_reservation(self):
    reference_number = int(input('Enter reference number: '))
    try:
      if self.reservations[reference_number]:
        self.reservations[reference_number]['Customer Name'] = self.update_value('Update customer name: ', self.reservations[reference_number]['Customer Name'])
        self.reservations[reference_number]['Check-in-date'] = self.update_value('Update check-in-date: ', self.reservations[reference_number]['Check-in-date'])
        self.reservations[reference_number]['Check-out-date'] = self.update_value('Update check-out-date: ', self.reservations[reference_number]['Check-out-date'])
        self.reservations[reference_number]['Status'] = self.update_value('Has customer paid? (Y/N): ', self.reservations[reference_number]['Status'])
        self.reservations[reference_number]['Room Size'] = self.update_value('Update room size: ', self.reservations[reference_number]['Room Size'])
        self.reservations[reference_number]['Number of people'] = self.update_value('Update number of people in a room: ', self.reservations[reference_number]['Number of people'])
        self.reservations[reference_number]['Price'] = self.update_value('Update price allocated to each customer: ', self.reservations[reference_number]['Price'])
        print ('Reservation successfully updated.\n================================================================================\n')
      else:
        print ('Reservation not found\n================================================================================\n')
    except KeyError:
      print ('No Reservation with input Reference Number\n================================================================================\n')

    self.continue_or_stop()

  def delete_reservation(self):
    reference_number = int(input('Enter reference number: '))
    try:
      if self.reservations[reference_number]:
        del self.reservations[reference_number]
        print ('Reservation successfully deleted.\n================================================================================\n')
      else:
        print ('Reservation not found\n================================================================================\n')
    except KeyError:
      print ('No Reservation with input Reference Number\n================================================================================\n')

    self.continue_or_stop()

  def view_all_reservations_in_system(self):
    if len(self.reservations) > 0:
      for reservation in self.reservations:
        print ("Reference Number:\t%s\nCustomer Name:\t%s\nCheck-in-date:\t%s\nCheck-out-date:\t%s\nStatus:\t%s\nRoom Size:\t%s\nNumber of people:\t%s\nPrice:\t%s\n" % (str(self.reservations[reservation]['Reference Number']), self.reservations[reservation]['Customer Name'], self.reservations[reservation]['Check-in-date'], self.reservations[reservation]['Check-out-date'], self.reservations[reservation]['Status'], self.reservations[reservation]['Room Size'], self.reservations[reservation]['Number of people'], self.reservations[reservation]['Price']))

      print ('\n================================================================================\n');
    else:
      print ("No reservation in system at the moment.\n================================================================================\n")

    self.continue_or_stop()

  def save_reservations(self):
    if len(self.reservations) > 0:
      with open('../csv/reservations.csv', 'w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = Reservation.get_field_names(self))
        writer.writeheader()
        for reservation in self.reservations:
          writer.writerow({ 'Reference Number': reservation, 'Customer Name': self.reservations[reservation]['Customer Name'], 'Check-in-date': self.reservations[reservation]['Check-in-date'], 'Check-out-date': self.reservations[reservation]['Check-out-date'], 'Status': self.reservations[reservation]['Status'], 'Room Size': self.reservations[reservation]['Room Size'], 'Number of people': self.reservations[reservation]['Number of people'], 'Price': self.reservations[reservation]['Price'] })
      print ('Reservation records saved successfully\n================================================================================\n')
    else:
      print ('No Reservation to save at the moment\n================================================================================\n')

    self.continue_or_stop()

  def load_reservations_object(self):
    with open('../csv/reservations.csv', 'a+') as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        self.reservations[int(row['Reference Number'])] = row

    self.is_reservations_loaded = True

  def load_reservations_from_file(self):
    count = 0
    with open('../csv/reservations.csv') as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        print ("Reference Number:\t%s\nCustomer Name:\t%s\nCheck-in-date:\t%s\nCheck-out-date:\t%s\nStatus:\t%s\nRoom Size:\t%s\nNumber of people:\t%s\nPrice:\t%s\n" % (row['Reference Number'], row['Customer Name'], row['Check-in-date'], row['Check-out-date'], row['Status'], row['Room Size'], row['Number of people'], row['Price']))
        count += 1

    if count == 0:
      print ('No Reservation in CSV file.\n================================================================================\n')
    else:
      print ('\n================================================================================\n');

    self.continue_or_stop()

  def view_reservations_for_paid(self):
    count = 0
    if len(self.reservations) > 0:
      for reservation in self.reservations:
        if self.reservations[reservation]['Status'].lower() == 'y':
          print ("Reference Number:\t%s\nCustomer Name:\t%s\nCheck-in-date:\t%s\nCheck-out-date:\t%s\nStatus:\t%s\nRoom Size:\t%s\nNumber of people:\t%s\nPrice:\t%s\n" % (str(self.reservations[reservation]['Reference Number']), self.reservations[reservation]['Customer Name'], self.reservations[reservation]['Check-in-date'], self.reservations[reservation]['Check-out-date'], self.reservations[reservation]['Status'], self.reservations[reservation]['Room Size'], self.reservations[reservation]['Number of people'], self.reservations[reservation]['Price']))
          count += 1
        
      if count == 0:
        print ('No Reservation for Paid.\n================================================================================\n')
      else:
        print ('\n================================================================================\n');
    else:
      print ('No Reservation found.\n================================================================================\n')

    self.continue_or_stop()
