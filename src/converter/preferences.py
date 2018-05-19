import configparser

class Preferences:
	def __init__(self, fname):
		self.fname = fname
		self.config = configparser.RawConfigParser()
		
	def setPref(self, section, par, val):
		if self.config.has_section(section):
			self.config[section][par] = val
		else:
			self.config[section] = {}
			self.config[section][par] = val
	def getPref(self, section, par):
		if self.config.has_option(section, par):
			res = self.config[section][par]
		else:
			res = ''
		return res
		
	def save(self):
		with open(self.fname, 'w') as configfile:
			self.config.write(configfile)
	
	def load(self):
		self.config.read(self.fname)
