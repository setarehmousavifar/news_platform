"""
Prefer mysqlclient; on Windows fall back to PyMySQL when mysqlclient
is not installed (common on Windows without Visual C++ build tools).
"""
try:
    import MySQLdb  # noqa: F401
except ImportError:  # pragma: no cover
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
