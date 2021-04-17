# libraries
import time
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import sys
import argparse

# read user args
ap = argparse.ArgumentParser()

# build matrix a
mata=sys.argv[1]
df = pd.read_csv(mata)
a = df.to_numpy()

# build matrix b
matb=sys.argv[2]
df = pd.read_csv(matb)
b = df.to_numpy().T

# take dimensions
rowsA, colsA = a.shape
rowsB, colsB = b.shape

print('a: ', rowsA, 'x', colsA, '\nb: ', rowsB, 'x', colsB)

# check if dimensions are compatible
if colsA != rowsB:
  print('Non multiplicable dimensions')
  quit()

pSize = int(sys.argv[3])

# list to collect matrix multiplication results
mat = []

# time starts
start = time.perf_counter()

# multiply row vs cols
def mult(filaX):
  for i in range(colsB): # columnas
    mat.append(filaX@b[:,i])

# manage thread pool and trigger multiplication
with ThreadPoolExecutor(max_workers=pSize) as ex:
  ex.map(mult, a)

# build matrix with collected results
matC = np.array(mat).reshape(rowsA, colsB)

# put the matrix into csv
matc=sys.argv[4]
np.savetxt(matc, matC, fmt='%4.0f', delimiter=',')

# stop time
end = time.perf_counter()

print(f"Time taken: {round(end - start, 5)} seconds(s)")