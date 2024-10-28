from import_export.formats.base_formats import CSV

class TxtFormat(CSV):
    def get_title(self):
        return "txt"

    def get_extension(self):
        return "txt"

    def create_dataset(self, in_stream, **kwargs):
        """This method is responsible for adjusting the delimiter during import."""
        kwargs['delimiter'] = '|'
        return super().create_dataset(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        """This method adjusts the delimiter for export."""
        kwargs['delimiter'] = '|'
        return super().export_data(dataset, **kwargs)

    @classmethod
    def from_filename(cls, filename):
        """Ensures the system recognizes .txt files"""
        return filename.endswith('.txt')