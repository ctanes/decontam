""" parsers for input files
"""

import re
import csv
import os

def parse_tool_names(tool_file_handle):
    """ parse file with list of tools, each tool should be on its own line:
        tool1
        tool2
        ...
        
        Returns:
             list with tool names
        Raises:
             IOError if cannot parse file
    """
    tools = []
    for line in tool_file_handle:
        tool = str.strip(line)
        tools.append(tool)
    if not tools:
        raise IOError("empty tool file")
    return tools


def check_file_exists(label, file_name):
    if not os.path.isfile(file_name): 
        raise IOError(label + "file :" + file_name + 
            "does not exist. Check file name or remove it from sample file.")


def check_number_of_rows(row, num_description_for_sample):
    if len(row) != num_description_for_sample:
        raise IOError("each sample should have " + str(num_description_for_sample) +
            " columns: sample_name fastq annotation") 


def parse_samples(samples_file_handle):
    """ parses file with list of test cases. 

    Each test case has name, FASTQ and annotation(for each read from FASTQ).

    Returns:
        list of tuples, each element of the list is a test case, 
        each test case is a tuple
        (1st element sample name, 2nd fastq file, 3rd annotation file)

    Raises: 
        IOError if cannot parse file
        IOError if cannot find fastq file
        IOError if cannot find annotation file
    """
    num_description_for_sample = 3 # name fastq annotation
    samples = []
    reader = csv.reader(samples_file_handle, delimiter="\t")
    for row in reader:
        check_number_of_rows(row, num_description_for_sample)
        sample_name = row[0]
        fastq_file = row[1]
        check_file_exists("FASTQ", fastq_file)
        annotation_file = row[2]
        check_file_exists("Annotation", fastq_file)
        samples.append( (sample_name, fastq_file, annotation_file) )
    if not samples:
        raise IOError("empty sample file") 
    return samples


def parse_annotation(annotation_file_handle):
    """ parses file with annotation for each read.

    Tab-delimeted file format is: read_identifier isHuman
    where read_identifier coresponds to identifier from corresponding fastq
    and isHuman = Y|N

    Returns:
        list of tuples, each tuple has read identifier and human 
        annotation(Y for human, N for nonhuman). 

        Number of elements of the list equal to number of annotated reads.
   
    Raises:
         IOError if cannot parse file 
    """
    read_annotation = []
    reader = csv.reader(annotation_file_handle, delimiter="\t")
    human_column_valid_values = ["Y", "N"]
    for row in reader:
        if len(row) != 2:
            raise IOError("annotation file should have 2 columns: read_id and (Y if read is human, N otherwise).")
        read_id = row[0]
        is_human = row[1]
        if not is_human in human_column_valid_values:
            raise IOError("2nd column should be equal to 'Y' or 'N'.")
        read_annotation.append( (read_id, is_human) )
    if not read_annotation:
        raise IOError("empty annotation file")
    return read_annotation

def parse_read_ids(fastq_file_handle):
    """ for a given fastq find all identifiers.
    
    Returns:
        set of ids.
    """
    raise NotImplementedError("parse_read_ids")

   
 