flowchart
  subgraph MOD[Modified Files]
    direction TB
    cfg_mod["config.py<br/>(modified)"]
    main_mod["main.py<br/>(modified)"]
  end

  subgraph ADD[Added Files]
    direction TB
    data_add["data.py<br/>(added)"]
  end

  subgraph SAME[Unchanged Files]
    direction TB
    utils_same["utils.py<br/>(unchanged)"]
  end


  cfg_mod --> cfg1["pandas settings"]
  cfg_mod --> cfg2["ENABLE_DATA_PROCESSING flag"]

  data_add --> d1["download_data_file()<br/>(network + write)"]
  data_add --> d2["download_required_files()<br/>(wrapper)"]
  data_add --> d3["load_and_explore_data()<br/>(read CSV, print)"]
  data_add --> d4["preprocess_data()<br/>(in-memory clean)"]

  main_mod --> m1["import ENABLE_DATA_PROCESSING<br/>import DATA_CSV_FILE"]
  main_mod --> m2["import data module"]
  main_mod --> m3["test_data_module()<br/>(clean -> download -> load -> preprocess)"]

 
  cfg1 --- d3 
  cfg2 --> main_mod
  d1 --> d2
  d2 --> m3
  d3 --> d4
  utils_same --> main_mod
  utils_same --> d1

 
  classDef added fill:#e6ffed,stroke:#2e7d32,stroke-width:1px;
  classDef modified fill:#fff4e5,stroke:#ff9800,stroke-width:1px;
  classDef unchanged fill:#eef6ff,stroke:#1565c0,stroke-width:1px;
  class cfg_mod,main_mod modified
  class data_add added
  class utils_same unchanged

