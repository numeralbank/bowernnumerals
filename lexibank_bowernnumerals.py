import pathlib
from tkinter.tix import COLUMN
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language
from pylexibank import FormSpec
from csvw.dsv import UnicodeDictReader


@attr.s
class CustomLanguage(Language):
    Sources = attr.ib(default=None)
    NameInSource = attr.ib(default=None)
    Subgroup = attr.ib(default=None)
    #Comment = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "bowernnumerals"
    languageclass = CustomLanguage
    form_spec = FormSpec(
        separators="", missing_data=["?"], first_form_only=True,
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
        sources = {
            language["NameInSource"]: language["Sources"].strip().split(",")
            for language in self.languages}
        args.log.info("added languages")
        errors = set()
        


        data = self.raw_dir.read_csv(
            "data.tsv", delimiter="\t"
        )
        header = data[0]
        for i in range(len(data)):
            entries = dict(zip(header, data[i]))
            for language, lidx in languages.items():
                if lidx not in languages:
                    errors.add(("language", lidx))
                else:
                    args.writer.add_forms_from_value(
                        Language_ID = lidx, 
                        Parameter_ID = concepts[concept],
                        Value = entries,
                        )