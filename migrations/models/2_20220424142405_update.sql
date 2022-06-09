-- upgrade --
ALTER TABLE "user_task" ADD "resolving_penalty" INT;
ALTER TABLE "user_task" ADD "resolving_dt" TIMESTAMPTZ;
-- downgrade --
ALTER TABLE "user_task" DROP COLUMN "resolving_penalty";
ALTER TABLE "user_task" DROP COLUMN "resolving_dt";
