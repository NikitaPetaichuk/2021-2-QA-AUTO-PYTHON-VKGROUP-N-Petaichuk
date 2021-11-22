import argparse
import json
from collections import Counter


OUTPUT_FILE_NAME = "NLP_result.txt"
OUTPUT_JSON_FILE_NAME = "NLP_result.json"


class NginxLogParser:

    def __init__(self, log_file_name):
        self.log_entries = []

        with open(log_file_name, "r") as log_file:
            while line := log_file.readline().strip():
                line_tokens = line.split()
                log_entry = {
                    "IP": line_tokens[0],
                    "METHOD": line_tokens[5][1:],
                    "URL": line_tokens[6],
                    "STATUS": line_tokens[8],
                    "SIZE": line_tokens[9]
                }
                self.log_entries.append(log_entry)

    @property
    def log_entries_count(self):
        return len(self.log_entries)

    def get_methods_count(self):
        log_entries_methods_list = [log_entry["METHOD"] for log_entry in self.log_entries]
        return Counter(log_entries_methods_list).items()

    def get_top_10_most_popular_requests(self):
        log_entries_urls_list = [log_entry["URL"] for log_entry in self.log_entries]
        return Counter(log_entries_urls_list).most_common(10)

    def get_top_5_biggest_requests_with_4xx_status(self):
        requests_with_4xx_status = [log_entry for log_entry in self.log_entries if log_entry["STATUS"].startswith("4")]
        requests_with_4xx_status.sort(key=lambda e: int(e["SIZE"]) if e["SIZE"] != "-" else -1, reverse=True)
        return requests_with_4xx_status[:5]

    def get_top_5_most_popular_requests_ips_with_5xx_status(self):
        ips_with_5xx_status = [log_entry["IP"] for log_entry in self.log_entries if log_entry["STATUS"].startswith("5")]
        return Counter(ips_with_5xx_status).most_common(5)


def create_args_parser():
    parser = argparse.ArgumentParser(description="Parser of nginx access log.")

    parser.add_argument("logfile", help="Path to the nginx access log")
    parser.add_argument("--count", help="Print requests count", dest="print_count", action="store_true")
    parser.add_argument("--methods-count",
                        help="Print methods count used in requests", dest="print_mc", action="store_true")
    parser.add_argument("--top-10-popular-requests",
                        help="Print top 10 most popular requests", dest="print_top_10", action="store_true")
    parser.add_argument("--top-5-biggest-4XX-requests",
                        help="Print top 5 biggest (according to size) requests with 4XX status",
                        dest="print_top_5_4XX", action="store_true")
    parser.add_argument("--top-5-5XX-requests-ips",
                        help="Print top 5 most popular requests ips with 5XX status",
                        dest="print_top_5_5XX", action="store_true")
    parser.add_argument("--all", help="Print all information about access nginx log",
                        dest="print_all", action="store_true")
    parser.add_argument("--json",
                        help="Return result in json format", dest="jsonify", action="store_true")

    parser.set_defaults(
        print_count=False, print_mc=False, print_top_10=False, print_top_5_4XX=False,
        print_top_5_5XX=False, print_all=False, jsonify=False
    )

    return parser


def handle_json_file_output(nginx_log_parser, args, no_flags):
    result_json = {}
    if args.print_count or no_flags or args.print_all:
        result_json["count"] = nginx_log_parser.log_entries_count
    if args.print_mc or args.print_all:
        result_json["methods_count"] = []
        for method, count in nginx_log_parser.get_methods_count():
            methods_count_entry = {
                "method": method,
                "count": count
            }
            result_json["methods_count"].append(methods_count_entry)
    if args.print_top_10 or args.print_all:
        result_json["most_popular_requests"] = []
        for url, count in nginx_log_parser.get_top_10_most_popular_requests():
            popular_request_entry = {
                "url": url,
                "count": count
            }
            result_json["most_popular_requests"].append(popular_request_entry)
    if args.print_top_5_4XX or args.print_all:
        result_json["biggest_4xx_requests"] = []
        for log_entry in nginx_log_parser.get_top_5_biggest_requests_with_4xx_status():
            popular_request_entry = {
                "url": log_entry["URL"],
                "status": log_entry["STATUS"],
                "size": log_entry["SIZE"],
                "ip": log_entry["IP"],
            }
            result_json["biggest_4xx_requests"].append(popular_request_entry)
    if args.print_top_5_5XX or args.print_all:
        result_json["popular_5xx_ips"] = []
        for ip, count in nginx_log_parser.get_top_5_most_popular_requests_ips_with_5xx_status():
            popular_request_entry = {
                "ip": ip,
                "count": count
            }
            result_json["popular_5xx_ips"].append(popular_request_entry)
    with open(OUTPUT_JSON_FILE_NAME, "w") as output_file:
        jsonified_result = json.dumps(result_json)
        output_file.write(jsonified_result)


def handle_regular_file_output(nginx_log_parser, args, no_flags):
    with open(OUTPUT_FILE_NAME, "w") as output_file:
        if args.print_count or no_flags or args.print_all:
            output_file.write(f"Общее количество запросов:\n{nginx_log_parser.log_entries_count}\n")
            output_file.write("\n")
        if args.print_mc or args.print_all:
            output_file.write("Общее количество запросов по типу:\n")
            for method, count in nginx_log_parser.get_methods_count():
                output_file.write(f"{method} - {count}\n")
            output_file.write("\n")
        if args.print_top_10 or args.print_all:
            output_file.write("Топ 10 самых частых запросов:\n")
            for url, count in nginx_log_parser.get_top_10_most_popular_requests():
                output_file.write(f"'{url}' - {count}\n")
            output_file.write("\n")
        if args.print_top_5_4XX or args.print_all:
            output_file.write(
                "Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:\n")
            for log_entry in nginx_log_parser.get_top_5_biggest_requests_with_4xx_status():
                output_file.write(
                    f"'{log_entry['URL']}' - {log_entry['STATUS']} - {log_entry['SIZE']} - {log_entry['IP']}\n")
            output_file.write("\n")
        if args.print_top_5_5XX or args.print_all:
            output_file.write(
                "Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:\n")
            for ip, count in nginx_log_parser.get_top_5_most_popular_requests_ips_with_5xx_status():
                output_file.write(f"'{ip}' - {count}\n")
            output_file.write("\n")


def main():
    args_parser = create_args_parser()
    args = args_parser.parse_args()

    no_first_three_flags = not (args.print_count or args.print_mc or args.print_top_10)
    no_second_three_flags = not (args.print_top_5_4XX or args.print_top_5_5XX or args.print_all)
    no_flags = no_first_three_flags and no_second_three_flags

    nginx_log_parser = NginxLogParser(args.logfile)
    if args.jsonify:
        handle_json_file_output(nginx_log_parser, args, no_flags)
    else:
        handle_regular_file_output(nginx_log_parser, args, no_flags)


if __name__ == "__main__":
    main()
