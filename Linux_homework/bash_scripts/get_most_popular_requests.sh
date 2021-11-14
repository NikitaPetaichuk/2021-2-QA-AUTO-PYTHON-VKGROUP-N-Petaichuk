echo "Топ 10 самых частых запросов:" > "bash_10_MPR_output.txt"
cat < "$1" | awk '{print $7}' | sort | uniq -c | sort -k1nr | head | awk '{printf "%s\n%s\n\n", $2, $1}' >> "bash_10_MPR_output.txt"