import itertools
from pathlib import Path

from PyPDF2 import PdfWriter, PdfReader, PageObject

from idiotDiary.core.utils.dates import get_now
from idiotDiary.mq.broker import broker


@broker.task
async def pack_pdf_file(file_paths: list[Path]) -> Path:
    page_lists: list[list[PageObject]] = []
    for file_path in file_paths:
        page_lists.append(PdfReader(file_path).pages)

    max_pages: int = len(max(page_lists, key=lambda x: len(x)))
    page_cycles: list[itertools.islice[PageObject]] = [
        itertools.islice(itertools.cycle(iterable), max_pages)
        for iterable in page_lists
    ]
    writer = PdfWriter()
    page_groups = zip(*page_cycles)
    for page_group in page_groups:
        for page in page_group:
            writer.add_page(page)

    folder = file_paths[0].parent
    pdf_file_path = folder / f"output-{get_now().isoformat()}.pdf"
    with pdf_file_path.open(mode="wb") as pdf_file:
        writer.write(pdf_file)

    return pdf_file_path
