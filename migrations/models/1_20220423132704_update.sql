-- upgrade --
ALTER TABLE "task" RENAME COLUMN "statement_text" TO "statement";
ALTER TABLE "task" ALTER COLUMN "hint_3" SET NOT NULL;
ALTER TABLE "task" ALTER COLUMN "hint_1" SET NOT NULL;
ALTER TABLE "task" ALTER COLUMN "hint_2" SET NOT NULL;
-- downgrade --
ALTER TABLE "task" RENAME COLUMN "statement" TO "statement_text";
ALTER TABLE "task" ALTER COLUMN "hint_3" DROP NOT NULL;
ALTER TABLE "task" ALTER COLUMN "hint_1" DROP NOT NULL;
ALTER TABLE "task" ALTER COLUMN "hint_2" DROP NOT NULL;
