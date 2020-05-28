Am I going to be quoted a higher interest rate today?
=====================================================

I got curious, given the current virus lockdown, people not being able to service their loans and other financial concerns, would I likely be quoted a higher interest rate for an unsecured personal loan.

So I wrote this short script up. Nothing too fancy, and it is not the most time efficient (it is terribly slow). I just wanted to scratch this itch, that's all. Not doing into default rates, credit spreads, yield curves, repo rates and what not.

Just requires Zopa's loan book from their website and the Bank of England's base rate.


To use:
-------

1. Go to Zopa's website to download their loanbook.
2. Go to https://www.bankofengland.co.uk/boeapps/iadb/Repo.asp to download a CSV of the latest base rates.
3. Insert the filenames into the python file `analysis.py` where needed.
4. Adjust dates.
5. Run `python3 analysis.py`.
