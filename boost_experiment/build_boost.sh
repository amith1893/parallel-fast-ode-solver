g++ bc.cc -shared -fPIC -o get_num_list.so -I/usr/include/python2.7 -lboost_python
sudo cp get_num_list.so /usr/local/lib
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

python bc.py
