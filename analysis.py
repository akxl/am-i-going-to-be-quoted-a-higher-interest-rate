# use a generator to filter out dates that I don't want.

from datetime import datetime


def retrieve_rows_within_dates(filename, from_date, to_date):
	with open(filename) as f:
		next(f)  # skip first row, i.e. column names.
		for line in f:
			line_as_array = line.split(',')
			disbursal_date = datetime.strptime(line_as_array[3], "%Y/%m/%d")
			if disbursal_date >= from_date and disbursal_date <= to_date:
				original_loan_amount = line_as_array[4]
				lending_rate = line_as_array[10]
				latest_status = line_as_array[11]
				yield (disbursal_date, float(original_loan_amount), float(lending_rate), latest_status)

def print_metrics_for_loans(loans):
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
	print('Average lending rate per loan: ' + str(sum_of_lending_rate / number_of_loans))
	sum_of_product_of_money_disbursed_and_lending_rate = sum((row[1]*row[2] for row in a))
	print('Average lending rate per unit money: ' + str(sum_of_product_of_money_disbursed_and_lending_rate / total_money_disbursed))
	print('-----------------------')


if __name__ == '__main__':
	print_metrics_for_loans(list(retrieve_rows_within_dates(
				'data_for_loanbook_extract_2020-04-01.csv', 
				datetime(2020,3,1,0,0), 
				datetime(2020,3,31,0,0))
			))
	
	print_metrics_for_loans(list(retrieve_rows_within_dates(
				'data_for_loanbook_extract_2019-10-01.csv', 
				datetime(2019,9,1,0,0), 
				datetime(2019,9,30,0,0))
			))
	
	
