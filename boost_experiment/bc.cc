#include <boost/python/module.hpp>
#include <boost/python.hpp>
#include <boost/python/def.hpp>
#include <vector>
#include <string>
#include <iostream>

void get_list(boost::python::list num_list)
{
#if 1
	for (int i = 0; i < len(num_list); i++)
	{
		int x = boost::python::extract<int>(num_list[i][0]);
		std::cout << "This is "	<< x << std::endl;
	}
#endif
}

BOOST_PYTHON_MODULE(get_num_list)
{
	using namespace boost::python;
	def("get_list", get_list);
}
