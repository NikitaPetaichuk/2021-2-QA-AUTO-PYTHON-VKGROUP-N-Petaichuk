HttpMethods=("GET" "POST" "PUT" "DELETE" "HEAD" "CONNECT" "OPTIONS" "TRACE")

echo "Общее количество запросов по типу:" > "bash_MC_output.txt"
cat < "$1" | awk '{print $6}' | sed 's/"//g' | sort | uniq -c | awk '{printf "%s - %s\n", $2, $1}' | while read -r line
do
    method=$(echo "$line" | awk '{print $1}')
    if ! echo "${HttpMethods[@]}" | grep -qw "${method}"; then
        line="${line//${method}/UNDEFINED}"
    fi
    echo "$line"
done >> "bash_MC_output.txt"