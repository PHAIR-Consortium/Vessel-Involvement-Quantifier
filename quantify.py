import numpy as np
from utils import get_scan, get_cropped_slice, get_plane, get_selected_segments, get_contact, get_contact_map


def get_involvement(path, vessel):
    scan = get_scan(path)

    max_degrees = 0
    planes = ['cor', 'sag', 'ax']

    for plane in range(len(planes)):
        for slice_id in range(0, scan.shape[plane]):
            slice = get_plane(planes[plane], scan, slice_id)
            slice = get_selected_segments(slice, vessel)

            if len(np.where(slice == 5)[0]) == 0 or len(np.where(slice == 3)[0]) == 0: continue

            cropped_slice = get_cropped_slice(slice)

            tumor_contact, background_contact = get_contact(cropped_slice)
            degrees = tumor_contact / (tumor_contact + background_contact) * 360 if (tumor_contact + background_contact) != 0 else 0
            if max_degrees < degrees: max_degrees = degrees

    return max_degrees


def get_resectability(res_map):
    if res_map[0] == 0 and res_map[1] == 0 and res_map [2] == 0 and res_map[3] <= 90 and res_map[4] <= 90:
        return 'resectable'
    if res_map[0] <= 90 and res_map[1] <= 90 and res_map [2] <= 90 and res_map[3] <= 270 and res_map[4] <= 270:
        return 'borderline resectable'
    return 'non resectable'

