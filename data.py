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

    return parser.parse_args()

def main():
    args = parse_arguments()
    
    setup( args.dataset_path )

    print_general_data_information()
    print()

    print( "--> STATE INFORMATION MESSAGE:")
    print_information_state_message()
    print()

    print( "--> FEEDBACK INFORMATION MESSAGE:")
    print_information_feedback_message()
    print()

    print( "--> TEMPERATURE, HUMIDITY AND PRESSURE INFORMATION MESSAGE:")
    print_information_temp_humid_press_message()
    print()

    print( "--> DOOR INFORMATION MESSAGE:")
    print_information_door_message()
    print()

    print( "--> MOVEMENT INFORMATION MESSAGE:")
    print_information_movement_message()
    print()

    print( "--> METEOROLOGY INFORMATION MESSAGE:")
    print_information_meteorology_message()


def print_general_data_information():
    info = general_information_by_tenant()
    
    heading= f" {'   tenant':17}{'|':6}{'start date':15}{'|':6}{' end date ':15}{'|':6}{'rate hours with at least one log'} "
    print(heading)
    print('-'*len(heading))
    for elem in info:
        print(
            f" {elem['tenant']:17}"
            f"{'|':6}{elem['start date']:15}"
            f"{'|':6}{elem['end date']:15}"
            f"{'|':14}{elem['rate hours with at least one log']:>9.0f}%"
        )

def print_information_state_message():
    info = information_state_message()
    
    header = f"{'  device':11}{'|':28}{'state':29}"
    print(header)
    print( '-'*len(header) )
    for k in info:
        print( f" {k:10}|  {list( info[k] ) }")

def print_information_feedback_message():
    info = information_feedback_message()
    
    header = f"{'  device':11}{'|':28}{'state':29}"
    print(header)
    print( '-'*len(header) )
    for k in info:
        print( f" {k:10}|  {list( info[k] ) }")

def print_information_temp_humid_press_message():
    info = information_temp_humid_press_message()
    
    heading= f"{'  variable':15}{'|':5}{' type'} {'|':1}{'has null':>10} {'|':2}{' min value'} {'|':2}{' max value'} "
    print(heading)
    print('-'*len(heading))

    for k in info:
        variable = k
        datatype = info[k]['type']
        hasnull = 'yes' if info[k]['has null'] else 'no'
        minvalue = info[k]['min value']
        maxvalue = info[k]['max value']

        print( f" {variable:14}|{datatype:>9} |{hasnull:>10} |{minvalue:11} |{maxvalue:10}")


def print_information_door_message():
    info = information_door_message()

    heading= f"{'  variable':15}{'|':5}{' type'} {'|':1}{'has null':>10} {'|':2}{' min value'} {'|':2}{' max value'} "
    print(heading)
    print('-'*len(heading))

    contact = info['contact']
    print( f" {'contact':14}|{contact['type']:>9} |{'yes' if contact['has null'] else 'no':>10} |{'-':>11} |{'-':>10}")

    for k in info:
        if k == 'contact':
            continue

        variable = k
        datatype = info[k]['type']
        hasnull = 'yes' if info[k]['has null'] else 'no'
        minvalue = info[k]['min value']
        maxvalue = info[k]['max value']

        print( f" {variable:14}|{datatype:>9} |{hasnull:>10} |{minvalue:11} |{maxvalue:10}")

def print_information_movement_message():
    info = information_movement_message()

    heading= f"{'  variable':15}{'|':5}{' type'} {'|':1}{'has null':>10} {'|':2}{' min value'} {'|':2}{' max value'} "
    print(heading)
    print('-'*len(heading))

    occupancy = info['occupancy']
    print( f" {'occupancy':14}|{occupancy['type']:>9} |{'yes' if occupancy['has null'] else 'no':>10} |{'-':>11} |{'-':>10}")

    for k in info:
        if k == 'occupancy':
            continue

        variable = k
        datatype = info[k]['type']
        hasnull = 'yes' if info[k]['has null'] else 'no'
        minvalue = info[k]['min value']
        maxvalue = info[k]['max value']

        print( f" {variable:14}|{datatype:>9} |{hasnull:>10} |{minvalue:11} |{maxvalue:10}")

def print_information_meteorology_message():
    info = information_meteorology_message()

    heading= f"{'  variable':15}{'|':5}{' type'} {'|':1}{'has null':>10} {'|':2}{' min value'} {'|':2}{' max value'} "
    print(heading)
    print('-'*len(heading))

    different = info['description']
    print( f" {'description':14}|{different['type']:>9} |{'yes' if different['has null'] else 'no':>10} |{'-':>11} |{'-':>10}")

    different = info['winddirection']
    print( f" {'winddirection':14}|{different['type']:>9} |{'yes' if different['has null'] else 'no':>10} |{'-':>11} |{'-':>10}")

    for k in info:
        if k == 'winddirection' or k == 'description':
            continue

        variable = k
        datatype = info[k]['type']
        hasnull = 'yes' if info[k]['has null'] else 'no'
        minvalue = info[k]['min value']
        maxvalue = info[k]['max value']

        print( f" {variable:14}|{datatype:>9} |{hasnull:>10} |{minvalue:11} |{maxvalue:10}")


if __name__ == "__main__":
    main()