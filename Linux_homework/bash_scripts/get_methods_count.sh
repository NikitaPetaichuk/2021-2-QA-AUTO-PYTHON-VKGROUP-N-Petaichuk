echo "Общее количество запросов по типу:" > "bash_MC_output.txt"
cat < "$1" | awk '{print $6}' | sed 's/"//g' | sort | uniq -c | awk '{printf "%s - %s\n", $2, $1}' >> "bash_MC_output.txt"