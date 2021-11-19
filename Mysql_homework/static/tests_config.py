class TestsConfig:

    ACCESS_LOG_DIRECTORY = "static"
    ACCESS_LOG_NAME = 'access.log'
    INTERNAL_LOG_FILE_NAME = "tests.log"

    MYSQL_USER = "root"
    MYSQL_PASSWORD = "pass"
    MYSQL_DB = "TEST_SQL"

    TABLES_NAMES = [
        'requests_count',
        'methods_count',
        'popular_requests',
        'biggest_4xx_requests',
        'popular_5xx_requests'
    ]
