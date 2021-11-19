import logging
from collections import Counter

from models.model import RequestsCount, MethodsCount, PopularRequests, Biggest4XXRequests, Popular5XXRequestsIP
from mysql_client.mysql_client import MysqlClient


class MysqlNginxLogParser:

    methods_list = ["GET", "POST", "PUT", "DELETE", "HEAD", "CONNECT", "OPTIONS", "TRACE"]

    def _parse_file(self, log_file_name):
        with open(log_file_name, "r") as log_file:
            while line := log_file.readline().strip():
                line_tokens = line.split()
                method = line_tokens[5][1:]
                log_entry = {
                    "IP": line_tokens[0],
                    "METHOD": method if method in self.methods_list else "UNDEFINED",
                    "URL": line_tokens[6],
                    "STATUS": line_tokens[8],
                    "SIZE": line_tokens[9]
                }
                self.log_entries.append(log_entry)

    def __init__(self, log_file_name, mysql_user, mysql_password, mysql_db_name):
        self.log_entries = []
        self.mysql_client = MysqlClient(mysql_user, mysql_password, mysql_db_name)
        self.logger = logging.getLogger('tests')

        self._parse_file(log_file_name)
        self.mysql_client.connect()

    def _add_entity_to_db(self, entity_class, entity_values):
        self.logger.debug(f"Adding {entity_values} data to {entity_class.__name__} table")

        entity = entity_class(**entity_values)
        self.mysql_client.session.add(entity)
        self.mysql_client.session.commit()

    def write_to_db_requests_count(self):
        self.logger.info("Writing to DB requests count data")

        requests_count = len(self.log_entries)
        self._add_entity_to_db(RequestsCount, {"count": requests_count})
        return 1

    def write_to_db_methods_count(self):
        self.logger.info("Writing to DB methods count data")

        log_entries_methods_list = [log_entry["METHOD"] for log_entry in self.log_entries]
        methods_count_list = Counter(log_entries_methods_list).items()
        for method, count in methods_count_list:
            self._add_entity_to_db(MethodsCount, {
                "method": method,
                "count": count
            })
        return len(methods_count_list)

    def write_to_db_10_popular_requests(self):
        self.logger.info("Writing to DB popular requests data")

        log_entries_urls_list = [log_entry["URL"] for log_entry in self.log_entries]
        popular_requests_list = Counter(log_entries_urls_list).most_common(10)
        for url, count in popular_requests_list:
            self._add_entity_to_db(PopularRequests, {
                "url": url,
                "count": count
            })
        return len(popular_requests_list)

    def write_to_db_5_biggest_4xx_requests(self):
        self.logger.info("Writing to DB biggest requests data (with 4XX status code)")

        requests_with_4xx_status = [log_entry for log_entry in self.log_entries if log_entry["STATUS"].startswith("4")]
        requests_with_4xx_status.sort(key=lambda e: int(e["SIZE"]) if e["SIZE"] != "-" else -1, reverse=True)
        border_index = min(5, len(requests_with_4xx_status))
        biggest_4xx_requests = requests_with_4xx_status[:border_index]
        for request_data in biggest_4xx_requests:
            self._add_entity_to_db(Biggest4XXRequests, {
                "url": request_data["URL"],
                "status": request_data["STATUS"],
                "size": request_data["SIZE"],
                "ip": request_data["IP"],
            })
        return len(biggest_4xx_requests)

    def write_to_db_5_popular_5xx_requests_ip(self):
        self.logger.info("Writing to DB popular requests data (with 5XX status code)")

        ips_with_5xx_status = [log_entry["IP"] for log_entry in self.log_entries if log_entry["STATUS"].startswith("5")]
        popular_5xx_requests_ip = Counter(ips_with_5xx_status).most_common(5)
        for ip, count in popular_5xx_requests_ip:
            self._add_entity_to_db(Popular5XXRequestsIP, {
                "ip": ip,
                "count": count
            })
        return len(popular_5xx_requests_ip)
