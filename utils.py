import nrrd
import nibabel as nib
import numpy as np
import pandas as pd
import sklearn
import csv
import scipy.stats as stats
from sklearn import metrics


def get_rad_degrees(patient_number, vessel):
    data = pd.read_excel(r'db_vessels.xlsx', engine='openpyxl')
    df_patient = data[data['number'] == patient_number]
    rad_degrees = df_patient[vessel + '2'].values[0] if len(df_patient) > 0 else 'None'
    return rad_degrees if rad_degrees != 'no' else '0'


def get_discrete_degrees(max_degrees):
    bins = [360, 270, 180, 90, 0]
    result = '0'
    for i in range(len(bins) - 1):
        if max_degrees <= bins[i]: result = str(bins[i + 1]) + '-' + str(bins[i])
    return result


def get_scan(path):
    if 'nii.gz' in path:
        nii_mask = nib.load(path)
        return np.array(nii_mask.dataobj)
    else:
        nrrd_mask = nrrd.read(path)
        return np.array(nrrd_mask)[0]


def get_selected_segments(slice, vessel):
    for j in range(0, 23):
        if j == vessel or j == 20: continue
        slice = np.where(slice == j, 7, slice)
    slice = np.where(slice == vessel, 5, slice)
    slice = np.where(slice == 20, 3, slice)

    return slice


def get_cropped_slice(slice):
    left_row = np.where(slice == 5)[0][0] - 1 if np.where(slice == 5)[0][0] < np.where(slice == 3)[0][0] else \
        np.where(slice == 3)[0][0] - 1
    left_column = min(np.where(slice == 5)[1]) - 1 if min(np.where(slice == 5)[1]) < min(
        np.where(slice == 3)[1]) else min(np.where(slice == 3)[1]) - 1

    right_row = np.where(slice == 5)[0][len(np.where(slice == 5)[0]) - 1] + 2 if np.where(slice == 5)[0][len(
        np.where(slice == 5)[0]) - 1] > np.where(slice == 3)[0][len(np.where(slice == 3)[0]) - 1] else \
        np.where(slice == 3)[0][len(np.where(slice == 3)[0]) - 1] + 2
    right_column = max(np.where(slice == 5)[1]) + 2 if max(np.where(slice == 5)[1]) > max(
        np.where(slice == 3)[1]) else max(np.where(slice == 3)[1]) + 2

    return slice[left_row:right_row, left_column:right_column]


def get_plane(plane, scan, slice_id):
    if plane == 'ax':
        return scan[:, :, slice_id]
    elif plane == 'sag':
        return scan[:, slice_id, :]
    elif plane == 'cor':
        return scan[slice_id, :, :]


def get_contact_map(image, kernel, padding=0, strides=1):
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding * 2, image.shape[1] + padding * 2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                except:
                    break

    return output


def get_contact(cropped_slice):
    kernels = [np.array([[1], [1]]), np.array([[1, 1]]), np.array([[1, 0], [0, 1]]), np.array([[0, 1], [1, 0]])]
    contact_map = [get_contact_map(cropped_slice, kernel) for kernel in kernels]

    tumor_contact = 0
    background_contact = 0
    for conv_map in contact_map:
        tumor_contact += np.count_nonzero(conv_map == 8)
        background_contact += np.count_nonzero(conv_map == 12)
    return tumor_contact, background_contact


def save_results(accuracy_degrees, accuracy_resectability, degrees_matrix, resectability_matrix, resectability_rad, resectability_ai):
    f_value, p_value = stats.f_oneway(degrees_matrix[0], degrees_matrix[1], degrees_matrix[2], degrees_matrix[3])
    f = open('results.csv', 'a')
    writer = csv.writer(f)
    writer.writerow(
        ['Overall accuracy for quantifying vascular involvement is ' + str(sum(accuracy_degrees) / len(accuracy_degrees)) + ' (' + str(sum(accuracy_degrees)) + '/' + str(len(accuracy_degrees)) + ')'])
    writer.writerow(["ANOVA result for vascular involvement is: f-value " + str(f_value) + ', p-value ' + str(p_value)])
    writer.writerow(["Overall accuracy for determining resectability stage is " + str(sum(accuracy_resectability) / len(accuracy_resectability))])
    writer.writerow(["Weighted kappa for resectability is " + str(sklearn.metrics.cohen_kappa_score(resectability_rad, resectability_ai))])
    writer.writerow(["Confusion matrix for vessel resectability is "] + resectability_matrix)
    f.close()
