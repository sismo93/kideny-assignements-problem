## kideny-assignements-problem
The preferred treatment for kidney failure is transplantation. However, the demand for donor kidneys
is far greater than the supply. Successful transplantation of a kidney relies on tissue-type compatibility
between the donor organ and patient, among other factors. Compatibility is determined through a tissuetype crossmatch between a potential donor and patient’s blood; if the two types differ substantially, the
patient’s body will reject the donor organ.
Typically, the donor organs come from deceased patients or from patients’ close relatives. Complementing
deceased donation is kidney exchange, which allows patients with a willing but medically incompatible living
donor to swap their donor with other patients. If the success rate of each transplant is high, both patients
are able to receive a viable transplant via the other patient’s donor. Notice that even if both pairs were
compatible, it can be sometimes possible to get more efficient transplants by exchanging donors. The process
is of course generalizable to more than two pairs, forming cycles of compatible transplants.
In this project, we solve the kidney assignment problem via Integer Programming techniques, in the aim
of maximizing the success rate of the transplantations overall.

## Model
Consider n patient-donor pairs (pi
, di), and define cij as the compatibility of donor di with patient pj . For
any i ∈ {1, ..., n}, let p(i) be the set of indices j ∈ {1, ..., n} such that pj is compatible with di
. Let us
consider the oriented network G = (V, A) where
• each node is either a patient or a donor.
• For each donor di
, there is an arc (di
, pj ), for each j ∈ p(i), i.e., from a donor to all its compatible
patients. The cost associated to this arc is wdi,pj = cij .
• For each patient-donor pair (pi
, di), there is an arc (pi
, di). The cost associated to this arc is wpi,di = 0.
Consider for example n = 6 pairs with the compatibilities in Table 1. We obtain the network depicted in
  
 d\p | p1 | p2 | p3 | p4|  p5|  p6
---- |----|----|----|---|----|-------  
d1   |0.5 |0.6 |    |   |    |
d2   |0.8 |0.4 |    |   |    |
d3   |    |    |    |0.4|    |
d4   |    |    |0.5 |   |0.5 |
d5   |    |    |0.7 |   |    |
d6   |    |    |    |   |0.9 |0.8

example of kidney exchange assignment is : d1 gives to p2, d2 gives to p1, d5
gives to p3, d3 gives to p4, d4 gives to p5 and d6 gives to p6.
Seeing the compatibilities cij as probabilities of successful surgery, our problem is to find an assignment
maximizing the number of transplants in expected value.

## Instance Structure

file 
    Small.csv,Normal.csv,Large.csv
    
First line is of the form

    n;m;M

where
    n is the number of patient-donor pairs (p_i, d_i),
    m is the  number of compatibilities (d_i, p_j),
    M is the maximum number of exchanges per cycle of transplants.

The remaining lines indicate the compatibility matrix and are of the form

    i;j;c

where
    i is the index of the donor d_i,
    j is the index of the patient p_j,
    c is the compatibility corresponding to the exchange (d_i, p_j).

NB: All indices start at 0.


## algorithmes positive cycle eliminations


We now see an ad hodc algorithm to solve our problem that does not need any solver. Given a feasible
solution x, let us define the residual network G(x) := (V, F(x) ∪ B(x))). We define
• the set of forward arcs F(x) := {(u, v) ∈ A : xuv = 0}, which contains the arcs in A that are not selected
in the the feasible solution x, and
• the set of backward arcs B(x) := {(v, u) : (u, v) ∈ A, xuv = 1}, which contains the reverse arcs of those
selected in x.
Furthermore, we define their cost by
w¯uv =
{
wuv, if (u, v) ∈ F(x),
−wvu, if (u, v) ∈ B(x).
It is possible to show that there is a cycle C in the residual network G(x) having a strictly positive cost
w¯(C) = ∑
e∈C∩(F (x)∪B(x))
w¯e,
2
if and only if x is not optimal. More precisely, for any positive cost cycle C w.r.t. w¯ in G(x), and defining
xuv(C) :=

0, if (u, v) ∈/ C and (v, u) ∈/ C,
1, if (u, v) ∈ C,
−1, if (v, u) ∈ C,
it is possible to prove that x + x(C) is still feasible (within bounds [0, 1] and satisfying the flow conservation)
and has a strictly better objective value than x. This means that we can iteratively find positive cost cycles
in the residual graph and update x ← x + x(C) until no positive cost cycle can be found in the residual
graph.
Implement the algorithm and check that the values match with the results obtained in the previous
section.
