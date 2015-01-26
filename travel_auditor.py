#!/usr/bin/python3 -i
#-*- coding: UTF-8 -*-

DEBUG = False

import sys
import os.path

##############
##Constants
#############

FILE_EXTENSION = ".audit"

##End constants

#file handle
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

def warning(*text):
	warningText="[WARNING] " + " ".join([str(i) for i in text])
	print(warningText)
	return warningText

def debug(*text):
	if DEBUG:
		debugText="[DEBUG] " + " ".join([str(i) for i in text])
		print(debugText)
		return debugText
	else:
		return ""

def yes_no_dialog(question):
	pass
	while True:
			ans=input(question)
			if ans.lower() == "y":
				return True
			if ans.lower() == "n":
				return False

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
	audit_file = open(filename+FILE_EXTENSION,"w")

	#write the participants to file
	for i in participants:
		audit_file.write(write_line(0,i))

	for i in range(len(entry_names)):
		audit_file.write(write_line(1,entry_names[i]))
		audit_file.write(write_line(2,entry_dates[i]))
		audit_file.write(write_line(3,",".join([str(k) for k in participants_in_entry[i]])))
		audit_file.write(write_line(4,",".join([str(k) for k in payments_in_entry[i]])))

		# print('i ' + str(i))#debug
		# if individual_services[i]:
		for j in individual_services[i]:
			if j:
				audit_file.write(write_line(5,",".join([str(k) for k in j])))

	audit_file.close()

def initialize_globals():
	global participants
	participants = []
	global entry_names
	entry_names = []
	global entry_dates
	entry_dates = []
	global participants_in_entry
	participants_in_entry = []
	global payments_in_entry
	payments_in_entry = []
	global individual_services
	individual_services = []

def read_file(filename):
	#Leading symbols legend:
	#0 - participant's name
	#1 - name of the entry
	#2 - date of the entry
	#3 - List of participants in entry
	#4 - List of payments per participant in entry
	#5 - An individual service in this entry
	audit_file=open(filename+FILE_EXTENSION,"r")

	parse=audit_file.readlines()
	parse=[i.strip("\n") for i in parse]

	debug("parse ", parse)#debug

	initialize_globals()

	global participants
	global entry_names
	global entry_dates
	global participants_in_entry
	global payments_in_entry
	global individual_services

	def apply_data(data,data_list,type1="string"):
		#Adds the string excluding the first character in string to a specified list
		if type1 == "string":
			data_list+=[data[1:]]
		elif type1 == "int":
			data_list+=[int(i) for i in data[1:]]
		elif type1 == "float":
			data_list+=[float(i) for i in data[1:]]

	def apply_list_data(data,data_list,type1="string"):
		#Adds the data excluding the first character, into a list. Elements in source are separated by SEPARATOR
		SEPARATOR=","
		if type1 == "string":
			data_list+=[data[1:].split(SEPARATOR)]
		elif type1 == "int":
			data_list+=[ [int(i) for i in data[1:].split(SEPARATOR)] ]
		elif type1 == "float":
			data_list+=[ [float(i) for i in data[1:].split(SEPARATOR)] ]

	individual_services_cur = []
	for index, line in enumerate(parse):

		debug("Parse loop", index, line)

		if line[0] == "0":
			apply_data(line,participants)

		if line[0] == "1":
			apply_data(line,entry_names)
			if parse[index-1][0] != "5" and parse[index-1][0] != "0":
				individual_services+=[[[]]]

		if line[0] == "2":
			apply_data(line,entry_dates)

		if line[0] == "3":
			apply_list_data(line,participants_in_entry,type1="int")

		if line[0] == "4":
			apply_list_data(line,payments_in_entry,type1="float")

		if line[0] == "5":
			individual_services_cur2 = []
			apply_list_data(line,individual_services_cur2)
			individual_services_cur2=individual_services_cur2[0]
			# print("individual_services_cur2[1:]  " + str(individual_services_cur2[1:]))#debug
			individual_services_cur+=[ [individual_services_cur2[0]] + [float(i) for i in individual_services_cur2[1:]] ]
			debug("5", "individual_services_cur",individual_services_cur , 'individual_services_cur2', individual_services_cur2)
			try:
				if parse[index+1][0] != "5":
					individual_services+=[individual_services_cur]
					individual_services_cur=[]
			except IndexError:
				warning("Reached end of file. No next element")
				individual_services+=[individual_services_cur]
				# individual_services_cur=[] #not needed at the end of file, it's a local variable anyway

	if len(individual_services) < len(entry_names):
		#if we reached EOF, add [[]] to fill up to required length
		individual_services+= [[[]]]*(len(entry_names)-len(individual_services))

	audit_file.close()

def main_menu():
	#Start the main menu
	while True:
		print("""
			Main Menu:

			1.New file
			2.Open file

			0.Exit program
		""")
		ans=input("What would you like to do? ")

		if ans=="1":
			#Create new file
			create_new_file()
			# break

		elif ans=="2":
			#Open file dialog
			open_file()

		elif ans=="0":
			break

		else:
			print("\n Unknown option, try again!")

def open_file():
	pass
	filename=input("Please enter a filename to open:")
	if os.path.isfile(filename+FILE_EXTENSION):
		read_file(filename)
	else:
		print("Sorry, file " +filename+FILE_EXTENSION+ " not found!")
		return False

	edit_file(filename)

def create_new_file():
	filename=input("Please enter a name of a file to create: ")

	if os.path.isfile(filename+FILE_EXTENSION):
		ans=yes_no_dialog("File with the name " + filename + FILE_EXTENSION + " already exists. \n Would you like to rewrite it? [y/n]: ")
		if ans:
			pass
		else:
			print("File with the name " + filename + FILE_EXTENSION + " already exists, and you have chosen not to overwrite it. Aborting file creation.")
			return False

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
			3.Calculate entry results and show entry
			4.Calculate overall results
			5.Add repayment entry

			0.Back to Main Menu
			"""
			)
		ans=input("What would you like to do? ")

		if ans=="1":
			#Add new entry, like one trip to a shop etc.
			add_new_entry()
			write_to_file(filename)

		elif ans=="2":
			#Edit an entry
			print("Sorry, not implemented yet")
			write_to_file(filename)

		elif ans=="3":
			#Show the entry
			show_entry()

		elif ans=="4":
			#Show the overall results for the whole file
			show_overall_results()

		elif ans=="5":
			#Add a repayment entry
			add_new_entry(entry_type="repayment")
			write_to_file(filename)

		elif ans=="0":
			break

		else:
			print("\n Unknown option, try again!")


def calculate_overall_results():	
	#Calculates the overall results for the whole file and returns them as list, corresponding to participants list
	result = [0.0]*len(participants)
	for entry in range(len(entry_names)):
		pass
		for participant in participants_in_entry[entry]:
			result[participant]+=calculate_entry_results(entry)[participant]

	return result


def show_overall_results():
	#prints the overall results for a file
	print("Overall debt per participant:",
		"\n".join([k[0]+":"+k[1] for k in zip(participants,[str(j) for j in calculate_overall_results()])]),

		sep='\n',end="\n")

def calculate_entry_results(index):
	#Calculates and returns the results on debts for an entry with index


	sum_payment=sum(payments_in_entry[index])

	individual_services2=[i[1:] for i in individual_services[index]]
	# print('individual_services2 ' + str(individual_services2))#debug
	sum_individuals=sum(sum(individual_services2,[]))#sums all numbers in list of lists

	sum_payment_without_individuals = sum_payment - sum_individuals
	amount_of_participants = len(participants_in_entry[index])

	#payment per participant without individual services
	base_payment_per_participant = sum_payment_without_individuals / amount_of_participants

	debug("index", index,"individual_services2", individual_services2)

	final_debt=[]
	for a in range(amount_of_participants):
		#add individual services to each participant's payment
		if(individual_services2[0]):
			sums_of_individuals_per_participant=sum([i[a] for i in individual_services2])
		else:
			sums_of_individuals_per_participant=0
		this_participant_to_pay= sums_of_individuals_per_participant + base_payment_per_participant
		final_debt+=[this_participant_to_pay-payments_in_entry[index][a]]

	return final_debt

def show_entry():
	#ask which entry to show and show it

	if not entry_names:
		print("This file contains no entries! Please add some!")
		return False

	entry_list=""
	for i in range(len(entry_names)):
		entry_list += str(i) + ") " + entry_names[i] + "; " + entry_dates[i] + "\n"

	while True:

		print(entry_list)
		ans=input("Which entry do you need? (Type e to exit): ")
		if ans.lower()=='e':
			break
		try:
			ans=int(ans)
		except ValueError:
			print("Wrong symbol, try again! \n")
		
		# try:
		if ans in range(len(entry_names)):
			#show the entry

			show_ind_services = ""
			show_debt = ""

			if  entry_names[ans] == "Repayment":
				pass
			else:
				if individual_services[ans][0]:
					show_ind_services ="Individual services:\n" + "\n\n".join([ j[0]+"\n"+ "\n".join([":".join(i) for i in zip(participants,[str(k) for k in j[1:]])]) for j in individual_services[ans]])
				show_debt = "Total debt for this entry (negative means the person should receive money):" + "\n".join([":".join(j) for j in zip([participants[i] for i in participants_in_entry[ans]],[str(i) for i in calculate_entry_results(ans)])])

			
			print("Name: " + entry_names[ans],
				"Date: " + entry_dates[ans],
				"Participants: " + ', '.join( [participants[int(i)] for i in participants_in_entry[ans]] ),
				"",
				"Payments per participant:", '\n'.join( [ participants[int(participants_in_entry[ans][i])] +": "+ str(payments_in_entry[ans][i])  for i in range(len(participants_in_entry[ans]))] ),
				"",
				show_ind_services,
				"",
				show_debt,
				"",
				sep='\n',end="\n")
		else:
			print("No such entry. Try again!")
		# except:

def add_new_entry(entry_type="default"):
	#Add new entry

	#Name this entry
	if entry_type=="default":
		entry_name=input("Please enter the name of this entry: ")
	elif entry_type=="repayment":
		entry_name="Repayment"

	#Date of the entry
	entry_date=input("Please enter the date of this entry (preferrable format: YYYYMMDD): ")

	#Define who participated in this entry
	
	list_of_participants = "\n"
	for i in range(len(participants)):
		list_of_participants += str(i) + ")" + participants[i] + "\n"
	if entry_type=="default":
		print(list_of_participants)
		s=input("Who participated in this entry? Write indicies of participants separated by comma or leave it blank if everybody participated:\n")
	elif entry_type=="repayment":
		#count everybody participating in repayment
		s=None

	if s:
		participants_in_entry_cur = [int(i) for i in s.split(',')]
	else:
		participants_in_entry_cur = [i for i in range(len(participants))]

	if entry_type=="repayment":
		print(list_of_participants)
		receiver=int(input("Who receives money in this repayment? Enter an index:"))
		# participants_in_entry_cur.remove(int(receiver))

	#manage how much each one paid
	payments_in_entry_cur = []
	for i in participants_in_entry_cur:

		if entry_type=="repayment":
			if i == receiver:
				#leave a receiver's payment at zero for now
				payments_in_entry_cur+=[0]
				continue

		payment=input("How much did " + participants[i] + " pay in this entry?: ")
		if payment:
			payments_in_entry_cur+=[float(payment)]
		else:
			payments_in_entry_cur+=[0]

	if entry_type=="repayment":
		#make receiver's payment a negative sum of other participants' payments
		pass
		payments_in_entry_cur[receiver]=-sum(payments_in_entry_cur)
		individual_services_cur = [[]]

	if entry_type=="default":
		#manage individual products or services
		individual_services_cur = []
		while True:
			ans=yes_no_dialog("Would you like to add individual products? [y/n]:" )
			if ans:
				#add a new individual service
				individual_services_cur += [add_individual_service(participants_in_entry_cur)]
			else:
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
