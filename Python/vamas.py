################################################################################
#
# vamas.py
#
# Provides a python VAMAS object for use by other apps.
#
################################################################################
#
# Copyright 2014 Kane O'Donnell
#
#     This library is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
# 
# NOTES
#
# 1. Yes, a lot of this stuff could have been made easier with NumPy. I've tried
# to avoid it so people can use this code with stock python.
# 
# 2. We implicitly assume here that any kinetic scale is given with respect to
# the Fermi level, not the vacuum level at the spectrometer. 
#
################################################################################
#
# Copyright 2021 Hideki NAKAJIMA
#
#    Revised Kane's code based on the practical usage on irregular vamas format.
#
################################################################################

from __future__ import division

class VAMAS:

	def __init__(self, filename):
		''' Can only init by providing a VAMAS file. '''
		
		f = open(filename)
		if f:
			lines = f.readlines()
			f.close()
			self.LoadFromText(lines)
		else:
			print('Error (vamas.py, VAMAS.__init__): File %s failed to open.')
			
	def LoadFromText(self, lines):
		''' Reads VAMAS text. Format taken from Dench et al, Surf. Interface Anal. 13 (1988) p 63.'''
		
		content = iter(lines)
		
		# First read content of the header.
		
		self.header = VAMASHeader(content)
		
		# Now grab all the blocks
		
		self.blocks = []
		for i in range(self.header.num_blocks):
			self.blocks.append(VAMASBlock(self.header, content)) # Block is an object
		
		# Should now get the experiment terminator: check.
		
		check_line = next(content).strip()
		if check_line != 'end of experiment':
			print('Warning (VAMAS.py, VAMAS::LoadFromText): Failed to find experiment terminator in expected place. VAMAS file may be corrupt.')
		
class VAMASHeader:
	
	def __init__(self, content):
		''' Parameter 'content' should be an iterator containing lines of text. '''
		
		self.LoadFromIterator(content)
	
	def LoadFromIterator(self, content):
		# remove lending blank lines
		i =0
		while i < 10 :
			self.format = next(content).strip()
			if self.format != '':
				break
			else:
				i += 1
		#print('Blank lines: '+ str(i))
		#self.format = next(content).strip()
		self.institution = next(content).strip()
		self.instrument = next(content).strip()
		self.operator = next(content).strip()
		self.experiment = next(content).strip()
		
		counter = int(next(content)) # number of comment lines
		self.comments = []
		for i in range(counter):
			self.comments.append(next(content).strip())
		
		self.experiment_mode =  next(content).strip()
		self.scan_mode = next(content).strip()
		
		if self.experiment_mode in ['MAP', 'MAPDP', 'NORM', 'SDP']:
			self.num_spectral_regions = int(next(content))
		else:
			self.num_spectral_regions = None
		
		if self.experiment_mode in ['MAP', 'MAPDP']:
			self.num_analysis_positions = int(next(content))
			self.num_x_coords = int(next(content))
			self.num_y_coords = int(next(content))
		else:
			self.num_analysis_positions = None
			self.num_x_coords = None
			self.num_y_coords = None
		
		counter = int(next(content)) # Number of experimental variables
		self.experimental_variable_names = []
		self.experimental_variable_units = []
		for i in range(counter):
			self.experimental_variable_names.append(next(content).strip())
			self.experimental_variable_units.append(next(content).strip())
		
		counter = int(next(content)) # Number of parameters on the inclusion
		# or exclusion list
		self.param_inclusion_exclusion_list = []
		for i in range(counter):
			self.param_inclusion_exclusion_list.append(next(content).strip())
		
		counter = int(next(content)) # Number of manually entered items in block
		self.manually_entered_items_list = []
		for i in range(counter):
			self.manually_entered_items_list.append(next(content).strip())
		
		counter = int(next(content)) # Number of future upgrade experiment entries
		self.num_future_upgrade_block_entries = int(next(content)) # Same for future upgrade blocks - use this later.
		
		self.future_upgrade_experiment_entries = []
		for i in range(counter):
			self.future_upgrade_experiment_entries.append(next(content).strip())
		
		self.num_blocks = int(next(content))
		
class VAMASBlock:

	def __init__(self, header, content):
		''' Parameter 'header' should be an initialized VAMASHeader object. 
		 Parameter 'content' should be an iterator containing lines of text. '''
		
		self.LoadFromIterator(header, content)
		if header.scan_mode == 'REGULAR':
			self.MakeAxes()
		self.ReorderOrdinates()
	
	def LoadFromIterator(self, header, content):
	
		self.header = header # So we always have a link back to the header data.
		self.name = next(content).strip()
		self.sample = next(content).strip()
		self.year = int(next(content))
		self.month = int(next(content))
		self.day = int(next(content))
		self.hours = int(next(content))
		self.minutes = int(next(content))
		self.seconds = int(next(content))
		self.GMT_offset = int(next(content))
		
		counter = int(next(content)) # Number of lines in block comment
		
		self.comments = []
		for i in range(counter):
			self.comments.append(next(content).strip())
		# checking validation of technique position after comment lines
		i =0
		while i < 10:
			self.technique = next(content).strip()
			if self.technique  in ['AES diff', 'AES dir', 'EDX', 'ELS', 'FABMS', 'FABMS energy spec', 'ISS', 'SIMS', 'SIMS energy spec', 'SNMS', 'SNMS energy spec', 'UPS', 'XPS', 'XRF']:
				break
			else:
				i += 1
		#print('Extra comment lines: ' + str(i))
		if header.experiment_mode in ['MAP', 'MAPDP']:
			self.x_coord = float(next(content))
			self.y_coord = float(next(content))
		
		self.experimental_variables = []
		
		for i in range(len(header.experimental_variable_names)):
			self.experimental_variables.append(float(next(content)))
		
		self.analysis_source = next(content).strip()
		
		if (header.experiment_mode in ['MAPDP', 'MADSVDP', 'SDP', 'SDPSV']) or self.technique in ['FABMS', 'FABMS energy spec', 'ISS', 'SIMS', 'SIMS energy spec', 'SNMS', 'SNMS energy spec']:
			self.sputtering_species_atomic_number = int(next(content))
			self.num_atoms_in_sputtering_particle = int(next(content))
			self.sputtering_species_charge = int(next(content))
		
		self.source_energy = float(next(content))
		self.source_strength = float(next(content))
		self.beam_width_x = float(next(content))
		self.beam_width_y = float(next(content))
		
		if header.experiment_mode in ['MAP', 'MAPDP', 'MAPSV', 'MAPSVDP', 'SEM']:
			self.field_of_view_x = float(next(content))
			self.field_of_view_y = float(next(content))
		
		if header.experiment_mode in ['MAPSV', 'MAPSVDP', 'SEM']:
			self.first_linescan_start_x = int(next(content))
			self.first_linescan_start_y = int(next(content))
			self.first_linescan_finish_x = int(next(content))
			self.first_linescan_finish_y = int(next(content))
			self.last_linescan_finish_x = int(next(content))
			self.last_linescan_finish_y = int(next(content))
		
		self.source_polar_angle = float(next(content))
		self.source_azimuth = float(next(content))
		self.analyser_mode = next(content).strip()
		self.analyser_pass_energy = float(next(content))
		
		if self.technique == 'AES diff':
			self.differential_width = float(next(content))
		
		self.analyser_mag = float(next(content))
		# Note: the next parameter is the workfunction for AES, EELS, ISS, UPS and XPS. It is the energy filter pass energy for FABMS, SIMS and SNMS.
		self.analyser_work_function = float(next(content))
		# R4000 vms has 1e+037 of WF.
		if self.analyser_work_function == 1e+037:
			self.analyser_work_function = 0
		self.target_bias = float(next(content))
		# Note: the following two parameters are called analysis widths but vary depending on the technique - see the original paper.
		self.analysis_width_x = float(next(content))
		self.analysis_width_y = float(next(content))
		self.analyser_polar_angle = float(next(content))
		self.analyser_azimuth = float(next(content))
		self.species = next(content).strip()
		# Note: next parameter is transition for e.g. XPS and AES and charge state for e.g. SIMS.
		self.transition = next(content).strip()
		self.charge_of_detected_particle = int(next(content))
		
		if header.scan_mode == 'REGULAR':
			self.abscissa_label = next(content).strip()
			self.abscissa_units = next(content).strip()
			self.abscissa_start = float(next(content))
			self.abscissa_increment = float(next(content))
		
		self.num_corresponding_variables = int(next(content))
		
		self.corresponding_variable_labels = []
		self.corresponding_variable_units = []
		for i in range(self.num_corresponding_variables):
			self.corresponding_variable_labels.append(next(content).strip())
			self.corresponding_variable_units.append(next(content).strip())
		
		self.signal_mode = next(content).strip()
		self.signal_collection_time = float(next(content))
		self.num_scans = int(next(content))
		self.signal_time_correction = float(next(content))
		
		if (self.technique in ['AES diff', 'AES dir', 'EDX', 'ELS', 'UPS', 'XPS', 'XRF']) and header.experiment_mode in ['MAPDP', 'MAPSVDP', 'SDP', 'SDPSV']:
			self.sputter_source_energy = float(next(content))
			self.sputter_beam_current = float(next(content))
			self.sputter_source_width_x = float(next(content))
			self.sputter_source_width_y = float(next(content))
			self.sputter_polar_angle = float(next(content))
			self.sputter_azimuth = float(next(content))
			self.sputter_mode = next(content).strip()
			
		self.sample_normal_tilt_polar_angle = float(next(content))
		self.sample_normal_tilt_azimuth = float(next(content))
		self.sample_rotation_angle = float(next(content))
		
		counter = int(next(content))
		self.additional_param_labels = []
		self.additional_param_units = []
		self.additional_param_values = []
		for i in range(counter):
			self.additional_param_labels.append(next(content).strip())
			self.additional_param_units.append(next(content).strip())
			self.additional_param_values.append(float(next(content)))
		
		self.future_upgrade_block_entries = []
		for i in range(header.num_future_upgrade_block_entries):
			self.future_upgrade_block_entries.append(next(content).strip())
		
		self.num_ordinate_values = int(next(content))
		
		self.minimum_ordinate_values = []
		self.maximum_ordinate_values = []
		for i in range(self.num_corresponding_variables):
			self.minimum_ordinate_values.append(float(next(content)))
			self.maximum_ordinate_values.append(float(next(content)))
		
		# The ordinates are next (FINALLY!). Just read them as a list and process later.
		
		self.ordinates = []
		for i in range(self.num_ordinate_values):
			self.ordinates.append(float(next(content)))
	
	def MakeAxes(self):
		''' Uses the abscissa data to construct binding energy and kinetic energy labels '''
		
		# So, the VAMAS file provides the number of ordinate values which is a multiple of the number of corresponding variables with number of ordinates for each variable. 
		# We also have the abscissa start and the increment. We can use this to generate a generic energy axis. 
		# On top of that, we can use the abscissa label to guess whether the abscissa is kinetic or binding (for electron spectroscopy) and then generate the other one using the photon energy and work function.
		
		# Note we have __future__ division here but we're explicitly casting just in 
		# case someone messes with the source code. Int division paranoia!
		num_ords = int(float(self.num_ordinate_values) / float(self.num_corresponding_variables))
		
		self.axis = []
		for i in range(num_ords):
			self.axis.append(self.abscissa_start + i * self.abscissa_increment)
		
		# Now, is the word kinetic in the label?
		if 'kinetic' in self.abscissa_label.lower():
			self.kinetic_axis = []
			self.binding_axis = []
			for i in range(num_ords):
				self.kinetic_axis.append(self.abscissa_start + i * self.abscissa_increment)
				self.binding_axis.append(-1 * (self.analyser_work_function) -1 * (self.abscissa_start + i * self.abscissa_increment) + self.source_energy)
		elif 'binding' in self.abscissa_label.lower():
			self.kinetic_axis = []
			self.binding_axis = []
			for i in range(num_ords):
				self.binding_axis.append(self.abscissa_start + i * self.abscissa_increment)
				self.kinetic_axis.append(-1 * (self.analyser_work_function) -1 * (self.abscissa_start + i * self.abscissa_increment) + self.source_energy)		
				
		# As a last item, calculate the dwell time per set of corresponding variables.
		self.dwell_time = float(num_ords) / self.signal_collection_time
		
	def ReorderOrdinates(self):
		''' Creates a list of lists by reordering the ordinate values. In the VAMAS file if there are N corresponding variables, the ordinates are listed as 1_1, .... 1_N, 2_1, .... , 2_N, etc where for each abscissa value all the corresponding values are listed in sequence. ReorderOrdinates creates a list [[1_1, 2_1, ...], ... , [1_N, 2_N, ...]], i.e. a list each for all the corresponding variables. '''
		
		num_ords = int(float(self.num_ordinate_values) / float(self.num_corresponding_variables))
		
		self.data = []
		
		for i in range(self.num_corresponding_variables):
			tmp = []
			for j in range(i, self.num_ordinate_values, self.num_corresponding_variables):
				tmp.append(self.ordinates[j])
			self.data.append(tmp)
		
		