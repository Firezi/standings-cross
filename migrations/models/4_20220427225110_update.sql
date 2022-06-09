-- upgrade --
ALTER TABLE "user_task" ADD "last_wrong_answer" VARCHAR(64);
-- downgrade --
ALTER TABLE "user_task" DROP COLUMN "last_wrong_answer";
