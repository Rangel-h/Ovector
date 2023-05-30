# Given a data basis (in "txt" format) of chirotopes of uniform oriented matroids,
# this program computes their O-vector.
from korthogonal import support_basis, support_circuits, create_circuits, convert_chirotope, Ovector_matroid

r = 5   # rank of the matroid
n = 8   # number of elements of the matroid

elements = list(range(n))   # Create ground set
SB = support_basis(elements, r)   # Create the support of all basis in reverse lexicographic order
SC = support_circuits(elements, r)  # Create the support of all circuits

counter = 0
file = open("O-vector.txt", "w")   # The O-vectors will be saved in this file.
with open("OM85_nondeg.txt") as archive:   # Open the database
    for line in archive:
        counter += 1
        Chirotope = convert_chirotope(line)   # Convert each chirotope in a (1,-1)-list
        Circuits = create_circuits(Chirotope, elements, r, SB, SC)   # Create all oriented circuits
        X = Ovector_matroid(r, n, Circuits)   # Calculate the O-vector of the matroid
        file.write("{}\n".format(X))   # Save the O-vector of the matroid in a file
        print("class {} O-vector =".format(counter), X)   # print O-vector

archive.close()
file.close()