import subprocess
from tempfile import mkstemp
import os
import shutil
import csv

class TradisEssentiality:
	def __init__(self, tabfile, verbose, exec="tradis_essentiality.R"):
		self.tabfile = tabfile
		self.exec     = exec
		self.verbose = verbose
		
		fd, self.output_filename = mkstemp()
		fd, self.essential_filename = mkstemp()

	def construct_command(self):
		return " ".join([self.exec,  self.tabfile])
		
	def run(self):
		if self.verbose:
			print(self.construct_command())
		subprocess.check_output(self.construct_command(), shell=True)
		
		self.replace_comma_tabs(self.tabfile +".all.csv", self.output_filename)
		shutil.copy(self.tabfile +".essen.csv", self.essential_filename)
		
		if self.verbose:
			print("all.csv\t" + self.output_filename)
			print("essen.csv\t" + self.essential_filename)
		
		os.remove(self.tabfile +".all.csv")
		os.remove(self.tabfile +".essen.csv")
		os.remove(self.tabfile +".ambig.csv")
		os.remove(self.tabfile +".QC_and_changepoint_plots.pdf")
		os.remove(self.tabfile )
		
		return self
		
	def replace_comma_tabs(self, input_file, output_file):
		with open(input_file, newline='') as csvfile:
			comparison_reader = csv.reader(csvfile, delimiter=',')
			
			with open(output_file, 'w') as outputfh:
				for line in comparison_reader:
					outputfh.write("\t".join(line)+"\n")
