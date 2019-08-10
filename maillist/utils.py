from __future__ import print_function, unicode_literals

############################################################################


def extract_email_from_line(line):
    """
    Extract an email address from a line of text; can be in the forms:
    address@example.com, Name <a@e.c>, or a@e.c (Name)
    """
    line = line.strip()

    # strip any trailing punctuation.
    for punc in [".", ",", ";"]:
        while line.endswith(punc):
            line = line[:-1]

    if "<" in line:
        # Name <a@e.c>
        p = line.find("<") + 1
        p2 = line.find(">")  # might be -1, not found
        if p2 == -1:
            line = line[p:]
        else:
            line = line[p:p2]

    if "(" in line:
        # a@e.c (Name) form
        p = line.find("(")
        p2 = line.find(")")  # might be -1, not found
        if p2 != -1:  # fall to the next case if this happens
            p2 += 1
            line = line[:p] + line[p2:]

    # base case: a@e.c garbage
    parts = line.split()
    if len(parts):
        return parts[0].lower()


############################################################################


def get_bulk_add_email_addresses(text):
    """
    Extracts email addresses from a block of text, one per line.
    """
    results = set()
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        email = extract_email_from_line(line)
        if email is not None:
            results.add(email)
        elif line:
            print("No email address in line {0!r}".format(line))
    return results


############################################################################
