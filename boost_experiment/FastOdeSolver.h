#ifndef ODE_SOLVER_H_
#define ODE_SOLVER_H_

typedef struct
{
	double *params;
	double step_size;
	double iter_value;
	double ode_value;

} param_state;

#endif //for ODE_SOLVER_H_
