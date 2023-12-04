
This repository is for generating `coco_test.json` to inference custom test data.
---
### Parameters
- "rootDircetory": Root path which contains 'annotations', 'train', and 'val'.
- "testPath": Subpath of "rootDirectory" which contains image data to inference.
- "categories": Names of category that test data have.
- "ensuredFormat": Filtering the extensions which is not included on this list.

#### To generate `coco_test.json`

```bash
python coco_test_format_generator.py
```

