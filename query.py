from psrqpy import QueryATNF
import logging

def query_atnf(output_file: str = 'atnf.txt') -> int:
    """
    Query the ATNF pulsar database and save specific pulsar parameters to a file.

    Parameters:
    - output_file: The file where the results will be saved (default is 'atnf.txt').

    Returns:
    - The number of pulsar entries saved to the file.
    """
    try:
        # Set up logging to track progress
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Querying ATNF database...')
        
        # Query the ATNF database
        query = QueryATNF(params=['P0', 'P1', 'EDOT', 'XX', 'YY', 'DIST', 'ASSOC', 'BINARY', 'TYPE', 'P1_I'])
        t = query.table
        logging.info('Query successful!')

        # Write query results to the output file
        counter = 0
        with open(output_file, 'w') as file:
            file.write(f'# P0 - P1 - EDOT - XX - YY\n')
            for row in t:
                P0 = row['P0']
                P1 = row['P1']
                EDOT = row['EDOT']
                XX = row['XX']
                YY = row['YY']
                
                # Check for valid data entries and format the output
                if P0 != '--' and P1 != '--' and EDOT != '--' and XX != '--' and YY != '--':
                    file.write(f'{P0:10.5e} {P1:10.5e} {EDOT:10.5e} {XX:10.3e} {YY:10.3e}\n')
                    counter += 1

        logging.info(f'Successfully saved {counter} objects to {output_file}.')
        return counter

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 0


def main():
    """
    Main function to query the ATNF pulsar database and save results to a file.
    """
    output_file = 'atnf.txt'
    total_saved = query_atnf(output_file)
    print(f"Saved {total_saved} objects to {output_file}.")

if __name__ == '__main__':
    main()
