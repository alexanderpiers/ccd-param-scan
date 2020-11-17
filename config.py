import os

def editConfigFile(parameter, newValue, baseconfig="config/config.ini", modifiedconfig="config/config-mod.ini", verbose=False):
	"""
		Reads in the CCD drone config file and edits the given parameters 

	"""

	# Check if in an outfiles are the same
	newConfigContent = ""
	infile = open(baseconfig, "r")

	for line in infile:

		# Strip the first part, check if it matches the parameter
		configFileParameterName = line.split("=")[0].strip()

		# If we get a match, write the new parameter, otherwise write the original line
		if configFileParameterName == parameter:
			newConfigLine = parameter + " = " + str(newValue) + "  ; MODIFIED\n" 
			newConfigContent += newConfigLine
			
			if verbose:
				print("Found line to modify!")
				print("Writing: " + newConfigLine)

		else:
			newConfigContent += line

	infile.close()

	outfile = open(modifiedconfig, "w+")
	outfile.write(newConfigContent)
	outfile.close()

if __name__ == '__main__':

	# Test the edit capabilities
	editConfigFile("two_og_hi", -1, verbose=True, baseconfig="config/config-mod.ini", modifiedconfig="config/config-mod.ini")