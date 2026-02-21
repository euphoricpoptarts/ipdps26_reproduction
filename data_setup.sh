wget -O graphs.tar.xz https://scholarsphere.psu.edu/resources/fd9ba209-a0cd-4f33-994b-c22ae3bcb243/downloads/35163?download=true
unxz --threads=0 --verbose graphs.tar.xz
tar -xvf graphs.tar
rm graphs.tar
g++ -O3 -o metis2mtx c++_programs/metis2mtx.cpp
mkdir mtx
python3 python_scripts/convert_all_graphs.py graphs/ mtx/
