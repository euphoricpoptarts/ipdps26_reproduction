g++ -O3 -o metis2gala c++_programs/metis2galabin.cpp
mkdir comp_data
python3 python_scripts/run_gala.py graphs/ comp_data/gala_results.txt
python3 python_scripts/run_vlouvain.py mtx/ comp_data/vlouv_results.txt