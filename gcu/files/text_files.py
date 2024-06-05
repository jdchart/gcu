import csv
from numpy import genfromtxt

def read_plain_text(path):
    """Return plain text file as string."""

    with open(path, 'r') as f:
        return f.read()

def read_csv(path, **kwargs):
    """Return csv file as multi dimensional list."""

    if kwargs.get("return_type", "list") == "list":
        content = []
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter = kwargs.get("delimiter", ","), quotechar = kwargs.get("quotechar", '"'))
            for row in csv_reader:
                content.append(row)
        return content
    elif kwargs.get("return_type", "list") == "np":
        return genfromtxt(path, delimiter = kwargs.get("delimiter", ","))