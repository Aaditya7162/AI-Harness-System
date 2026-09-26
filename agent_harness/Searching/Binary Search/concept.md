# ---- Concept ---- #
Max Array Size -- 10^6(locally)

Max Array Size -- 10^7(globally)
<br><br>1. Binary Search can only be applied to a sorted array

**<u>Example :</u>**

a= [5 6 10 12 15 20 30 45]<br>
   &emsp;&nbsp;&nbsp;[0&nbsp;1&nbsp;&nbsp;2 &nbsp; 3 &nbsp; 4&nbsp;&nbsp;  5 &nbsp; 6 &nbsp;&nbsp; 7] <--- Indexes
<br>&emsp;&emsp;i&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;j

i=0<br>
j=n-1;<br>
target(x)=30

# Steps
<br>1. Find mid of i and j mid=(i+j)/2
<br>2. mid value
a[mid] --> 12
if x>a[mid] so x cannot be lying on left side if array sorted in ascending order and vice versa
this leads to fact that left side is of no use<br><br>
3. change i=mid+1<br>
a= [5 6 10 12 15 20 30 45]<br>
   &emsp;&nbsp;&nbsp;[0 1&nbsp; 2 &nbsp; 3 &nbsp; 4 &nbsp; 5 &nbsp; 6 &nbsp; 7]<br>
&emsp;&nbsp;&nbsp;i0&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;j0<br>
&emsp;&nbsp;&nbsp;i0&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;i1<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;j1
<br>4. repeat steps 1 , 2 and 3 again
5. When last iteration is used then mid value is the answer