# Educational Diagrams for `bmw_v3_simple-from-colab.py`

These diagrams provide different perspectives on the code to help a beginner understand not just the *flow* (execution order), but also the *data structure*, *data lifecycle*, and *function interactions*.

## 1. Data Structure Diagram (Class Diagram Style)

**Concept:** Although the code uses Pandas DataFrames and not custom classes, visualizing the "Schema" of the data at different stages helps you understand what columns are available.

**Level 5 Abstraction:** Shows the key DataFrames and their primary columns/types.

```mermaid
classDiagram
    note "This diagram visualizes DataFrames as Classes to show their structure."

    class RawCSV {
        +String Model
        +Int Year
        +String Region
        +Float Price_USD
        +Int Sales_Volume
        +... (other raw cols)
    }

    class CleanedDataFrame {
        +String Model
        +Int Year
        +String Region
        +Float Price_USD
        +Int Sales_Volume
        -- Transformations --
        +Stripped Column Names
        +No Empty Columns
    }

    class YearlyAggregated {
        +Int Year
        +Int Total_Sales
        +Float YoY_Growth
    }

    class ModelAggregated {
        +Int Year
        +String Model
        +Int Sales_Volume
    }

    class RegionAggregated {
        +Int Year
        +String Region
        +Int Sales_Volume
    }

    RawCSV --> CleanedDataFrame : preprocess_data()
    CleanedDataFrame --> YearlyAggregated : aggregate_time_series()
    CleanedDataFrame --> ModelAggregated : aggregate_time_series()
    CleanedDataFrame --> RegionAggregated : aggregate_time_series()
```

## 2. Data Lifecycle (State Diagram)

**Concept:** This shows how the *state* of your data changes as it moves through the pipeline. It answers "What condition is my data in right now?"

**Level 5 Abstraction:** Focuses on the major transformations of the dataset.

```mermaid
stateDiagram-v2
    [*] --> NotExists : Start
    NotExists --> OnDisk : download_required_files()
    OnDisk --> InMemoryRaw : load_and_explore_data()
    
    state "Raw DataFrame" as InMemoryRaw
    state "Cleaned DataFrame" as Cleaned
    state "Aggregated Data" as Aggregated
    state "Visualized/Reported" as Final

    InMemoryRaw --> Cleaned : preprocess_data()\n(Trims cols, checks nulls)
    
    Cleaned --> Aggregated : aggregate_time_series()\n(Groups by Year/Model/Region)
    
    Aggregated --> Final : Visualization & Reporting Functions
    
    Final --> [*] : Script Ends
```

## 3. Function Interaction (Sequence Diagram)

**Concept:** This shows the "conversation" between the main script and the helper functions. It highlights the *input* (arguments) and *output* (return values) of each call.

**Level 5 Abstraction:** Shows the Main Script as the controller calling specific functional blocks.

```mermaid
sequenceDiagram
    participant Main as Main Script
    participant Data as Data Module
    participant Analysis as Analysis Module
    participant Viz as Visualization Module
    participant Report as Reporting Module

    Note over Main: 1. Data Stage
    Main->>Data: download_required_files()
    Data-->>Main: (File saved to disk)
    Main->>Data: load_and_explore_data(csv_file)
    Data-->>Main: Returns df (Raw)
    Main->>Data: preprocess_data(df)
    Data-->>Main: Returns df_clean

    Note over Main: 2. Analysis Stage
    Main->>Analysis: aggregate_time_series(df_clean)
    Analysis-->>Main: Returns df_yearly, ts_data, ts_years...

    Note over Main: 3. Visualization Stage
    Main->>Viz: create_overview_visualizations(df_yearly, df_clean)
    Viz-->>Main: (Saves .png files)
    Main->>Viz: create_interactive_dashboard(...)
    Viz-->>Main: (Saves .html files)

    Note over Main: 4. Reporting Stage
    Main->>Report: generate_monthly_report(df_clean, avg_sales)
    Report-->>Main: Returns report_string
    Main->>Main: Writes report to .txt
    Main->>Report: generate_final_summary(...)
    Report-->>Main: Prints & Saves Summary
```
