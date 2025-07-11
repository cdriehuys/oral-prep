import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from quiz import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("questions_file", type=Path)

    def handle(self, *args, **options):
        questions_file: Path = options["questions_file"]
        with questions_file.open() as f:
            data = json.load(f)

        question_count = len(data)
        imported_count = 0

        for question in data:
            model = models.Question(
                certificate_type=question["certificate"],
                plane_type=question["type"],
                question=question["question"],
                answer=question["answer"],
                import_id=question["questionId"],
            )

            if question["imageFile"] is None:
                if self._save_question(model):
                    imported_count += 1

                continue

            image_path = questions_file.parent / "images" / question["imageFile"]
            with image_path.open("rb") as f:
                model.image = File(f, name=image_path.name)
                if self._save_question(model):
                    imported_count += 1

        self.stdout.write(
            f"Finished import ({imported_count}/{question_count} new questions)"
        )

    def _save_question(self, question: models.Question) -> bool:
        try:
            question.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported question with import ID {question.import_id}"
                )
            )
            return True
        except IntegrityError as e:
            try:
                conflict = models.Question.objects.filter(
                    import_id=question.import_id
                ).get()
            except models.Question.DoesNotExist:
                raise CommandError(
                    "There was a conflict inserting the question that wasn't caused by the import ID."
                ) from e

            has_content_differences = any(
                (
                    question.certificate_type != conflict.certificate_type,
                    question.plane_type != conflict.plane_type,
                    question.question != conflict.question,
                    question.answer != conflict.answer,
                )
            )

            if has_content_differences:
                self.stdout.write(
                    self.style.WARNING(
                        f"Importing question {question.import_id} would overwrite existing changes to the question."
                    )
                )

        return False
