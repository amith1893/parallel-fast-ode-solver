#include <stdio.h>
#include <omp.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>


#define NOW()(omp_get_wtime())
typedef double mytime_t;

int main(int argc, char *argv[])
{
	int a[] = {4,3,2,1,7,8,9,10,0,-1};
	#pragma omp parallel
	{
		#pragma omp single
		{
			for(int i=0; i<10; i++)
			{
				#pragma omp task
				{
					printf("%d\n", i);
				}
			}
		}		
		
	}	

}
