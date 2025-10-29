# Memory Pool

The complete dataset of 60 apps memory pool used in our experiments is publicly available at: [Google Drive](https://drive.google.com/drive/folders/1x7sDGJ4R_MmR57kVGi64IWekAAxxqbUV?usp=sharing)

Memory Pool Data Structure:

```
├───data
|   ├───screenshots
|   |   ├───step_0.png
|   |   ├───step_1.png
|   |   ...
|   ├───ui_trees
|   |   ├───step_0.xml
|   |   ├───step_1.xml
|   |   ...
|   └───record.json
├───xxx.apk
├───segments_data.json
└───app_analysis_result.txt
```

MemoDroid addresses this by introducing a **three-layer memory mechanism**:
- **Episodic Memory**: Captures functional interaction traces (screenshots, actions, transition graphs).
- **Reflective Memory**: Summarizes redundant or issue-prone behaviors into natural language.
- **Strategic Memory**: Synthesizes high-level exploration strategies across apps or domains.

The `data/` dir is Level-1 Episodic Memory, the `segments_data.json` is Level-2 Reflective Memory, and the `app_analysis_result.txt` is Level-3 Strategic Memory.