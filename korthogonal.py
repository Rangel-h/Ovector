from itertools import combinations, product
import numpy as np
import math

def subsets(s, k): # Generates all the subssets of "s" of size "k"
    return list(combinations(s, k))

def support_basis(elements,r): # Create the support of all basis in reverse lexicographic order
    elements1 = list(elements)
    elements1.reverse()
    SB = []
    SB1 = subsets(elements1, r)
    for B1 in SB1:
        B2 = list(B1)
        B2.reverse()
        SB.append(B2)
    SB.reverse()
    return SB

def support_circuits(elements,r): # Create the support of all circuits
    SC1 = subsets(elements, r + 1)
    SC = []
    for C1 in SC1:
        SC.append(list(C1))
    return SC


def create_circuits(Chirotope,elements,r,SB, SC):
    Circuits = []  # this list will store the oriented circuits

    # In this part we obtain the signature of all circuits and then they are added to Circuits
    Circuits1 = []
    for C in SC:
        SBC1 = subsets(C, r)# Generate the support off all basis contained in circuit A
        SBC =[]
        for x in SBC1:
            SBC.append(list(x))
        # print("Basis contained in circuit A", C, SBC)
        # This will be the oriented circuit whose support is A, we suppose that the first entry is positive
        Oriented_C = [1]
        for i in range(1, r + 1):
            # This will store the chirotope of two bases that appear in the formula, the position of the
            # elements and the sign of the previous element in the circuit
            Dif_sim = [Oriented_C[i - 1]]
            for B1 in SBC:
                if C[i - 1] in B1 and C[i] not in B1:
                    # this add to Dif_sim the position of element i-1 in B1
                    Dif_sim.append(B1.index(C[i - 1]) + 1)
                    # this add to Dif_sim the sign of B_1 in the Chirotope
                    Dif_sim.append(Chirotope[SB.index(B1)])
                    break
                else:
                    continue
            for B2 in SBC:
                if C[i - 1] not in B2 and C[i] in B2:
                    # this add to Dif_sim the position of element i-1 in B2
                    Dif_sim.append(B2.index(C[i]) + 1)
                    # this add to Dif_sim the sign of B_2 in the Chirotope
                    Dif_sim.append(Chirotope[SB.index(B2)])
                    break
                else:
                    continue
            # Formula to obtain signature of circuits
            Oriented_C.append(((-1) ** (1 + Dif_sim[1] + Dif_sim[3])) * (Dif_sim[0]) * (Dif_sim[2]) * (Dif_sim[4]))
        Circuits1.append(Oriented_C)  # List of circuits without 0
    counter = 0
    for k in Circuits1:
        X = []  # This will be the Circuit with 0
        for i in range(len(elements)):
            if i in SC[counter]:
                X.append(k[SC[counter].index(i)])
            else:
                X.append(0)
        Circuits.append(X)
        counter += 1
    return Circuits

def Ovector_matroid(r, n, Circuits):
    # --------------------------- Create Topes
    T = list(product([1, -1], repeat=n))  # List of tuplas
    Topes = list(map(list, T))  # Convert Tuplas to lists

    # ---------------------------- Calculate orthogonality of every Tope
    Ort = []  # This will store the Orthogonality of every tope
    for i in Topes:
        P = []  # This list will store the product i * j
        for j in Circuits:  # Multiplication of tope i and circuit j
            p = np.multiply(i, j)
            P.append(p)
        Ortk = []  # This list will store Ort(k) for any k in P
        for k in P:
            H = 0  # Cardinality of equalizer of k
            S = 0  # Cardinality of separator of k
            for l in range(len(k)):
                A = k[l]
                if (A == 1):
                    H += 1
                elif (A == -1):
                    S += 1
                else:
                    pass
            Ortk.append(min(H, S))
        Ort.append(min(Ortk))

    # ------------------------------------------- Create O- vector
    Ovector = []  # O-vector of the matroid
    #
    for j in range(1, math.floor((r+1)/2)+1):
    #for j in range(1, max(Ort) + 1):
        Ovector.append(Ort.count(j))

    #print("O(C_{}({})) =".format(r, n), Ovector)
    return Ovector

def convert_chirotope(line): #Convert each chirotope in a (1,-1)-list
    Chirotope = []
    for i in line:
        if i == "+":
            Chirotope.append(1)
        if i == "-":
            Chirotope.append(-1)
        else:
            pass
    return Chirotope