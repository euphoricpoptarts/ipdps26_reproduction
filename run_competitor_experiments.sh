g++ -O3 -o metis2gala metis2galabin.cpp
mkdir comp_data
python3 python_scripts/run_gala.py graphs/ comp_data/gala_results.txt
python3 python_scripts/run_vlouvain.py mtx/ comp_data/vlouv_results.txt
python3 python_scripts/run_gve_louvain.py mtx/ comp_data/gve_louvain_results.txt
python3 python_scripts/run_gve_leiden.py mtx/ comp_data/gve_leiden_results.txt
python3 python_scripts/run_vieclus.py graphs/ comp_data/vieclus_results.txt