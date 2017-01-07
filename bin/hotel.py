#!/usr/bin/python3

from reservation import Reservation
import sys
import csv

class Hotel:
  reservations = {}

  def add_reservation(self):
    customer_name = input('Enter customer name: ')
    check_in_date = input('Enter check-in-date: ')
    check_out_date = input('Enter check-out-date: ')
    status = input('Has customer paid? (Y/N): ')
    room_size = input('Enter room size: ')
    number_of_people = input('Enter number of people in a room: ')
    price = input('Enter price allocated to each customer: ')
    
    params = {
      'customer_name': customer_name,
      'check_in_date': check_in_date,
      'check_out_date': check_out_date,
      'status': status,
      'room_size': room_size,
      'number_of_people': number_of_people,
      'price': price
    }

    reservation_object = Reservation(params)
    reservations[reservation_object.reference_number] = reservation_object

  def update_value(input_prompt, old_value):
    input_value = input(input_prompt)
    if input_value.strip() == '':
      return old_value
    else:
      return input_value      

  def update_reservation(self):
    reference_number = input('Enter reference number: ')
    if reservations[reference_number]:
      reservations[reference_number].customer_name = update_value('Update customer name: ', reservations[reference_number].customer_name)
      reservations[reference_number].check_in_date = update_value('Update check-in-date: ', reservations[reference_number].check_in_date)
      reservations[reference_number].check_out_date = update_value('Update check-out-date: ', reservations[reference_number].check_out_date)
      reservations[reference_number].status = update_value('Has customer paid? (Y/N): ', reservations[reference_number].status)
      reservations[reference_number].room_size = update_value('Update room size: ', reservations[reference_number].room_size)
      reservations[reference_number].number_of_people = update_value('Update number of people in a room: ', reservations[reference_number].number_of_people)
      reservations[reference_number].price = update_value('Update price allocated to each customer: ', reservations[reference_number].price)
      print ('Reservation successfully updated.')
    else:
      print ('Reservation not found')

  def delete_reservation(self):
    reference_number = input('Enter reference number: ')
    if reservations[reference_number]:
      del reservations[reference_number]
      print ('Reservation successfully deleted.')
    else:
      print ('Reservation not found')

  def view_all_reservations_in_system():
    for reservation in reservations:
      print (reservations[reservation].reference_number, reservations[reservation].customer_name)

  def save_reservations(self):
    with open('../csv/reservations.csv', 'a+') as csv_file:
      writer = csv.DictWriter(csv_file, fieldnames = Reservation.get_field_names())
      write.writeheader()
      for reservation in reservations:
        writer.writerow({ 'Reference Number': reservation, 'Customer Name': reservations[reservation].customer_name, 'Check-in-date': reservations[reservation].check_in_date, 'Check-out-date': reservations[reservation].check_out_date, 'Status': reservations[reservation].status, 'Room Size': reservations[reservation].room_size, 'Number of people': reservations[reservation].number_of_people, 'price': reservations[reservation].price })

  def load_reservations_from_file(self):
    with open('../csv/reservations.csv') as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        print (row['Reference Number'], row['Customer Name'])

  def view_reservations_for_paid(self):
    count = 0
    for reservation in reservations:
      if reservations[reservation].status == 'Paid':
        print (reservations[reservation].reference_number, reservations[reservation].customer_name)

  def go_back_to_menu(self):
    self.welcome()

  def welcome(self):
    print ('Welcome to A.A. Hotel Inn.\nHotel Reservation System\n\n')
    print ('Please select an option from the menu below:')
    choice = input ("1: Add a reservation\n2: Modify existing reservation\n3: Delete reservation\n4: View all reservation records in the system\n5: Save current records to a file\n6: Load all records from a saved file\n7: View all records of all the amounts made\n8: Go back to menu\n9: Exit application\n")
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
      sys.exit()
