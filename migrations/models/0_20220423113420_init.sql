-- upgrade --
CREATE TABLE IF NOT EXISTS "game_info" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_dt" TIMESTAMPTZ NOT NULL,
    "end_dt" TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "coords" VARCHAR(64) NOT NULL,
    "statement_text" VARCHAR(300) NOT NULL,
    "right_answer" VARCHAR(64) NOT NULL,
    "hint_1" VARCHAR(300),
    "hint_2" VARCHAR(300),
    "hint_3" VARCHAR(300)
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(64) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_resolved" BOOL NOT NULL  DEFAULT False,
    "wrong_attempts_count" INT NOT NULL  DEFAULT 0,
    "hint_1_used" BOOL NOT NULL  DEFAULT False,
    "hint_2_used" BOOL NOT NULL  DEFAULT False,
    "hint_3_used" BOOL NOT NULL  DEFAULT False,
    "task_id" INT NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_user_task_user_id_dd81f4" UNIQUE ("user_id", "task_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
