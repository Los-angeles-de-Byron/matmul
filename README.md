# Matrix multiplication with Thread Pool

* [About the Project](#about-the-project)
  * [Understanding the process behind a thread-pool](#understanding-the-process-behind-a-thread-pool)
  * [Implementation](#implementation)
* [How it works](#how-it-works)
  * [Things to consider](#things-to-consider)
  * [The thread pool](#the-thread-pool)
  * [The multiplication](#the-multiplication)
  * [Storing our results](#storing-our-results)
* [Usage](#usage)
  * [Clone the repo](#clone-the-repo)
  * [Try it on Replit](#try-it-on-replit)
* [Sources](#sources)

## About the Project

1. Multiply 2 matrices using thread-pool, the program will receive 2 csv files as input that must be read and loaded into memory.
  <i>The matrix product must be burned to another file</i>
2. The size of the thread pool to be used will be given
3. Each matrix is composed of integers, the files do not have headers, the column separator is the character "," and each line indicates a new row

### Understanding the process behind a thread-pool
A thread pool is a group of pre-instantiated, idle threads which stand ready to be given work. These are preferred over instantiating new threads for each task when there is a large number of short tasks to be done rather than a small number of long ones. This prevents having to incur the overhead of creating a thread a large number of times.

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Thread_pool.svg/1200px-Thread_pool.svg.png)

When the thread pool is created, it will either instantiate a certain number of threads to make available or create new ones as needed depending on the needs of the implementation.

When the pool is handed a Task, it takes a thread from the container (or waits for one to become available if the container is empty), hands it a Task, and meets the barrier. This causes the idle thread to resume execution, invoking the execute() method of the Task it was given. Once execution is complete, the thread hands itself back to the pool to be put into the container for re-use and then meets its barrier, putting itself to sleep until the cycle repeats.

### Implementation
It will vary by environment, but in simplified terms, you need the following:

- A way to create threads and hold them in an idle state. This can be accomplished by having each thread wait at a barrier until the pool hands it work. 
- A container to store the created threads, such as a queue or any other structure that has a way to add a thread to the pool and pull one out.
- A standard interface or abstract class for the threads to use in doing work. This might be an abstract class called Task with an execute() method that does the work and then returns.

## How it works

### Things to consider

Before diving into our solution, we need to understand a basic concept when multipliying matrixes:

If <img src="https://latex.codecogs.com/svg.image?A"/> is an <img src="https://latex.codecogs.com/svg.image?m&space;\times&space;n"/> matrix <img src="https://latex.codecogs.com/svg.image?B"/> is an <img src="https://latex.codecogs.com/svg.image?n&space;\times&space;p"/> matrix,

<img src="https://latex.codecogs.com/svg.image?\begin{pmatrix}&space;a_{11}&space;&&space;a_{12}&space;&&space;\cdots&space;&space;&&space;a_{1n}&space;\\&space;a_{21}&space;&&space;a_{22}&space;&&space;\cdots&space;&space;&&space;a_{2n}&space;\\&space;\vdots&space;&space;&&space;\vdots&space;&space;&&space;\ddots&space;&space;&&space;\vdots&space;&space;\\&space;a_{m1}&space;&&space;a_{m2}&space;&&space;\cdots&space;&space;&&space;a_{nm}&space;\\\end{pmatrix}" title="\begin{pmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{nm} \\\end{pmatrix}" />
,
<img src="https://latex.codecogs.com/svg.image?\begin{pmatrix}&space;b_{11}&space;&&space;b_{12}&space;&&space;\cdots&space;&space;&&space;b_{1p}&space;\\&space;b_{21}&space;&&space;b_{22}&space;&&space;\cdots&space;&space;&&space;b_{2p}&space;\\&space;\vdots&space;&space;&&space;\vdots&space;&space;&&space;\ddots&space;&space;&&space;\vdots&space;&space;\\&space;b_{m1}&space;&&space;b_{m2}&space;&&space;\cdots&space;&space;&&space;b_{np}&space;\\\end{pmatrix}" title="\begin{pmatrix} b_{11} & b_{12} & \cdots & b_{1p} \\ b_{21} & b_{22} & \cdots & b_{2p} \\ \vdots & \vdots & \ddots & \vdots \\ b_{m1} & b_{m2} & \cdots & b_{np} \\\end{pmatrix}" />

the matrix product <img src="https://latex.codecogs.com/svg.image?&space;C&space;=&space;AB" title=" C = AB" /> is defined to be the <img src="https://latex.codecogs.com/svg.image?m&space;\times&space;p"/> matrix

<img src="https://latex.codecogs.com/svg.image?C&space;=&space;\begin{pmatrix}c_{11}&space;&&space;c_{12}&space;&&space;\cdots&space;&space;&&space;c_{1p}&space;\\c_{21}&space;&&space;c_{22}&space;&&space;\cdots&space;&&space;c_{2p}&space;\\\vdots&space;&&space;\vdots&space;&&space;\ddots&space;&space;&&space;\vdots&space;\\c_{m1}&space;&&space;c_{m2}&space;&&space;\cdots&space;&&space;c_{mp}&space;\\\end{pmatrix}" title="C = \begin{pmatrix}c_{11} & c_{12} & \cdots & c_{1p} \\c_{21} & c_{22} & \cdots & c_{2p} \\\vdots & \vdots & \ddots & \vdots \\c_{m1} & c_{m2} & \cdots & c_{mp} \\\end{pmatrix}" />

such that

<img src="https://latex.codecogs.com/svg.image?c_{ij}&space;=&space;a_{i1}b_{1j}&space;&plus;&space;a_{i2}b_{2j}&space;&plus;&space;\cdots&space;&plus;&space;a_{in}b_{nj}&space;=&space;\sum_{k=1}^{n}a_{ik}b_{kj}" title="c_{ij} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{in}b_{nj} = \sum_{k=1}^{n}a_{ik}b_{kj}" />

for <img src="https://latex.codecogs.com/svg.image?i=1,&space;\cdots&space;,&space;m&space;" title="i=1, \cdots , m " /> and <img src="https://latex.codecogs.com/svg.image?j=1,&space;\cdots&space;,&space;p" title="j=1, \cdots , p" />

### The thread pool

```py
  with ThreadPoolExecutor(max_workers=pSize) as ex:
    ex.map(mult, a)
```

Basically, ThreadPoolExecutor was introduced in Python in concurrent.futures module to efficiently manage and create threads.
The pool keeps track and manages the threads lifecycle and schedules them on the programmer's behalf thus making the code much simpler and less buggy.

The argument we are using (<i>max_workers</i>) it's the number of threads aka size of pool.
The method we are using (<i>map(fn, *iterables, timeout = None, chunksize = 1)</i>) maps the method and iterables together immediately and will raise an exception concurrent. futures.TimeoutError if it fails to do so within the timeout limit. If the iterables are very large, then having a chunk-size larger than 1 can improve performance when using ProcessPoolExecutor but with ThreadPoolExecutor it has no such advantage, ie it can be left to its default value.

No matter the dimensions of your matrix, this functionality will manage to deliver the complete job.
As you can appreciate, the <i>map</i> method will receive the multiplication function and it will send the matrix <img src="https://latex.codecogs.com/svg.image?A"/> as well. It should be noted that the function will be reading the rows of matrix <img src="https://latex.codecogs.com/svg.image?A"/>.

### The multiplication

```py
  def mult(filaX):
    for i in range(colsB):
      mat.append(filaX@b[:,i])
```

As we mentioned earlier, this function receives matrix <img src="https://latex.codecogs.com/svg.image?A"/> rows (one row every time is being called) and it performs dot product with every column in matrix <img src="https://latex.codecogs.com/svg.image?B"/> in a very pythonic way

### Storing our results

```py
  matC = np.array(mat).reshape(rowsA, colsB)
```

Our answers of the dot product between rows and columns are stored in <i>mat</i> list and then, leveraging python capabilities, we reshape the list into a numpy array to display the results in a csv

## Usage

### Clone the repo

1. Clone the repo in your computer

```sh
  git clone https://github.com/Los-angeles-de-Byron/custom_syscall.git
```

2. Try the program with the following command

```sh
python matmul.py matA.csv matB.csv <threadpool_size>* <output_file>
```

<i>*it should be an int value</i>

### Try it on Replit

1. Click [here](https://replit.com/join/wukqkevc-lindsm) to open the project in replit

2. Before trying to insert the command click on the "Run" button to install necessary libraries. Don't worry if you see an error in the <i>Console</i> tab.

3. Change to the **Shell** tab and write the following command:

```sh
 python main.py matA.csv matB.csv <threadpool_size>* <output_file>
```

<i>*it should be an int value</i>

4. And there you go! The display must be the dimensions of each matrix and the elapsed time of the operation. You can go check your <output_file> to see the answer of the multiplication.

## Sources

* [Matrix multiplication fundamentals](https://en.wikipedia.org/wiki/Matrix_multiplication)
* [Threadpoolexecutor in python](https://www.geeksforgeeks.org/how-to-use-threadpoolexecutor-in-python3/)
