from fastapi import FastAPI
from config.database import get_connection

import time
import threading


app = FastAPI(
    title="CyberDemandIQ API",
    version="1.0.0"
)


# ============================================================
# CACHE
# ============================================================

CACHE_TTL = 60

_stats_cache = None
_stats_cache_time = 0

_cache_lock = threading.Lock()


def get_cached_stats():

    global _stats_cache
    global _stats_cache_time

    now = time.time()

    if (
        _stats_cache is not None
        and now - _stats_cache_time < CACHE_TTL
    ):
        return _stats_cache

    with _cache_lock:

        now = time.time()

        if (
            _stats_cache is not None
            and now - _stats_cache_time < CACHE_TTL
        ):
            return _stats_cache

        conn = None
        cur = None

        try:

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    label,
                    COUNT(*) AS records
                FROM cybersecurity.network_flows
                GROUP BY label
            """)

            rows = cur.fetchall()

            label_distribution = {
                row[0]: row[1]
                for row in rows
            }

            total_records = sum(
                label_distribution.values()
            )

            total_attack_records = sum(
                count
                for label, count
                in label_distribution.items()
                if label != "BENIGN"
            )

            total_benign_records = (
                label_distribution.get(
                    "BENIGN",
                    0
                )
            )

            attack_types = {
                label: count
                for label, count
                in label_distribution.items()
                if label != "BENIGN"
            }

            attack_types = dict(
                sorted(
                    attack_types.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            )

            _stats_cache = {
                "total_records": total_records,
                "total_attack_records": total_attack_records,
                "total_benign_records": total_benign_records,
                "label_distribution": label_distribution,
                "attack_types": attack_types
            }

            _stats_cache_time = time.time()

            return _stats_cache

        finally:

            if cur:
                cur.close()

            if conn:
                conn.close()


# ============================================================
# HEALTH
# ============================================================

@app.get("/")
def home():

    return {
        "status": "online",
        "service": "CyberDemandIQ API"
    }


# ============================================================
# DATABASE STATS
# ============================================================

@app.get("/api/database-stats")
def database_stats():

    try:

        stats = get_cached_stats()

        return {
            "database": "PostgreSQL",
            "schema": "cybersecurity",
            "table": "network_flows",
            "total_records": stats["total_records"],
            "label_distribution": stats[
                "label_distribution"
            ]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# ATTACK STATISTICS
# ============================================================

@app.get("/api/attack-statistics")
def attack_statistics():

    try:

        stats = get_cached_stats()

        return {
            "total_attack_records":
                stats["total_attack_records"],

            "total_benign_records":
                stats["total_benign_records"],

            "attack_types":
                stats["attack_types"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# NETWORK FLOWS
# ============================================================

@app.get("/api/network-flows")
def network_flows(
    limit: int = 100,
    attack_only: bool = False
):

    conn = None
    cur = None

    try:

        limit = min(
            max(limit, 1),
            200
        )

        conn = get_connection()
        cur = conn.cursor()

        columns = [
            "destination_port",
            "flow_duration",
            "total_fwd_packets",
            "total_backward_packets",
            "packet_length_mean",
            "packet_length_std",
            "flow_bytess",
            "flow_packetss",
            "label"
        ]

        select_columns = """
            destination_port,
            flow_duration,
            total_fwd_packets,
            total_backward_packets,
            packet_length_mean,
            packet_length_std,
            flow_bytess,
            flow_packetss,
            label
        """

        if attack_only:

            query = f"""
                SELECT
                    {select_columns}
                FROM cybersecurity.network_flows
                WHERE label <> 'BENIGN'
                LIMIT %s
            """

        else:

            query = f"""
                SELECT
                    {select_columns}
                FROM cybersecurity.network_flows
                LIMIT %s
            """

        cur.execute(
            query,
            (limit,)
        )

        rows = cur.fetchall()

        records = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "count": len(records),
            "records": records
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()