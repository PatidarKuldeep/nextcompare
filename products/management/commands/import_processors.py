import csv
from django.core.management.base import BaseCommand
from products.models import Processor


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):

        file_path = options["csv_file"]

        with open(file_path, newline='', encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                Processor.objects.update_or_create(
                    name=row["name"].strip(),
                    defaults={
                        "brand": row["brand"],
                        "antutu_score": int(row["antutu_score"]),
                        "geekbench_single": int(row["geekbench_single"]),
                        "geekbench_multi": int(row["geekbench_multi"]),
                        "benchmark_score": int(float(row["benchmark_score"])),
                    }
                )

        self.stdout.write(self.style.SUCCESS("Processors imported successfully"))