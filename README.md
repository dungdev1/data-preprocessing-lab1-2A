# data-preprocessing-lab1-2A
A solution for data preprocessing lab1, part 2A, HCMUS, Ho Chi Minh City, VietNam
## Run
a) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "minMaxNormalization" --new_min "min" --new_max "max"
where 	- new_min, new_max is option: default is 0.0 and 1.0
	      - "path" may be absolute path or relative path
ex: lab1.py "name" "id" -i "123.csv" -o "result.csv" -t "minMaxNormalization" --new_min 3.0 --new_max 5.0 

b) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "zScoreNormalization"

c) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "equalWidthDiscretize" --bin "number_bins"

d) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "equalFrequencyDiscretize" --bin "number_bins"

e) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "removeMissingInstance"

f) lab1.py "propList" -i/--input_path "path" -o/--output_path "path" -t/--task "fillInMissingInstance"
