import glob

from quantify import get_involvement, get_resectability
from utils import get_discrete_degrees, get_rad_degrees, save_results
from plot import save_boxplot
from settings import *

if __name__ == '__main__':
    paths = [f for f in glob.glob('test_data/*')]

    resectability_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    degrees_matrix = [[], [], [], [], []]
    accuracy_degrees, accuracy_resectability = [], []
    resectability_rad, resectability_ai = [], []

    for scan in paths:
        if 'nrrd' in scan: patient_number = scan.split('.nrrd')[0].split('test_data/')[1].replace('_', '-')
        if 'nii' in scan: patient_number = scan.split('.nii.gz')[0].split('test_data/')[1].replace('_', '-')
        print("Analyzing patient ", patient_number)

        ai_vessel_assessment = [0, 0, 0, 0, 0]
        rad_vessel_assessment = [0, 0, 0, 0, 0]
        for vessel in range(len(vessels)):
            max_degrees = get_involvement(scan, vessels_id[vessel]) - 10
            ai_degrees = get_discrete_degrees(max_degrees)
            rad_degrees = get_rad_degrees(patient_number, vessels[vessel])

            if rad_degrees == 'None': continue

            accuracy_degrees.append(int(ai_degrees == rad_degrees))
            degrees_matrix[degrees_id.index(rad_degrees)].append((abs(max_degrees) + max_degrees) / 2)
            ai_vessel_assessment[vessel] = 0 if len(ai_degrees.split('-')) == 1 else int(ai_degrees.split('-')[1])
            rad_vessel_assessment[vessel] = 0 if len(rad_degrees.split('-')) == 1 else int(rad_degrees.split('-')[1])

        ai_res_stage = get_resectability(ai_vessel_assessment)
        rad_res_stage = get_resectability(rad_vessel_assessment)
        accuracy_resectability.append(int(ai_res_stage == rad_res_stage))

        resectability_matrix[resectability_id.index(rad_res_stage)][resectability_id.index(ai_res_stage)] += 1
        resectability_rad.append(resectability_id.index(rad_res_stage))
        resectability_ai.append(resectability_id.index(ai_res_stage))

    save_boxplot(degrees_matrix)
    save_results(accuracy_degrees, accuracy_resectability, degrees_matrix, resectability_matrix, resectability_rad,
                 resectability_ai)
