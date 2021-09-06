# XPS vamas format conversion into tab-delimited text files
import sys, os, re
import vamas

def list_vms(filePath):
	vamas1 = vamas.VAMAS(filePath) # create instance
	
	print(str(vamas1.header.format))
	print('Number of blocks: ' + str(vamas1.header.num_blocks))
	#for x in vamas1.blocks:
	#	print(str(x.name))
	
	dir = os.path.dirname(filePath)
	fileName = os.path.basename(filePath)
	fileName = os.path.splitext(fileName)[0]
	list_file = []
	#exit()
	p = 0
	for block in vamas1.blocks:
		p += 1
		id = block.sample + block.name
		id = ''.join(e for e in id if e.isalnum())                                # remove special characters and leave alpha and num
		print(str(p) + ' : ' + str(id))
		
		ElemD = block.species + block.transition
		ElemD = ''.join(e for e in ElemD if e.isalnum())                                 # remove special characters and leave alpha and num
		tfilePath = str(dir + os.sep + fileName + '_' + id + '_' + ElemD + '.txt')                                # filename exported from vms
		print(tfilePath)
		list_file.append(tfilePath)
		numData = int(float(block.num_ordinate_values) / float(block.num_corresponding_variables))                                # equivalent to num_ods
		if vamas1.header.scan_mode == 'REGULAR':
			if block.abscissa_label.lower() == 'binding energy':
				strMode = 'BE/eV'
			if block.abscissa_label.lower() == 'kinetic energy':
				strMode = 'KE/eV'
			if block.abscissa_label.lower() == 'photon energy':
				strMode = 'PE/eV'
		
			Para = block.technique + ' source:' + str(block.source_energy) + ', spec:' + str(ElemD) + ', ' + strMode + ':' + str(block.abscissa_start) + ', dE:' + str(block.abscissa_increment) + ', pnts:' + str(numData)
			print(Para)
			if block.technique in ['XPS', 'UPS']:
				Text = 'BE/eV' + '\t' + 'PE: ' + str(block.source_energy) + ' eV'  + '\n'                                # header of exported txt
			else:
				Text = strMode + '\t' + 'EE: ' + str(block.source_energy) + ' eV'  + '\n' 
			print(Text)
			for j in range(numData):
				if block.technique in ['XPS', 'UPS']:
					x = str(block.binding_axis[j])
				else:
					x = str(block.axis[j])
				y = str(block.data[0][j])
				Text += x + '\t' + y + '\n'
				#if j == 0 or j == numData - 1:
				#	print(x + '\t' + y)
			with open(tfilePath, 'w') as file:
				file.write(str(Text))
			file.close
		
	return list_file

