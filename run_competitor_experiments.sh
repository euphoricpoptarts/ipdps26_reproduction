g++ -O3 -o metis2gala metis2galabin.cpp
mkdir comp_data
python3 python_scripts/run_gala.py graphs/ comp_data/gala_results.txt
python3 python_scripts/run_vlouvain mtx/ comp_data/vlouv_results.txt
python3 python_scripts/run_gve_louvain mtx/ comp_data/gve_louvain_results.txt
python3 python_scripts/run_gve_leiden mtx/ comp_data/gve_leiden_results.txt