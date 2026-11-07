#!/usr/bin/env python3
"""Inventario e importacion local de cuentas verificadas, sin iniciar sesiones."""
import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

EMAIL = re.compile(r"^[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}$", re.I)

def read_accounts(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        obj = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(obj, dict):
            obj = obj.get("accounts", [])
        if not isinstance(obj, list):
            raise ValueError("JSON: se esperaba lista o accounts")
        return [x for x in obj if isinstance(x, dict)]
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("----")
        rows.append({"email": fields[0].strip(), "password": fields[1].strip() if len(fields)>1 else "",
                     "recovery_email": fields[2].strip() if len(fields)>2 else ""})
    return rows

def canonical(row):
    email = str(row.get("email") or row.get("correo") or "").strip().lower()
    if not EMAIL.fullmatch(email):
        return None
    local, sep, domain = email.partition("@")
    if domain in ("gmail.com", "googlemail.com"):
        local = local.split("+", 1)[0].replace(".", "")
        return local + "@gmail.com"
    return email

def atomic_write(path, cfg):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".cuentas-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def main():
    p = argparse.ArgumentParser(description="Inventario y migracion local sin duplicados")
    p.add_argument("--source", required=True, help="Archivo TXT/CSV/JSON de cuentas propias")
    p.add_argument("--config", default=str(Path(__file__).resolve().parent / "config.json"))
    p.add_argument("--apply", action="store_true", help="Aplicar importacion; por defecto solo auditoria")
    p.add_argument("--verified-only", action="store_true", help="Importar solo filas con verified=true")
    args = p.parse_args()
    source, target = Path(args.source).resolve(), Path(args.config).resolve()
    if source == target:
        p.error("Origen y destino deben ser diferentes")
    incoming = read_accounts(source)
    cfg = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {"accounts": []}
    existing = cfg.get("accounts", [])
    if not isinstance(existing, list):
        raise ValueError("config.accounts no es una lista")
    known = {canonical(x) for x in existing if isinstance(x, dict)}
    additions, duplicates, invalid, unverified = [], 0, 0, 0
    for row in incoming:
        email = canonical(row)
        if not email:
            invalid += 1
            continue
        if args.verified_only and str(row.get("verified", "")).strip().lower() not in ("true", "1", "yes", "si", "sí"):
            unverified += 1
            continue
        if email in known:
            duplicates += 1
            continue
        known.add(email)
        # Conserva los campos admitidos por la configuracion original.
        entry = {k: v for k, v in row.items() if k in
                 ("id", "email", "password", "recovery_email", "totp_secret", "status", "notes")}
        entry["email"] = email
        entry["id"] = str(entry.get("id") or f"Account_{len(existing) + len(additions) + 1}")
        used_ids = {str(x.get("id")) for x in existing + additions}
        while entry["id"] in used_ids:
            entry["id"] = "Account_" + str(len(used_ids) + 1)
        entry.setdefault("recovery_email", "")
        entry.setdefault("totp_secret", "")
        entry.setdefault("proxy", "")
        entry.setdefault("ip_info", "")
        entry.setdefault("current_step", 0)
        entry.setdefault("step_message", "Cuenta importada; pendiente de revision")
        entry.setdefault("expiry_date", "-")
        entry.setdefault("last_screenshot", "")
        entry.setdefault("status", "pending")
        additions.append(entry)
    print(json.dumps({"origen": len(incoming), "existentes": len(existing),
                      "nuevas": len(additions), "duplicadas": duplicates,
                      "invalidas": invalid, "no_verificadas": unverified,
                      "modo": "APLICAR" if args.apply else "AUDITORIA"}, ensure_ascii=False))
    if not args.apply:
        return
    if target.exists():
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = target.with_name(target.name + ".bak-" + stamp)
        shutil.copy2(target, backup)
        os.chmod(backup, 0o600)
        print("Respaldo:", backup)
    cfg["accounts"] = existing + additions
    atomic_write(target, cfg)
    print("Importacion completada; no se imprimieron credenciales.")

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print("Error:", exc, file=sys.stderr)
        sys.exit(1)
