import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        database = list(reader)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as dnafile:
        sequence = dnafile.read()

    # TODO: Find longest match of each STR in DNA sequence
    matches = {}

    # This results in "name" : 0
    for i in database[0]:
        # where sequence is the full dna sequence and i is the subsequence like agat
        matches[i] = (longest_match(sequence, i))

    # TODO: Check database for matching profiles
    suspect = 'No Match'
    suspect_counter = 1

    for i in range(len(database)):
        for j in matches:
            # Matches values are ints, need to cast them to strings for comparison
            if str(matches[j]) == database[i][j]:
                suspect_counter += 1
        if suspect_counter == len(matches):
            # We've got the suspect!  No need to continue
            suspect = database[i]['name']
            break
        else:
            suspect_counter = 1

    print(suspect)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
