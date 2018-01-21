#g++ FastOdeSolver.cc -shared -fPIC -o ode_solver.so -I/usr/include/python2.7 -lboost_python
#mpicxx FastOdeSolver.cc -shared -fPIC -o ode_solver.so -I/usr/include/python2.7 -lboost_python -fopenmp
mpicxx FastOdeSolverModified.cc -shared -fPIC -o ode_solver_modf.so -I/usr/include/python2.7 -lboost_python -fopenmp


#sudo cp ode_solver.so /usr/local/lib
#LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

#python FastOde.py config.ini
