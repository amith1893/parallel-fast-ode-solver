#include <omp.h>
#include <stdio.h>



void increment(int *i)
{
	if (*i == 10)
	{
		return;
	}
	else
	{
		*i += 1;	
		#pragma omp task
		increment(i);
	}

}

void increment_helper(int a[])
{
	int i;
	for(i=0;i<10;i++)
	{
		#pragma omp task
		increment(&a[i]);	
	}
}

int main()
{
	int a[10] = {0,1,2,3,4,5,6,7,8,9};

	#pragma omp parallel
	{
		#pragma omp single
		increment_helper(a);
	}

	int j;
	for(j=0;j<10;j++)
	{
		printf("%d\n", a[j]);
	}

}
