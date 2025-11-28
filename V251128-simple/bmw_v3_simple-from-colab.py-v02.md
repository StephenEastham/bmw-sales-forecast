```mermaid
flowchart TD
  %% Level 1 (L1): Entry
  Start([Start: main.py]) --> L1_Config

  %% Level 2 (L2): high-level pipeline stages (flags control branches)
  subgraph L2["L2: Pipeline Stages"]
    direction TB
    L1_Config[[Config: load constants & flags]] 
    CleanOutputs["Utils: clean_outputs()"]
    Stage_Data{{"ENABLE_DATA_PROCESSING ?"}}
    Stage_TS{{"ENABLE_TIME_SERIES ?"}}
    Stage_Static{{"ENABLE_STATIC_PLOTS ?"}}
    Stage_Reporting{{"ENABLE_REPORTING ?"}}
    Stage_Dash{{"ENABLE_DASHBOARDS ?"}}
    Stage_Agg{{"ENABLE_AGGREGATOR ?"}}
  end

  Start --> L1_Config --> CleanOutputs
  CleanOutputs --> Stage_Data
  CleanOutputs --> Stage_TS
  CleanOutputs --> Stage_Static
  CleanOutputs --> Stage_Reporting
  CleanOutputs --> Stage_Dash
  CleanOutputs --> Stage_Agg

  %% Level 3 (L3): modules invoked for each stage
  subgraph DataModule["L3: data.py"]
    direction TB
    DL_REQ["download_required_files()"]
    LOAD["load_and_explore_data(csv)"]
    PREP["preprocess_data(df)"]
  end

  subgraph AnalysisModule["L3: analysis.py"]
    direction TB
    AGG["aggregate_time_series(df_clean)"]
  end

  subgraph VizStaticModule["L3: viz_static.py"]
    direction TB
    OVERVIEW["create_overview_visualizations(df_yearly, df_clean)"]
    HEATMAP_STATIC["create_heatmap(df_clean)"]
  end

  subgraph VizInteractiveModule["L3: viz_interactive.py"]
    direction TB
    DASH["create_interactive_dashboard(ts_years, ts_data, df_yearly, df_clean)"]
    HEATMAP_INT["create_heatmap_interactive(df_model_yearly)"]
  end

  subgraph ReportingModule["L3: reporting.py"]
    direction TB
    MONTHLY["generate_monthly_report(df_clean, average_sales)"]
    FINAL["generate_final_summary(df_clean, average_sales, ts_years, ts_data)"]
  end

  subgraph UtilsModule["L3: utils.py"]
    direction TB
    SETUP_LOG["setup_logger(...)"]
    ZIP_ALL["zip_all_outputs()"]
    PRINT_SEC["print_section(title)"]
  end

  subgraph AggregatorModule["L3: aggregator.py"]
    direction TB
    AGG_HTML["create_aggregator_html()"]
  end

  %% Connect stage decisions to modules
  Stage_Data -->|yes| DL_REQ --> LOAD --> PREP
  Stage_Data -->|no| skip_data["skip data stage"]

  Stage_TS -->|yes| AGG
  Stage_TS -->|no| skip_ts["skip ts"]

  Stage_Static -->|yes| OVERVIEW --> HEATMAP_STATIC
  Stage_Dash -->|yes| DASH --> HEATMAP_INT

  Stage_Reporting -->|yes| MONTHLY --> WRITE_MONTHLY["write sales_report_*.txt"] --> FINAL --> WRITE_SUM["write ANALYSIS_SUMMARY.txt"]
  Stage_Agg -->|yes| AGG_HTML --> ZIP_ALL

  %% Level 4 (L4): functions -> sub-actions
  subgraph DataActions["L4: Data actions / substeps"]
    direction TB
    Dld_file["download_data_file(url)"]
    ReadCSV["pd.read_csv()"]
    PrintSummary[print head, dtypes, describe]
    CleanCols[trim columns, detect empty columns]
  end

  DL_REQ --> Dld_file
  LOAD --> ReadCSV --> PrintSummary
  PREP --> CleanCols

  subgraph AnalysisActions["L4: Analysis substeps"]
    direction TB
    YearAgg[groupby Year -> Total_Sales]
    ComputeTS[extract ts_data, ts_years]
    YoY[compute YoY growth]
    ModelRegionAgg[groupby Model & Region]
  end

  AGG --> YearAgg --> ComputeTS --> YoY --> ModelRegionAgg

  subgraph VizActions["L4: Viz substeps"]
    direction TB
    PlotTrend[plot line + markers -> save 01_sales_overview.png]
    PlotYoY[plot bar YoY -> part of overview]
    PlotModelBar[barh top models]
    SaveOverview["save PNG -> out_path('01_sales_overview.png')"]
    SaveHeatmap["save heatmap -> out_path('02_model_region_heatmap.png')"]
  end

  OVERVIEW --> PlotTrend --> PlotYoY --> PlotModelBar --> SaveOverview
  HEATMAP_STATIC --> SaveHeatmap

  subgraph ReportingActions["L4: Reporting substeps"]
    direction TB
    FormatReport[format strings / f-strings]
    TopModels[compute top 5 models]
    ByRegion[compute totals & percentages]
    WriteFileMonthly[write to sales_report_timestamp.txt]
    WriteSummary[write ANALYSIS_SUMMARY.txt]
  end

  MONTHLY --> FormatReport --> TopModels --> ByRegion --> WriteFileMonthly
  FINAL --> FormatReport --> WriteSummary

  subgraph AggActions["L4: Aggregator substeps"]
    direction TB
    CollectPNGs[list OUTPUT_DIR *.png]
    CollectHTML[list OUTPUT_DIR *.html]
    BuildHTML[compose 07_all_outputs.html]
    OpenBrowser["webbrowser.open(...)"]
    ZipOutputs["zip_all_outputs()"]
  end

  AGG_HTML --> CollectPNGs --> CollectHTML --> BuildHTML --> OpenBrowser
  ZIP_ALL --> ZipOutputs

  %% Level 5 (L5): concrete operations / file outputs
  ReadCSV --> FileIn[("reads file: `DATA_CSV_FILE` or URL")]
  WriteFileMonthly --> FileMonthly[("outputs/sales_report_YYYYMMDD_HHMMSS.txt")]
  SaveOverview --> PNG01[("outputs/01_sales_overview.png")]
  SaveHeatmap --> PNG02[("outputs/02_model_region_heatmap.png")]
  FIG05[("outputs/05_interactive_dashboard.html")]
  FIG06[("outputs/06_model_heatmap_interactive.html")]
  BuildHTML --> ALL_HTML[("outputs/07_all_outputs.html")]
  ZipOutputs --> ZIP_FILE[("outputs/all_outputs.zip")]

  DASH --> FIG05
  HEATMAP_INT --> FIG06

  %% Utilities usage
  CleanOutputs --> PRINT_SEC
  PRINT_SEC -->|used by many| ReadCSV
  SETUP_LOG -->|optional| Start
  ZIP_ALL --> ZipOutputs

  %% End
  WriteSummary --> End([End: SUCCESS])
  FileMonthly --> End
  ALL_HTML --> End
  ZipOutputs --> End

  %% Styling / notes
  classDef stage fill:#f3f4f6,stroke:#333,stroke-width:1px;
  class L1_Config,CleanOutputs,Stage_Data,Stage_TS,Stage_Static,Stage_Reporting,Stage_Dash,Stage_Agg stage;
  ```