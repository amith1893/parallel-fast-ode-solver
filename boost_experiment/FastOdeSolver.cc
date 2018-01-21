#include <boost/python/module.hpp>
#include <boost/python.hpp>
#include <boost/python/def.hpp>
#include <vector>
#include <string>
#include <iostream>
#include "FastOdeSolver.h"

void populateParamState (boost::python::list param_combs, boost::python::int num_params)
{
	std::cout << "Uhhffff....Reached here" << std::endl;
}

void OdeSolve(boost::python::list param_combs, boost::python::int num_params)
{
	/*
	 * Define a vector of structures
	 * Populate each structure at a time 
	 * Once populated, keep adding it to the vector 
	 * Iterate through the vector and check if it has been populated correctly
	 */

	populateParamState(params_combs, num_params);

#if 0
	for (int i = 0; i < len(num_list); i++)
	{
		int x = boost::python::extract<int>(num_list[i][0]);
		int x = boost::python::extract<int>(num_list[i][1]);
		int x = boost::python::extract<int>(num_list[i][2]);
		int x = boost::python::extract<int>(num_list[i][0]);
		int x = boost::python::extract<int>(num_list[i][0]);
		std::cout << "First param "	<< x << std::endl;
	}
#endif

}

BOOST_PYTHON_MODULE(ode_solver)
{
	using namespace boost::python;
	def("OdeSolve", OdeSolve);
}
