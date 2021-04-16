import time
from threading import Thread
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv('matA.csv')
a = df.to_numpy()

df = pd.read_csv('matB.csv')
b = df.to_numpy().T

rowsA = len(a)
rowsB = len(b)

colsA = len(a[0])
colsB = len(b[0])

print('a: ', rowsA, 'x', colsA)
print('b: ', rowsB, 'x', colsB)

# pool size
pSize = 500

mat = []

threads = list()
start = time.perf_counter()

def mult(X, Y):
  mat.append(X@Y.T)

# # crear threads
def createThread(poolSize):
  for i in range(rowsA): # fila master
      for j in range(colsB): # columna slave
        x = Thread(target=mult, args=(a[int(rowsA/poolSize*i),:], b[:,int(colsB/poolSize*j)]))
        threads.append(x)
        x.start()
  
  # hacer join
  for index, thread in enumerate(threads):
    thread.join()

with ThreadPoolExecutor(max_workers=pSize) as ex:
  ex.submit(createThread, rowsA)

matC = np.array(mat).reshape(rowsA, colsB)
# print(matC)

np.savetxt('matC.csv', matC, fmt='%4.0f', delimiter=',')

end = time.perf_counter()
print(f"Time taken: {round(end - start, 5)} seconds(s)")