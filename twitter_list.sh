declare -a arr=("@test1" "@test2" "@etc")
for i in "${arr[@]}"
do
	python twitteranalyzer.py "$i" | tail -1 > "$i"_output.json
done
