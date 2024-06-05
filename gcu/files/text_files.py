import csv

def read_plain_text(path):
    """Return plain text file as string."""

    with open(path, 'r') as f:
        return f.read()

def read_csv(path, **kwargs):
    """Return csv file as multi dimensional list."""

    content = []
    with open(path, 'r') as f:
        csv_reader = csv.reader(f, delimiter = kwargs.get("delimiter", ","), quotechar = kwargs.get("quotechar", '"'))
        for row in csv_reader:
            content.append(row)
    return content