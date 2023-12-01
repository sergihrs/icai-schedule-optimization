import json
import pyomo.environ as pyo
from preprocess import G, D, H, S, T, C
from preprocess import HS, A, TA, TN, TP, TS, Q, L
from pyomo.opt import SolverFactory
from time import perf_counter

# MODEL
model = pyo.ConcreteModel(name="ICAI Scheduling Problem")
start_time = perf_counter()

# SETS
model.g = pyo.Set(initialize=list(G))
model.d = pyo.Set(initialize=list(D))
model.h = pyo.Set(initialize=list(H))
model.s = pyo.Set(initialize=list(S))
model.t = pyo.Set(initialize=list(T))
model.c = pyo.Set(initialize=list(C))

# PARAMETERS
model.HS = pyo.Param(model.s, initialize=lambda _, s: HS[s])
model.A = pyo.Param(model.g, model.h, initialize=lambda _, g, h: A[g][h])
model.TA = pyo.Param(
    model.d, model.h, model.t, initialize=lambda _, d, h, t: TA[d][h][t]
)
model.TN = pyo.Param(model.g, model.s, initialize=lambda _, g, s: TN[g][s])
model.TP = pyo.Param(
    model.d, model.h, model.t, initialize=lambda _, d, h, t: TP[d][h][t]
)
model.TS = pyo.Param(model.s, model.t, initialize=lambda _, s, t: TS[s][t])
model.Q = pyo.Param(model.c, model.g, model.s, initialize=lambda _, c, g, s: Q[c][g][s])
model.L = pyo.Param(model.c, initialize=lambda _, c: L[c])


# VARIABLES
model.x = pyo.Var(model.g, model.d, model.h, model.s, model.t, domain=pyo.Binary)

model.g1 = pyo.Var(model.g, model.d, model.h, model.s, domain=pyo.Binary)

model.s1 = pyo.Var(model.g, model.s, model.t, domain=pyo.Binary)

model.d1 = pyo.Var(model.g, model.d, model.h, model.s, domain=pyo.Binary)
model.d2 = pyo.Var(model.g, model.d, model.h, model.s, domain=pyo.Binary)


# HARD CONSTRAINTS
def ctc(m, g, d, h, s):
    return sum(m.x[g, d, h, s, t] for t in m.t) == m.TN[g, s] * m.g1[g, d, h, s]


model.ctc = pyo.Constraint(model.g, model.d, model.h, model.s, rule=ctc)


def nsd_eoo(m, g, d, h):
    return (
        sum(m.x[g, d, h, s, t] / m.TN[g, s] for s in m.s for t in m.t if m.TN[g, s] > 0)
        == m.A[g, h]
    )


model.nsd_eoo = pyo.Constraint(model.g, model.d, model.h, rule=nsd_eoo)


def shr_t2s_cta(m, g, s):
    return (
        sum(
            m.x[g, d, h, s, t] * m.TS[s, t] * m.TA[d, h, t]
            for d in m.d
            for h in m.h
            for t in m.t
        )
        == m.HS[s] * m.TN[g, s]
    )


model.shr_t2s_cta = pyo.Constraint(model.g, model.s, rule=shr_t2s_cta)


def ntc(m, d, h, t):
    return sum(m.x[g, d, h, s, t] for g in m.g for s in m.s) <= 1


model.ntc = pyo.Constraint(model.d, model.h, model.t, rule=ntc)


def tcp(m, g, s, t):
    return (
        sum(m.x[g, d, h, s, t] for d in m.d for h in m.h) == m.HS[s] * model.s1[g, s, t]
    )


model.tcp = pyo.Constraint(model.g, model.s, model.t, rule=tcp)


def nco(m, d, h, c):
    return (
        sum(
            m.x[g, d, h, s, t] * m.Q[c, g, s] / m.TN[g, s]
            for g in m.g
            for s in m.s
            for c in m.c
            for t in m.t
            if m.TN[g, s] > 0
        )
        <= m.L[c]
    )


model.nco = pyo.Constraint(model.d, model.h, model.c, rule=nco)


def nsa(m, g, d, s):
    return sum(m.x[g, d, h, s, t] for h in m.h for t in m.t) <= 2 * m.TN[g, s]


model.nsa = pyo.Constraint(model.g, model.d, model.s, rule=nsa)


def nhs1(m, g, d, s, h):
    if h == str(len(m.h)):
        return pyo.Constraint.Skip
    return (
        sum(m.x[g, d, str(int(h) + 1), s, t] - m.x[g, d, h, s, t] for t in m.t)
        <= m.d1[g, d, h, s] * m.TN[g, s]
    )


model.nhs1 = pyo.Constraint(model.g, model.d, model.s, model.h, rule=nhs1)


def nhs2(m, g, d, s, h):
    if h == str(len(m.h)):
        return pyo.Constraint.Skip
    return (
        sum(m.x[g, d, str(int(h) + 1), s, t] - m.x[g, d, h, s, t] for t in m.t)
        >= -m.d2[g, d, h, s] * m.TN[g, s]
    )


model.nhs2 = pyo.Constraint(model.g, model.d, model.s, model.h, rule=nhs2)


def nhs3(m, g, d, s):
    return sum(m.d1[g, d, h, s] + m.d2[g, d, h, s] for h in m.h) <= 2


model.nhs3 = pyo.Constraint(model.g, model.d, model.s, rule=nhs3)

# OBJECTIVE FUNCTION
model.obj = pyo.Objective(
    expr=sum(
        model.x[g, d, h, s, t] * model.TP[d, h, t]
        for g in model.g
        for d in model.d
        for h in model.h
        for s in model.s
        for t in model.t
    ),
    sense=pyo.minimize,
)

print(f"Model created in {perf_counter() - start_time:.2f} seconds")
print(f"Number of variables: {len(model.x)}")
print(f"Number of constraints: {len(model.component_map(pyo.Constraint))}")
print(f"-" * 50)

# SOLVE
opt = SolverFactory("gurobi")
start_time = perf_counter()
result_obj = opt.solve(model, tee=True)
print(f"Model solved in {perf_counter() - start_time:.2f} seconds")
print(result_obj)

solution_dict = model.x.get_values()
with open("./schedules.json", "w", encoding="utf-8") as outfile:
    json_dict = dict()
    for tuple_key, value in solution_dict.items():
        if value == 1.0:
            json_dict[str(tuple_key)] = value
    json.dump(json_dict, outfile)
