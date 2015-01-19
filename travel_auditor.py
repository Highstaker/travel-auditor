#!/usr/bin/python3 -i
#-*- coding: UTF-8 -*-

import sys

audit_file = ""

###############################
######Global variables to store all entries
############################

#All participants on this trip
participants = []

#Names of individual entries
entry_names = []

#Dates of individual entries
entry_dates = []

#List of tuples showing the participants for certain entries, or -1 if everybody participated
participants_in_entry = []

#List of tuples showing how much every participant paid for this entry
payments_in_entry = []

#List of individual services
individual_services = []

def write_to_file(filename):

	#Leading symbols legend:
	#0 - participant's name
	#1 - name of the entry
	#2 - date of the entry
	#3 - List of participants in entry
	#4 - List of payments per participant in entry
	#5 - An individual service in this entry

	def write_line(index,data):
		s = str(index) + data + "\n"
		return s

	global audit_file
	audit_file = open(filename+".audit","w")

	#write the participants to file
	for i in participants:
		audit_file.write(write_line(0,i))

	for i in range(len(entry_names)):
		audit_file.write(write_line(1,entry_names[i]))
		audit_file.write(write_line(2,entry_dates[i]))
		audit_file.write(write_line(3,str(participants_in_entry[i]).replace("[","").replace("]","")))
		audit_file.write(write_line(4,str(payments_in_entry[i]).replace("[","").replace("]","")))

		for j in individual_services[i]:
			audit_file.write(write_line(5,str(j).replace("[","").replace("]","")))



	audit_file.close()

def main_menu():

	while True:
		print("""
			Main Menu:

			1.New file
			2.Open file

			0.Exit program
		"""
			)
		ans=input("What would you like to do? ")

		if ans=="1":
			#Create new file
			create_new_file()
			# break

		elif ans=="2":
			#Open file dialog
			pass

		elif ans=="0":
			break

		else:
			print("\n Unknown option, try again!")

def create_new_file():
	filename=input("Please enter a name of a file to create: ")	

	amount_of_participants = input("Please enter the amount of participants: ")
	amount_of_participants = int(amount_of_participants)

	global participants

	for i in range(amount_of_participants):
		participants += [ input("Enter the name of participant " + str(i) + ": ")]

	write_to_file(filename)
	edit_file(filename)


def edit_file(filename):
	pass
	while True:
		print("""
			1.Add new entry
			2.Edit entry
			3.Calculate entry results
			4.Calculate overall results

			0.Back to Main Menu
		"""
			)
		ans=input("What would you like to do? ")

		if ans=="1":
			#Add new entry, like one trip to a shop etc.
			add_new_entry()
			write_to_file(filename)

		elif ans=="2":
			#Edit
			write_to_file(filename)
			pass

		elif ans=="0":
			break

		else:
			print("\n Unknown option, try again!")

def add_new_entry():
	pass

	#Name this entry
	entry_name=input("Please enter the name of this entry: ")

	#Date of the entry
	entry_date=input("Please enter the date of this entry (preferrable format: YYYYMMDD): ")

	#Define who participated in this entry
	list_of_participants = ""

	for i in range(len(participants)):
		list_of_participants += participants[i] + "\n"

	s=input("Who participated in this entry? Write indicies of participants separated by comma or leave it blank if everybody participated:\n")

	if s:
		participants_in_entry_cur = [int(i) for i in s.split(',')]
	else:
		participants_in_entry_cur = [i for i in range(len(participants))]

	#manage how much each one paid
	payments_in_entry_cur = []

	for i in participants_in_entry_cur:
		payment=input("How much did " + participants[i] + " pay in this entry?: ")
		if payment:
			payments_in_entry_cur+=[float(payment)]
		else:
			payments_in_entry_cur+=[0]

	#manage individual products or services
	individual_services_cur = []
	while True:
		pass
		ans=input("Would you like to add individual products? [y/n]:" )

		if ans.lower()=="y":
			#add a new individual service
			individual_services_cur += [add_individual_service(participants_in_entry_cur)]

		elif ans.lower()=="n":
			#no more individual services, continue
			break

	#apply local variables to globals
	global entry_names
	global entry_dates
	global participants_in_entry
	global payments_in_entry
	global individual_services

	entry_names+=[entry_name]
	entry_dates+=[entry_date]
	participants_in_entry+=[participants_in_entry_cur]
	payments_in_entry+=[payments_in_entry_cur]
	individual_services+=[individual_services_cur]

def add_individual_service(participants_in_entry_cur):
	#Add an individual service and returns a tuple containing its name as the first element and the sums each participant paid for it
	ind_service_name=input("Enter individual service name: ")

	payments=[ind_service_name]
	for i in participants_in_entry_cur:
		payment=input("How much should be paid by " + participants[i] + " for this individual service (" + ind_service_name +")?: ")
		if payment:
			payments+=[float(payment)]
		else:
			payments+=[0]

	return payments



def main():
	main_menu()

if __name__ == '__main__':
	main()
