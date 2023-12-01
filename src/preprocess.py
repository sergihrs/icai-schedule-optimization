import json

subject_name_json = json.load(open("data/subject-name.json", "r", encoding="utf-8"))
subject_hours_json = json.load(open("data/subject-hours.json", "r", encoding="utf-8"))
group_availability_json = json.load(
    open("data/group_availability.json", "r", encoding="utf-8")
)
teacher_specialty_json = json.load(
    open("data/teacher_specialty.json", "r", encoding="utf-8")
)
teacher_per_subject_json = json.load(
    open("data/teachers_per_subject.json", "r", encoding="utf-8")
)
teacher_availability_json = json.load(
    open("data/teacher_availability.json", "r", encoding="utf-8")
)
Qcgs_json = json.load(open("data/Qcgs.json", "r", encoding="utf-8"))
Lc_json = json.load(open("data/Lc.json", "r", encoding="utf-8"))

# Sets
G = {"IMAT-1A", "IMAT-1B", "IMAT-2A", "IMAT-2B", "IMAT-3A"}
D = {"1", "2", "3", "4", "5"}
H = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
S = set(subject_name_json.keys())
T = set(teacher_availability_json.keys())

C = set(Lc_json.keys())

# Print set differences
assert T == set(teacher_specialty_json.keys())
assert set(teacher_per_subject_json.keys()) == S

# Parameters
HS = subject_hours_json.copy()  # H[s] = hours of subject s
# print("HS", HS["DTC-IMAT-213"])

assert all(HS[s] > 0 for s in S)

A = {}
for g in G:
    A[g] = {}
    for h in H:
        A[g][h] = group_availability_json[g][int(h) - 1]
# print("A", A["IMAT-1A"]["5"])

assert all(A[g][h] in {0, 1} for g in G for h in H)

TS = {}  # TS[t][s] = 1 if teacher t is specialist in subject s, 0 otherwise
for s in S:
    TS[s] = {}
    for t in T:
        if s in teacher_specialty_json[t]:
            TS[s][t] = 1
        else:
            TS[s][t] = 0
# print("TS", TS["DOI-IMAT-314"]["PabloDuenasMartinez"])

assert all(TS[s][t] in {0, 1} for t in T for s in S)

TN = {}  # TN[g][s] = k number of teachers needed for subject s in group g
for g in G:
    TN[g] = {}
    for s in S:
        TN[g][s] = teacher_per_subject_json[s][g]
# print("TN", TN["IMAT-3A"]["DOI-IMAT-314"])

assert all(TN[g][s] >= 0 for g in G for s in S)

Q = {}  # Qcgs[c][g][s] = k number of classrooms c group g needs for subject s
for c in C:
    Q[c] = {}
    for g in G:
        Q[c][g] = {}
        for s in S:
            if g in Qcgs_json[c] and s in Qcgs_json[c][g]:
                Q[c][g][s] = Qcgs_json[c][g][s]
            else:
                Q[c][g][s] = 0
# print("Q", Q["Lab-E"]["IMAT-1A"]["DOI-IMAT-314"])

assert all(Q[c][g][s] >= 0 for c in C for g in G for s in S)

L = Lc_json.copy()  # Lc[c] = k number of available classrooms for class c
# print("Lc", Lc["Lab-E"])

assert all(L[c] >= 0 for c in C)

TA = {}  # TA[d][h][t] = 1 if teacher t is available at day d and hour h, 0 otherwise
TP = (
    {}
)  # TP[d][h][t] = 1 if teacher t DOESNT want to teach at day d and hour h, 0 otherwise
for d in D:
    TA[d] = {}
    TP[d] = {}
    for h in H:
        TA[d][h] = {}
        TP[d][h] = {}
        for t in T:
            if int(h) in teacher_availability_json[t]["Av"][d]:
                TA[d][h][t] = 0
            else:
                TA[d][h][t] = 1

            if int(h) in teacher_availability_json[t]["Pr"][d]:
                TP[d][h][t] = 1
            else:
                TP[d][h][t] = 0
# print("TA", TA["1"]["3"]["EugenioFranciscoSanchezUbeda"])
# print("TP", TP["1"]["3"]["EugenioFranciscoSanchezUbeda"])

assert all(TA[d][h][t] in {0, 1} for d in D for h in H for t in T)
