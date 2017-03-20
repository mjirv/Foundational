while read line; do
    python get_status.py "$line"
done <list_of_handles.txt
