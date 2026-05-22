from pathlib import Path

migration_path = Path("/app/api/migrations/versions/2025_07_02_2332-1c9ba48be8e4_add_uuidv7_function_in_sql.py")
text = migration_path.read_text()

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

migration_path.write_text(text)

app_factory_path = Path("/app/api/app_factory.py")
app_factory_text = app_factory_path.read_text()
config_needle = """    dify_app.config.from_mapping(dify_config.model_dump())
    dify_app.config["RESTX_INCLUDE_ALL_MODELS"] = True
"""
config_replacement = """    dify_app.config.from_mapping(dify_config.model_dump())
    dify_app.config["RESTX_INCLUDE_ALL_MODELS"] = True
    dify_app.config["SESSION_COOKIE_SAMESITE"] = "None"
    dify_app.config["SESSION_COOKIE_SECURE"] = True
"""
if config_needle not in app_factory_text:
    raise SystemExit("app_factory cookie patch target not found")

app_factory_path.write_text(app_factory_text.replace(config_needle, config_replacement))
