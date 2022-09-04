import matplotlib.pyplot as plt
import argparse, os
from data_processing import *

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"\'{path}\' is not a valid path")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument( 
        'dataset_path', 
        metavar='DATASET PATH', 
        help='path to where the dataset files are', 
        type=dir_path
    )
    parser.add_argument( 
        'save_images_path', 
        metavar='SAVE IMAGES PATH', 
        help='existing path where the images will be saved (if \'ADDITIONAL DIRECTORY\' is not defined)', 
        type=dir_path
    )
    parser.add_argument( 
        '-d', '--additional_directory',
        metavar='ADDITIONAL DIRECTORY', 
        help='directory to be used/created inside \'SAVE IMAGES PATH\' where the images will be saved', 
        type=str
    )
    parser.add_argument(
        '--titles',
        action='store_true',
        help='[default] create charts with titles'
    )
    parser.add_argument(
        '--no-titles',
        action='store_false',
        dest= 'titles',
        help='create charts without titles'
    )
    parser.set_defaults(titles=True)
    return parser.parse_args()

def clearPlt():
    plt.cla()
    plt.clf()


def main():
    args = parse_arguments()

    save_to_path = os.path.join(args.save_images_path, args.additional_directory) if args.additional_directory else args.save_images_path
    if not os.path.exists(save_to_path):
        os.makedirs(save_to_path)
    
    setup( args.dataset_path, args.titles )

    ax = relative_amount_data_by_month()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'relative-amount-data-by-month.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_month()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-month.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_humidity_by_month()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-humidity-by-month.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_week()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-week.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_humidity_by_week()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-humidity-by-week.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = relative_occupancy_by_hour()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'relative-occupancy-by-hour.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = relative_occupancy_by_hour_week()
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'relative-occupancy-by-hour-week.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour(with_std=False)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour(with_std=True)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-std.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_with_occupancy(with_std=False)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-with-occupancy.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_with_occupancy(with_std=True)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-with-occupancy-std.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_week(with_std=False)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-week.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_week(with_std=True)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-week-std.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_week_with_occupancy(with_std=False)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-week-with-occupancy.pdf'),
        format='pdf'
    )

    clearPlt()

    ax = average_temperature_by_hour_week_with_occupancy(with_std=True)
    ax.get_figure().savefig(
        os.path.join(save_to_path, 'average-temperature-by-hour-week-with-occupancy-std.pdf'),
        format='pdf'
    )

    clearPlt()


if __name__ == "__main__":
    main()
