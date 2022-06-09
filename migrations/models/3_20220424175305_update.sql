-- upgrade --
ALTER TABLE "user_task" ALTER COLUMN "resolving_penalty" SET DEFAULT 0;
ALTER TABLE "user_task" ALTER COLUMN "resolving_penalty" SET NOT NULL;
-- downgrade --
ALTER TABLE "user_task" ALTER COLUMN "resolving_penalty" DROP NOT NULL;
ALTER TABLE "user_task" ALTER COLUMN "resolving_penalty" DROP DEFAULT;
