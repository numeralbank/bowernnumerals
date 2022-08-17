import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar
from pylexibank import Language
from pylexibank import FormSpec


@attr.s
class CustomLanguage(Language):
    Sources = attr.ib(default=None)
    NameInSource = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Comment = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "bowernnumerals"
    language_class = CustomLanguage
    form_spec = FormSpec(
        separators=",;/", missing_data=["?", "!"], first_form_only=True,
    )

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        args.log.info("added sources")

        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"]+"_"+slug(concept["ENGLISH"])
            concepts[concept["ENGLISH"]] = idx
            args.writer.add_concept(
                ID=idx,
                Name=concept["ENGLISH"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
                )
        args.log.info("added concepts")

        languages = args.writer.add_languages(lookup_factory="NameInSource")
        args.log.info("added languages")

        data = self.raw_dir.read_csv(
            "data.tsv",
            delimiter="\t",
            dicts=True
        )
        for row in progressbar(data):
            language_id = languages[row["LANGUAGE"]]
            for concept, concept_id in concepts.items():
                entry = row[concept].strip()
                if entry:
                    args.writer.add_forms_from_value(
                        Language_ID=language_id,
                        Parameter_ID=concept_id,
                        Value=entry,
                        Source="Bowern2012",
                    )