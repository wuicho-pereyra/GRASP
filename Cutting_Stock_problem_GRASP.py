import numpy as np
import os
import random
from random import randint
import csv


def loadCSV(pathRequeriments, pathStock):
	requeriments = np.loadtxt(pathRequeriments,delimiter = ',')

	materials = []

	fichero = open(pathStock,'rb')
	for line in fichero:
		local = []
		line = line.split(',')
		for item in line:
			if len(item)!=0 and item!='\n':
				local.append(float(item))
		materials.append(local)
	fichero.close()
	return requeriments,materials

def compute_waste(orderingList):
	globalResult = []
	wasteTotal = 0
	for i in range(len(orderingList)):
		waste = 0
		result = []
		if len(orderingList[i]) != 0:
			#print orderingList[i]
			line = []
			if len(orderingList[i]) > 1:
				for j in range(len(orderingList[i])):
					if j>0:
						if orderingList[i][j][1] <= waste:
							line.append(orderingList[i][j][1])	
							waste -= orderingList[i][j][1]
							if j == len(orderingList[i])-1:
								result.append([materialsList[i][2], materialsList[i][1], line])
						else:
							result.append([materialsList[i][2], materialsList[i][1], line])
							waste = materialsList[i][2] - orderingList[i][j][1]
							line = []
							line.append(orderingList[i][j][1])
							if j == len(orderingList[i])-1:
								result.append([materialsList[i][2], materialsList[i][1], line])
					else:
						line.append(orderingList[i][j][1])
						waste = materialsList[i][2]-orderingList[i][j][1]
			else:
				result.append([materialsList[i][2], materialsList[i][1], [orderingList[i][0][1]]])


			cuts = [len(result),materialsList[i][2], materialsList[i][1]]
			cost = 0
			for fil in range(len(result)):
				for column in range(len(result[fil][2])):
					cuts.append(result[fil][2][column])
					cost+=result[fil][2][column]
			cuts.append(len(result)*materialsList[i][2]-cost)
			wasteTotal+=len(result)*materialsList[i][2]-cost
			globalResult.append(cuts)

	return globalResult, wasteTotal

def select_tramo(available_tramos, materialsList, requerimentsList, idx):
	selections = np.where(available_tramos[:-1] != 0)[0]
	flag = 1
	while flag == 1:
		selection = available_tramos[random.choice(selections)]
		if materialsList[int(selection-1)][2] >= requerimentsList[idx-1][1]:
			flag = -1

	return selection


def GRASP(requeriments, materials, in_loop = 100, out_loop = 100):
	materialsList = []
	cont = 1
	for i in range(len(materials)):
		for j in range(2,len(materials[i])):
			materialsList.append([cont,materials[i][0],materials[i][j]])
			cont +=1
	requerimentsList = []

	for i in range(len(requeriments)):
		for j in range(int(requeriments[i][0])):
			requerimentsList.append([requeriments[i][2],requeriments[i][1]])

	#print requerimentsList
	#print
	#print materialsList
	#print

	candidatesList = np.empty([len(requerimentsList),len(materialsList)+1])

	for i in range(len(requerimentsList)):
		for j in range(len(materialsList)+1):
			if j == len(materialsList):
				candidatesList[i][j] = i+1
				continue
			if materialsList[j][1] == requerimentsList[i][0]:
				candidatesList[i][j] = materialsList[j][0]
			else:
				candidatesList[i][j] = 0

	#print candidatesList
	#print			

	in_loop = 100
	out_loop = 100

	for n in range(out_loop):
		solutions = []
		for i in range(len(requerimentsList)):
			selection = select_tramo(candidatesList[i], materialsList, requerimentsList, i+1)
			solutions.append([candidatesList[i][-1],requerimentsList[i][1],selection])

		typesMaterialsCut = range(1,len(candidatesList[0])+1)
		solutions = np.array(solutions)

		orderingList = []
		for i in range(len(typesMaterialsCut)):
			orderingList.append(solutions[np.where(solutions[:,-1] == typesMaterialsCut[i])[0]])

		for i in range(len(orderingList)):
			orderingList[i] = orderingList[i][orderingList[i][:,1].argsort()]

		#print orderingList
		#print

		[sol_opt, waste_opt] = compute_waste(orderingList)
		#print sol_opt
		#print waste_opt
		#print

		for m in range(in_loop):
			orderingList_aux = [x for x in orderingList if len(x) != 0]
			modify_cut = random.choice(random.choice(orderingList_aux))
			idx_modify_cut = modify_cut[0]
			typ_modifi_cut = modify_cut[2]
			tramos_modify_cut = candidatesList[np.where(candidatesList[:,-1] == idx_modify_cut)][0]
			selection = select_tramo(tramos_modify_cut, materialsList, requerimentsList, int(idx_modify_cut))
			modify_cut_new = list(modify_cut)
			modify_cut_new[2] = selection

			#print modify_cut
			#print idx_modify_cut
			#print typ_modifi_cut
			#print tramos_modify_cut
			#print selection
			#print modify_cut_new
			#print

			a = np.where(orderingList[int(typ_modifi_cut)-1][:, 0] == idx_modify_cut)
			#print a[0][0]
			#print np.delete(orderingList[int(typ_modifi_cut)-1], a, 0)
			#print
			#print orderingList
			#print
			#print np.insert(orderingList[int(selection)-1], 0, modify_cut_new, axis = 0)
			#print
			#print

			orderingList_new = []
			for i in range(len(typesMaterialsCut)):
				if i+1 != typ_modifi_cut and i+1 != selection:
					orderingList_new.append(orderingList[i])
					#print orderingList[i]
					#print
				else:
					if i+1 == typ_modifi_cut:
						orderingList_aux = np.delete(orderingList[i], a, 0)
						flag = 1
					if i+1 == selection:
						if flag == 1:
							orderingList_aux = np.insert(orderingList_aux, 0, modify_cut_new, axis = 0)
						else:
							orderingList_aux = np.insert(orderingList[i], 0, modify_cut_new, axis = 0)
					flag = -1
					#print '--------------'
					#print orderingList[i]
					#print '--------------'
					#print orderingList_aux
					orderingList_new.append(orderingList_aux)

			#print orderingList_new

			[sol_opt_aux, waste_opt_aux] = compute_waste(orderingList_new)
			#print sol_opt_aux
			#print waste_opt_aux
			#print

			if waste_opt_aux < waste_opt:
				sol_opt = sol_opt_aux
				waste_opt = waste_opt_aux
				orderingList = orderingList_new
				#print n, m, waste_opt

		#print '---------'
		#print sol_opt
		#print waste_opt
		#print

		if n == 0:
			sol_opt_global = sol_opt
			waste_opt_global = waste_opt
		else:
			if waste_opt < waste_opt_global:
				sol_opt_global = sol_opt
				waste_opt_global = waste_opt
		print n, waste_opt_global

	print '///////////////////////////////'
	print waste_opt_global
	print
	#print sol_opt_global

	count = 0


	with open('Cortes de requerimientos.csv', 'wb') as csvfile:
	    solutionCSV = csv.writer(csvfile)
	    for i in range(len(sol_opt_global)):
	    	count += len(sol_opt_global[i][4::])
	        solutionCSV.writerow(sol_opt_global[i])
	    solutionCSV.writerow(['Desperdicio'])
	    solutionCSV.writerow([waste_opt_global])

	print count

##################################################################

pathRequeriments = os.getcwd()+'/requeriments.csv'
pathStock = os.getcwd()+'/stock.csv'

[requeriments, materials] = loadCSV(pathRequeriments, pathStock)