from pathlib import Path

path = Path("/app/api/migrations/versions/2025_07_02_2332-1c9ba48be8e4_add_uuidv7_function_in_sql.py")
text = path.read_text()

needle = """    if _is_pg(conn):
        # PostgreSQL: Create uuidv7 functions
        op.execute(sa.text(r\"\"\"
"""
replacement = """    if _is_pg(conn):
        has_uuidv7 = conn.execute(sa.text(\"\"\"
            SELECT EXISTS (
                SELECT 1
                FROM pg_proc
                WHERE proname = 'uuidv7'
                  AND pronargs = 0
            )
        \"\"\")).scalar()

        # PostgreSQL: Create uuidv7 functions
        if not has_uuidv7:
            op.execute(sa.text(r\"\"\"
"""
if needle not in text:
    raise SystemExit("uuidv7 migration patch target not found")

text = text.replace(needle, replacement)
text = text.replace(
    '        op.execute(sa.text("DROP FUNCTION uuidv7"))',
    '        op.execute(sa.text("DROP FUNCTION IF EXISTS public.uuidv7()"))',
)
text = text.replace(
    '        op.execute(sa.text("DROP FUNCTION uuidv7_boundary"))',
    '        op.execute(sa.text("DROP FUNCTION IF EXISTS public.uuidv7_boundary(timestamptz)"))',
)

path.write_text(text)
