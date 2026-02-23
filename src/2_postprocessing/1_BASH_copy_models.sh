# !/bin/bash

# !!! Warning: this step will copy all the models from AF3 to a new directory. 
#      It should be changed in case you expect there to be too many models in the final directory.
INPUT_PATH=/projects/0/prjs1135/AF3_TCR_pipeline_test/AF3_jsons/
OUTPUT_PATH=/projects/0/prjs1135/AF3_TCR_pipeline_test/all_tcrs/

for case_path in "$INPUT_PATH"/*; do
    python copy_and_name_models_af3.py --model-dir $case_path/AF3_inference_output \
        --output-dir $OUTPUT_PATH \

    done
