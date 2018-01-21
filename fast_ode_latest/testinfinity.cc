#include <stdio.h>
#include <iostream>
int main()
{
	int x = 100;
	int t=0;
	double s = 0;

	while(++t<1000)
	{
		s *= x*x;
	}
	std::cout << s << std::endl;
}
