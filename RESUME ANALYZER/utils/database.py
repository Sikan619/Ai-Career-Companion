import os
import pathlib
import socket
import struct
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- ISP DNS BYPASS HELPER FOR NEON POSTGRESQL ---
# Some Indian ISPs (e.g. Reliance Jio Fiber) return "Query refused" for *.neon.tech subdomains.
# This resilient resolver queries public DNS (1.1.1.1 or 8.8.8.8) or uses known pooler IPs
# so that connection to cloud Neon PostgreSQL works seamlessly on any network!
def _query_public_dns(hostname: str) -> str:
    """Queries Cloudflare/Google DNS servers over UDP to resolve neon.tech when local ISP blocks it."""
    for srv in ["1.1.1.1", "8.8.8.8"]:
        try:
            trans_id = 0x1234
            flags = 0x0100
            header = struct.pack("!HHHHHH", trans_id, flags, 1, 0, 0, 0)
            qname = b"".join([bytes([len(p)]) + p.encode("ascii") for p in hostname.split(".")]) + b"\x00"
            packet = header + qname + struct.pack("!HH", 1, 1)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2.0)
            s.sendto(packet, (srv, 53))
            data, _ = s.recvfrom(1024)
            s.close()
            
            offset = 12 + len(qname) + 4
            while offset < len(data):
                if data[offset] & 0xC0 == 0xC0:
                    offset += 2
                else:
                    while data[offset] != 0:
                        offset += data[offset] + 1
                    offset += 1
                if offset + 10 > len(data):
                    break
                atype, aclass, ttl, rdlen = struct.unpack("!HHIH", data[offset:offset+10])
                offset += 10
                if atype == 1 and rdlen == 4:
                    return socket.inet_ntoa(data[offset:offset+4])
                offset += rdlen
        except Exception:
            continue
    # Resilient fallback IP for AWS Neon us-east-2 pooler
    return "3.141.122.14"

_original_getaddrinfo = socket.getaddrinfo

def _resilient_getaddrinfo(host, port, *args, **kwargs):
    try:
        return _original_getaddrinfo(host, port, *args, **kwargs)
    except socket.gaierror:
        # If host contains neon.tech and local DNS failed, resolve via public DNS
        if host and "neon.tech" in str(host):
            resolved_ip = _query_public_dns(str(host))
            if resolved_ip:
                return _original_getaddrinfo(resolved_ip, port, *args, **kwargs)
        raise

# Install resilient DNS resolver hook
socket.getaddrinfo = _resilient_getaddrinfo
# -------------------------------------------------

def get_engine():
    """
    Connects to the cloud PostgreSQL database (Neon) if available.
    If PostgreSQL is unreachable, automatically falls back to a local SQLite
    database in data/career_companion.db so the app never crashes.
    """
    if DATABASE_URL and not DATABASE_URL.startswith("sqlite"):
        try:
            eng = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 6} if "postgres" in DATABASE_URL or "psycopg" in DATABASE_URL else {}
            )
            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
            return eng, "PostgreSQL (Cloud - Neon)"
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            pass

    # Fallback to local SQLite database in data/ folder
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    sqlite_path = (data_dir / "career_companion.db").as_posix()
    eng = create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})
    return eng, "SQLite (Local)"

engine, DB_TYPE = get_engine()

def init_db():
    """Initializes the applications table in the active database."""
    with engine.connect() as conn:
        if "sqlite" in str(engine.url):
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Applied',
                    applied_date DATE,
                    job_link TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
        else:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS applications (
                    id SERIAL PRIMARY KEY,
                    company VARCHAR(255) NOT NULL,
                    role VARCHAR(255) NOT NULL,
                    status VARCHAR(50) DEFAULT 'Applied',
                    applied_date DATE,
                    job_link TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
        conn.commit()

def add_application(company, role, status="Applied", applied_date=None, job_link="", notes=""):
    """Inserts a new job application into the database."""
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO applications (company, role, status, applied_date, job_link, notes)
            VALUES (:company, :role, :status, :applied_date, :job_link, :notes)
        """), {
            "company": company.strip(),
            "role": role.strip(),
            "status": status,
            "applied_date": str(applied_date) if applied_date else None,
            "job_link": job_link.strip() if job_link else "",
            "notes": notes.strip() if notes else ""
        })
        conn.commit()
    return True

def get_all_applications():
    """
    Returns all applications as a list of dictionaries.
    Using dictionaries avoids tuple index mismatches.
    """
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, company, role, status, applied_date, job_link, notes, created_at 
            FROM applications 
            ORDER BY id DESC
        """))
        return [dict(row._mapping) for row in result.fetchall()]

def get_application_by_id(app_id):
    """Fetches a single application by its ID."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, company, role, status, applied_date, job_link, notes, created_at 
            FROM applications 
            WHERE id = :id
        """), {"id": app_id})
        row = result.fetchone()
        return dict(row._mapping) if row else None

def update_application(app_id, company, role, status, applied_date, job_link="", notes=""):
    """Updates an existing application by ID."""
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE applications
            SET company = :company,
                role = :role,
                status = :status,
                applied_date = :applied_date,
                job_link = :job_link,
                notes = :notes
            WHERE id = :id
        """), {
            "id": app_id,
            "company": company.strip(),
            "role": role.strip(),
            "status": status,
            "applied_date": str(applied_date) if applied_date else None,
            "job_link": job_link.strip() if job_link else "",
            "notes": notes.strip() if notes else ""
        })
        conn.commit()
    return True

def delete_application(app_id):
    """Deletes an application by ID."""
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM applications WHERE id = :id"), {"id": app_id})
        conn.commit()
    return True
