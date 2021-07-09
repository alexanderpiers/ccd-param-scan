import numpy as np
import os
import subprocess
from config import editConfigFile
import argparse
import time


def runParameterScan(paramsToScan, paramsScanVal, CCDDroneDir, outputdir, outputfile, baseconfig, number=1, verbose=False):

	outputBaseFilename = "Img_"

	configFiles = generateScanParamConfig(paramsToScan, paramsScanVal, baseconfig=baseconfig)

	for file in configFiles:
		if verbose:
			print("Running CCDDExpose on %s config file"%file)

		# Apply new settings
		loadNewSettingsProcess = subprocess.run([os.path.join(CCDDroneDir, "CCDDApplyNewSettings "), file], cwd=CCDDroneDir, stdout=True)
		
		# Make the output filename
		stripConfigFile = os.path.split(file)[-1].split(".")[0]

		for i in range(number):
			outputFilename = outputfile + stripConfigFile + "_" + str(i) + ".fits"

			# Expose and readout
			exposeProcess = subprocess.run([os.path.join(CCDDroneDir, "CCDDExpose"), 20, os.path.join(outputdir, outputFilename)], cwd=CCDDroneDir, stdout=True)
			
		if os.path.exists(file):
			os.remove(file)

	

def generateScanParamConfig(parametersToScan, parametersValue, baseconfig="config/config.ini" ):
	"""
		Recursive function that scans over parameters
	"""

	param = parametersToScan[-1]
	values = np.arange(*parametersValue[-1])

	configFilenames = []

	for val in values:

		# Edit the config file with the specific parameter
		config = baseconfig.split(".")[0]
		config = "{}_{}_{}".format(config, param, str(val))
		config = config.replace(".", "p")
		config += ".ini"

		editConfigFile(param, val, baseconfig=baseconfig, modifiedconfig=config)

		if len(parametersToScan) > 1:
			# Drop into the next depth of recursion 
			configFilenames.extend(generateScanParamConfig(parametersToScan[:-1], parametersValue[:-1], baseconfig=config))
			
			# Removes the not final modified configs
			if os.path.exists(config):
				os.remove(config)
		else:
			
			# edit config file and append to list
			configFilenames.append(config)

		

	return configFilenames

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="CLI for scanning CCD parameters")

	parser.add_argument("-o", "--outdir", default="data", help="Output directory for data")
	parser.add_argument("-d", "--drone" , default="/home/damic/CCDDrone", help="CCDDrone Directory")
	parser.add_argument("-c", "--config", default="config/config.ini", help="Base config file to modify")
	parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Mode")
	parser.add_argument("-s", "--scan", nargs="*", required=True, help="Parameter scan. Format: name start stop increment. Can scan over multiple parameters")
	parser.add_argument("-f", "--filename", default="Img_", help="Base of the output filename")
	parser.add_argument("-n", "--number", default=1, type=int, help="Number of images to take per settings")

	args = parser.parse_args()

	outputdir = args.outdir
	dronedir  = args.drone
	config    = args.config
	verbose   = args.verbose
	scanvars  = args.scan
	outfile   = args.filename
	numberOfExposures = args.number

	print(args)

	# Parse the scan values into the correct format
	if len(scanvars) % 4 != 0:
		print("Incorrect formatting provide for scan arguments. Must be in form: name start stop increment") 

	paramsToScan = []
	paramsScanVal = []
	for i in range(len(scanvars) // 4):
		paramsToScan.append(scanvars[i*4])
		paramsScanVal.append( tuple([float(x) for x in scanvars[i*4 + 1: (i+1)*4]]) )

	# Execute the scan
	print("Running parameter scan...")
	runParameterScan(paramsToScan, paramsScanVal, dronedir, outputdir, outfile, config, number=numberOfExposures, verbose=verbose)

