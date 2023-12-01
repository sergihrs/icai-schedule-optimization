# Mathematical Formulation

### Sets

g: groups {"IMAT-1A", "IMAT-1B", ...}
d: days {1, ..., 5}
h: hours {1, ..., 10}
s: subjects {"DMA-IMAT-101", "DMA-IMAT-102", ...}
t: teachers {"EugenioFranciscoSanchezUbeda", ...}

c: class {Lab-E, Lab-R, ...}


### Parameters

$\text{HS}_{s} \in \mathbb{N}$ = hours of subject s per week to fulfill the curriculum
$\text{A}_{gh} \in \{0,1\}$ = availability of group g in hour h
$\text{TA}_{dht} \in \{0,1\}$ = whether a teacher t is available in hour h of day d
$\text{TN}_{gs} \in \mathbb{N}_0$ = number of teachers needed per group g and subject s
$\text{TP}_{dht} \in \{0,1\}$ = whether a teacher t prefers NOT to teach in hour h of day d
$\text{TS}_{st} \in \{0,1\}$ = whether subject s can be taught by teacher t
$\text{Q}_{cgs} \in \mathbb{N}_0$ = number of classrooms of type c that a group g needs for a subject s
$\text{L}_{c} \in \mathbb{N}_0$ = number of available classrooms of type c

### Variables

x$_{gdhst}$ = whether teacher t teaches subject s to group g in hour h of day d

$\gamma_{gdhs}$ = auxiliary variable for constraint CTC
$\zeta_{gst}$ = auxiliary variable for constraint TCP
$\delta'_{gdhs}$ = auxiliary variable for constraint NHS
$\delta''_{gdhs}$ = auxiliary variable for constraint NHS

### Hard constraints

1. Assure that exactly one subject is assigned to each group in each hour of its schedule (morning or afternoon), and with the exact number of teachers needed for that subject:

    - CTC (complete teacher capacity):
$\sum_{t} x = \text{TN}_{gs} \cdot \gamma_{gdhs} \quad \forall g,d,h,s$

    - NSD & EOO (non-subject duplication  and early or overnight):
$\sum_{s,t} x \cdot \frac{1}{\text{TN}_{gs}} = \text{A}_{gh} \quad \forall g,d,h$

2. Assure that each group gets the exact number of hours of each subject and that each teacher only teaches subjects of his speciality when he is available:

    - SHR & T2S & CTA (subject hours requirement, teacher to speciality and checking teacher availability):
$\sum_{d,h,t} x \cdot \text{TS}_{st} \cdot \text{TA}_{tdh} = \text{HS}_{s} \cdot \text{TN}_{gs} \quad \forall g,s$

3. Assure that a teacher does not clone himself:

    - NTC (no teacher clonation):
$\sum_{g,s} x \leq 1 \quad \forall d,h,t$

4. Assure that each subject is always taught by the same teacher:

    - TCP (teacher consistency principle):
$\sum_{d,h} x = \text{HS}_{s} \cdot \zeta_{gst} \quad \forall g,s,t$

5. Assure that there are enough classrooms of each type at each time slot:

    - NCO (no class overflow):
$\sum_{g,s,t} x \cdot \frac{\text{Q}_{cgs}}{\text{TN}_{gs}} \leq \text{L}_{c} \quad \forall c,d,h$

6. Assure that a subject is given maximum two hours per day:

    - NSA (no subject abuse):
$\sum_{h,t} x \leq 2 \cdot \text{TN}_{gs} \quad \forall g,d,s$

7. Assure that all subjects are given in consecutive hours in a day:

    - NHS (no holes in subject):
$\sum_{t} x_{h+1} - \sum_{t} x_{h} \leq \delta'_{gdhs} \cdot \text{TN}_{gs} \quad \forall g,d,h \lt 10,s$
$\sum_{t} x_{h+1} - \sum_{t} x_{h} \geq -\delta''_{gdhs} \cdot \text{TN}_{gs} \quad \forall g,d,h \lt 10,s$
$\sum_{h}\delta'_{gdhs} + \delta''_{gdhs} \leq 2  \quad \forall g,d,s$


### Objective Function (Soft Constraints)

- CTP (checking teacher preference):
$$min_x \sum_{g,d,h,s,t} x_{gdhst} \cdot \text{TP}_{dht}$$