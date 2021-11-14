echo "Общее количество запросов:" > "bash_count_output.txt"
cat < "$1" | wc -l >> "bash_count_output.txt" &
