#include <boost/python/module.hpp>
#include <boost/python.hpp>
#include <boost/python/def.hpp>
#include <vector>
#include <string>
#include <iostream>
#include "FastOdeSolver.h"
#include <math.h>
#include <stdlib.h>
#include <omp.h>


#define NOW()(omp_get_wtime())
typedef double mytime_t;


#define INIT_ODE_VAL (-99999.0)

void populateParamState (global_vars *gvars, std::vector<param_state> *param_state_list, boost::python::list param_combs, boost::python::object num_params)
{
	int np = gvars->num_params;
	
	for (int i=0; i<len(param_combs); i++)
	{
		param_state ps;
		ps.params = (double *)malloc(sizeof(double)*np);
		int j = 0;
		for (;j<np; j++)
		{
			ps.params[j] = boost::python::extract<double>(param_combs[i][j]);
			
		}
		
		ps.step_size = boost::python::extract<double>(param_combs[i][j++]);
		ps.ode_value = boost::python::extract<double>(param_combs[i][j++]);
		ps.iter_value = boost::python::extract<int>(param_combs[i][j++]);
		ps.move_flag  = 0;
		param_state_list->push_back(ps);
	}

}

void populateGlobalState (global_vars *gvars, boost::python::object num_params, boost::python::object accuracy, boost::python::object num_iter, boost::python::object init_val, boost::python::object max_steps)
{
	gvars->num_params = boost::python::extract<int>(num_params);
	gvars->accuracy = boost::python::extract<double>(accuracy);
	gvars->num_iter = boost::python::extract<int>(num_iter);
	gvars->init_val = boost::python::extract<double>(init_val);
	gvars->max_steps = boost::python::extract<int>(max_steps);
}

double evaluate_differential_equation (double y, double t, std::vector<double> params)
{
	double new_y = (params[0] * t * y * y) - (params[1]/t) + (params[2]/t*t);
   	return new_y;	
}

void forwardEulerSolver (std::vector<double> params, double step, int iter_val, double initial_value, int num_iter, double &res)
{
	double y0 = initial_value;
	res = y0 * 1.0;
	double t = 0;
	int counter = 0;
	//std::cout << num_iter << std::endl;
	while (counter <= num_iter)
	{
		t += step;
		res += step * evaluate_differential_equation(res, t, params);
		counter += 1;	
	}

	//iter_val += 1;
	//step /= 2;
	
	//std::cout << "For params " << params[0] << "," << params[1] << "," << params[2] << " the result is " << res << std::endl;
}

int checkForAccuracy (double res, double prev_res, int iter_num, global_vars *gvars)
{
	
	//std::cout << iter_num << " " << gvars->num_iter << std::endl;
	if (iter_num >= gvars->max_steps)
	{
		return -1;
	}

	if (isinf(res))
	{
		return 0;
	}
	
	if (isinf(prev_res))
	{
		return 0;
	}	

	{
		double curr_accuracy = abs((res-prev_res)/res);
		double expected_accuracy = gvars->accuracy;

		if (curr_accuracy <= expected_accuracy)
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
}

void iterateVector (global_vars *gvars, std::vector<param_state> &param_state_list)
{

	omp_set_num_threads(4);	
	//#pragma omp parallel for	
	for (int i=0; i < param_state_list.size(); i++)
	{
		//int thr_num = omp_get_thread_num();
		//std::cout << thr_num << std::endl;
		
		//#pragma omp single
		//#pragma omp task
		{	
		std::vector<double> params;
		for (int j = 0; j < gvars->num_params; j++)
		{
			params.push_back(param_state_list[i].params[j]);
		}
		
		double res;

		double prev_res = param_state_list[i].ode_value;
		forwardEulerSolver (params, param_state_list[i].step_size, param_state_list[i].iter_value, gvars->init_val, gvars->num_iter, res);		
		
		int ret = checkForAccuracy (res, prev_res, param_state_list[i].iter_value, gvars);	

#if 0
		{
			std::cout << param_state_list[i].params[0] << "," << param_state_list[i].params[1] << "," << param_state_list[i].params[2] << "," << param_state_list[i].step_size << "," << param_state_list[i].iter_value << "," << param_state_list[i].ode_value << std::endl;
		}
#endif

		switch(ret)
		{
			case 0:
				{
					param_state_list[i].iter_value += 1;
					param_state_list[i].step_size /= 2;
					param_state_list[i].ode_value = res;
				}
				break;
			case 1:
				{
					param_state_list[i].move_flag = 1;
				}
				break;
			case -1:
				{
					param_state_list[i].move_flag = -1;
				}	
				break;
			default: break;


		}
		}
	}
}

int all_params_solved(std::vector<param_state> &param_state_list, std::vector<param_state> *param_state_resolved_list, std::vector<param_state> *param_state_unresolved_list)
{

	for (int i=0; i<param_state_list.size(); i++)
	{
		switch (param_state_list[i].move_flag)
		{
			case 1:
				{
					param_state_resolved_list->push_back(param_state_list[i]);
					param_state_list.erase(param_state_list.begin() + i);		
				}
				break;
			case -1:
				{
					param_state_unresolved_list->push_back(param_state_list[i]);
					param_state_list.erase(param_state_list.begin() + i);
				}
				break;
			default: break;
		}
	}

	if (param_state_list.size() == 0)
	{
		return 1;
	}
	else 
	{
		return 0;
	}
}

void OdeSolve(boost::python::list param_combs, boost::python::object num_params, boost::python::object accuracy, boost::python::object num_iter, boost::python::object init_val, boost::python::object max_steps)
{
	/*
	 * Define a vector of structures
	 * Populate each structure at a time 
	 * Once populated, keep adding it to the vector 
	 * Iterate through the vector and check if it has been populated correctly
	 */
	
	global_vars gvars;
	std::vector<param_state> param_state_list;
	std::vector<param_state> param_state_resolved_list;
	std::vector<param_state> param_state_unresolved_list;
	
	mytime_t start = NOW();

	populateGlobalState(&gvars, num_params, accuracy, num_iter, init_val, max_steps);
	populateParamState(&gvars, &param_state_list, param_combs, num_params);
	
	//std::cout << "Length of param list is " << param_state_list.size() << std::endl;
		
	/*
	 * while(all_params_solved)
	 * {
	 * 		run through everything
	 * 			* run the ode solver with a given step size
	 			* store the existing ode value
				* compare with the previous ode value 		 			
				* find if the accuracy is reached by the accuracy formula
				* if the current value is infinite then decrement the step size with the same ode value 
	
	 *
	 *
	 */

	//iterateVector (&gvars, param_state_list, &param_state_resolved_list, &param_state_unresolved_list);
	int num = 1;
	while (! all_params_solved(param_state_list, &param_state_resolved_list, &param_state_unresolved_list))
	{
		//std::cout << num << std::endl;
		iterateVector (&gvars, param_state_list);
		num++;
	}

	mytime_t end = NOW();
	
	std::cout << "Length of resolved " << param_state_resolved_list.size() << std::endl;
	std::cout << "Length of unresolved " << param_state_unresolved_list.size() << std::endl;
	std::cout << "Length of original " << param_state_list.size() << std::endl;
	std::cout << "Time Elapsed " << end - start << std::endl;

	/*
	 * Increase the number of iterations
	 * Increase the number of samples
	 * Calculate the time for sequential constructs
	 * Read about tasks and parallel for loops
	 * Introduce parallelism
	 * Notice the time taken again.
	 * Compare with the sequential
	 * Print out the unresolved and the resolved list
	 */

}

BOOST_PYTHON_MODULE(ode_solver)
{
	using namespace boost::python;
	def("OdeSolve", OdeSolve);
}
