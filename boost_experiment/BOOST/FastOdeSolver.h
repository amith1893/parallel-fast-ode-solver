#ifndef ODE_SOLVER_H_
#define ODE_SOLVER_H_

typedef struct
{
	double *params;
	double step_size;
	double iter_value;
	double ode_value;
	int move_flag;

} param_state;

typedef struct
{
	int num_params;
	int num_iter;
	int max_steps;
	double accuracy;
	double init_val;

} global_vars;

#endif //for ODE_SOLVER_H_
