declare -a arr=("social_attention" "achievement" "interpersonal_harmony" "uncertainty" "innovation" "threats" "rewards" "communal_goals" "creativity" "intellectual_stimulation" "efficiency" "order")
for i in "${arr[@]}"
do
    grep "'$i': True" $1 | cut -d ':' -f 1 | sed -e "s/[{']//g" > "audience_$i.txt"
done
