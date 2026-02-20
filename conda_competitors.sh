conda install conda-forge::networkit
conda install rapidsai::cugraph
python3 python_scripts/networkit_leiden.py graphs/ comp_data/networkit_leiden_results.txt
python3 python_scripts/networkit_louvain.py graphs/ comp_data/networkit_louvain_results.txt
python3 python_scripts/run_cugraph_louvain.py graphs/ comp_data/cugraph_louvain_results.txt
python3 python_scripts/run_cugraph_leiden.py graphs/ comp_data/cugraph_leiden_results.txt