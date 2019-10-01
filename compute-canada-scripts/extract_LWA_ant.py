import numpy as np
from lsl.reader.ldp import LWASVDataFile
import argparse


parser = argparse.ArgumentParser('Pulls a single antenna into a separate .dat file from LWA data')
parser.add_argument('--input', type=string, help='raw LWA-SV file path')
parser.add_argument('--stand', type=int, default=5, help='DP stand ID')
parser.add_argument('--pol', type=int, default=0, help='antenna polarization')
parser.add_argument('--output', type=string, help='output file name')
args = parser.parse_args()

def extract_single_ant(input_file, dp_stand_id, polarization):
    """Extract and combine all data from a single antenna into a numpy array.

    Parameters
    ----------
    input_file : string
                raw LWA-SV file path
    DP_stand_id : int
                stand id from 1 to 256 inclusive
    polarization : int
                antenna polarization

    Returns
    -------
    numpy array
        array of size (avail frames, bandwidth)
    """

    input_data = LWASVDataFile(input_file)
    output_data = []

    while input_data.getRemainingFrameCount() > 0:
        current_frame = input_data.readFrame()

        if current_frame.parseID() == (dp_stand_id, polarization):
            for i in range(len(current_frame.data.iq)):
                output_data.append(current_frame.data.iq[i])

    output_data = np.array(output_data)

    return output_data

antenna_array = extract_single_ant(args.input, args.stand, args.output)

antenna_array.tofile(args.output)