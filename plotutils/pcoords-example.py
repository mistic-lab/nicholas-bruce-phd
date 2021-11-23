import plotly.express as px
import pandas as pd
import argparse

def main(args):
    df = pd.read_csv(args.file, sep=',', header=0, index_col=0)

    # Headers are 'fc', 'bw', 't', 'P', 'c42', 'c63'

    if args.color is not None and args.color not in df.keys():
        raise Exception(f'The key you chose for the color axis does not exist. Options in this file are {df.keys()}')

    label_map = {"fc": "Center Frequency", "bw": "Bandwidth", "c42": "C42", "c63": "C63", "t": "Duration", "P": "Received Power" }

    fig = px.parallel_coordinates(df, color=args.color, labels=label_map, color_continuous_scale=px.colors.sequential.Rainbow, dimensions=)

    fig.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot pcoords from example file of RFI features",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@'
    )
    parser.add_argument('--file', '-f', type=str, default='pcoords-example.csv', help='CSV file to plot')
    parser.add_argument('--color','-c', type=str, default=None, help='key from csv file to use as color axis')

    args = parser.parse_args()
    main(args)