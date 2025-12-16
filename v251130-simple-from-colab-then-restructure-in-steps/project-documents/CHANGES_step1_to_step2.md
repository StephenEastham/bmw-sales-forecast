flowchart TD
  %% High-level transition
  S1["step1 (baseline)"] --> S2["step2 (changes)"]

  %% Files affected
  subgraph A [Modified Files]
    direction TB
    cfg_mod["config.py<br/>(modified)"]
    main_mod["main.py<br/>(modified)"]
  end

  subgraph B [Added Files]
    direction TB
    data_add["data.py<br/>(added)"]
  end

  subgraph C [Unchanged]
    direction TB
    utils_same["utils.py<br/>(unchanged)"]
  end

  S2 --> A
  S2 --> B
  S2 --> C

 
  cfg_mod --> cfg_dot1["pandas import & settings"]
  cfg_mod --> cfg_dot2["ENABLE_DATA_PROCESSING flag"]

  data_add --> d_dot1["download_data_file()<br/>(network + write)"]
  data_add --> d_dot2["download_required_files()<br/>(wrapper) "]
  data_add --> d_dot3["load_and_explore_data()<br/>(read CSV, print) "]
  data_add --> d_dot4["preprocess_data()<br/>(in-memory cleaning) "]

  main_mod --> m_dot1["import ENABLE_DATA_PROCESSING<br/>import DATA_CSV_FILE"]
  main_mod --> m_dot2["import data module"]
  main_mod --> m_dot3["test_data_module()<br/>(sequence: clean -> download -> load -> preprocess)"]

  cfg_dot1 --> d_dot3    
  cfg_dot2 --> main_mod 
  d_dot1 --> d_dot2     
  d_dot2 --> m_dot3    
  d_dot3 --> d_dot4     
  utils_same --> main_mod
  utils_same --> d_dot1   


  classDef modified fill:#f9f,stroke:#333,stroke-width:1px;
  classDef added fill:#efe,stroke:#333,stroke-width:1px;
  classDef unchanged fill:#eef,stroke:#333,stroke-width:1px;
  class cfg_mod,main_mod modified
  class data_add added
  class utils_same unchanged
```
