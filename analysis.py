# use a generator to filter out dates that I don't want.

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from statistics import median


def get_weeks(start_date, number_of_weeks):
	return [start_date + relativedelta(weeks=x) for x in range(number_of_weeks+1)]

def retrieve_rows_within_dates(filename, from_date_exclusive, to_date_inclusive):
	with open(filename) as f:
		next(f)  # skip first row, i.e. column names.
		for line in f:
			line_as_array = line.split(',')
			disbursal_date = datetime.strptime(line_as_array[3], "%Y/%m/%d") # e.g.2020/02/29
			if disbursal_date > from_date_exclusive and disbursal_date <= to_date_inclusive:
				original_loan_amount = line_as_array[4]
				lending_rate = line_as_array[10]
				latest_status = line_as_array[11]
				yield (disbursal_date, float(original_loan_amount)*100, float(lending_rate)*10000, latest_status)

def metrics_for_loans(loans):
	a = loans
	max_date = max((row[0] for row in a))
	min_date = min((row[0] for row in a))
	print('Max date:' + str(max_date))
	print('Min date:' + str(min_date))
	number_of_loans = len(a)
	print('Number of loans: ' + str(number_of_loans))
	total_money_disbursed = sum((row[1] for row in a))
	print('Total money disbursed: ' + str(total_money_disbursed))
	sum_of_lending_rate = sum((row[2] for row in a))
	average_lending_rate_per_loan = sum_of_lending_rate / number_of_loans
	print('Average lending rate per loan: ' + str(average_lending_rate_per_loan))
	sum_of_product_of_money_disbursed_and_lending_rate = sum((row[1]*row[2] for row in a))
	average_lending_rate_per_unit_money = sum_of_product_of_money_disbursed_and_lending_rate / total_money_disbursed
	print('Average lending rate per unit money: ' + str(average_lending_rate_per_unit_money))
	max_lending_rate = max((row[2] for row in a))
	print('Max lending rate: ' + str(max_lending_rate))
	min_lending_rate = min((row[2] for row in a))
	print('Min lending rate: ' + str(min_lending_rate))
	median_lending_rate = median((row[2] for row in a))
	print('Median loan lending rate: ' + str(median_lending_rate))
	print('-----------------------')
	return (min_date, max_date, number_of_loans, total_money_disbursed, average_lending_rate_per_loan, average_lending_rate_per_unit_money, max_lending_rate, min_lending_rate, median_lending_rate)


# Get your data from https://www.bankofengland.co.uk/boeapps/iadb/Repo.asp
def get_boe_interest_rate(filename, from_date_exclusive, to_date_inclusive):
	with open(filename) as f:
		next(f)
		for line in f:
			line_as_array = line.replace('\"', '').split(',')
			decision_date = datetime.strptime(line_as_array[0], '%d %b %y') # e.g. 29 Feb 20
			if decision_date > from_date_exclusive and decision_date <= to_date_inclusive:
				yield (decision_date, float(line_as_array[1]) * 100.0)

# TODO
#def find_defaults_within_dates
	# find principal losses
	# find interest losses


if __name__ == '__main__':
	
	start_date = datetime(2019,12,31,0,0)
	number_of_weeks = 13
	weeks = get_weeks(start_date, number_of_weeks)
	last_date = max(weeks)
	print(last_date)
	data = [
		metrics_for_loans(list(retrieve_rows_within_dates(
			'data_for_loanbook_extract_2020-04-01.csv',
			weeks[i],
			weeks[i+1]
		)))
		for i in range(number_of_weeks)
	]
	
	df = pd.DataFrame(data, columns=['min_date', 'max_date', 'number_of_loans', 'total_money_disbursed', 'average_lending_rate_per_loan', 'average_lending_rate_per_unit_money', 'max_lending_rate', 'min_lending_rate', 'median_lending_rate'])
	df.to_csv('output.csv')
	
	
	boe_data = list(get_boe_interest_rate('boe-rate.csv', start_date, last_date))
	boe_df = pd.DataFrame(boe_data, columns=['decision_date', 'rate'])
	
	week_starts = df['min_date']
	plt.plot(week_starts, df['min_lending_rate'], 'g--', label='min loan')
	plt.plot(week_starts, df['median_lending_rate'], 'kx', label='median loan')
	plt.plot(week_starts, df['average_lending_rate_per_unit_money'], 'bo', label='sterling weighted average')
	plt.plot(week_starts, df['max_lending_rate'], 'r^', label = 'max loan')
	plt.plot(boe_df['decision_date'], boe_df['rate'], '-k', label = 'BoE Base Rate')
	plt.legend(loc='upper left')
	plt.xlabel('Week starting')
	plt.ylabel('Interest Rate (bps)')
	plt.show()
	

	
