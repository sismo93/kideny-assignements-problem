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
is - of course - generalizable to more than two pairs, forming cycles of compatible transplants.
In this project, we solve the kidney assignment problem via Integer Programming techniques, in the aim
of maximizing the success rate of the transplantations overall.

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
