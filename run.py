from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from main_window import Ui_Dialog


class RMCHInterface(Ui_Dialog, QDialog):

    def __init__(self):
        super(Ui_Dialog, self).__init__()
        self.setupUi(self)

        # Initialize interface variables
        self.inputFileLocation = str()
        self.outputFileLocation = str()

        # Declare string criteria for removal
        self.headers = ["<meta charset=\"UTF-8\">",
                        "<title>*|MC:SUBJECT|*</title>",
                        "<!--*|IF:MC_PREVIEW_TEXT|*-->",
                        "*|MC_PREVIEW_TEXT|*"]

        # Link objects to methods
        self.pushButton_browse.clicked.connect(self.select_file)
        self.pushButton_remove.clicked.connect(self.remove_headers)

    def select_input_file_location(self) -> None:
        """
        Prompt the user to select the input HTML file through
        a file dialog
        :return: None
        """
        self.inputFileLocation = QFileDialog.getOpenFileName(self, "Open HTML File", filter="*.html")[0]

    def select_output_file_location(self) -> None:
        """
        Prompt the user to save a new HTML file with the headers
        removed, using a file dialog
        :return: None
        """
        self.outputFileLocation = QFileDialog.getSaveFileName(self, "Save HTML File", filter="*.html")[0]

    def set_status(self, status: str) -> None:
        """
        Set the status of the software by changing the text
        of the status label within the UI
        :param status: The status as a string
        :return: None
        """
        self.label_status.setText(status)

    def select_file(self) -> None:
        """
        Prompt user to select file, update UI after file is
        selected
        :return:
        """
        self.select_input_file_location()
        if self.inputFileLocation != "":
            self.lineEdit_location.setText(str(self.inputFileLocation))
        self.set_status("Click remove headers to save the new file.")

    def remove_headers(self) -> None:
        """
        Given the file location from lineEdit_location, generate
        a new file that doesn't contain the MC headers and prompt
        the user to save that new file
        :return: None
        """
        self.inputFileLocation = self.lineEdit_location.text()

        # Verify that the location specified in lineEdit_location is
        # valid.
        if self.inputFileLocation == "":
            self.set_status("Input file must be specified")
            return
        else:
            try:
                if self.inputFileLocation[-5:] != ".html":
                    self.set_status("Input file must be HTML")
                    return
            except:
                self.set_status("Input file must be HTML")
                return

        # Begin I/O
        try:
            self.select_output_file_location()
            if self.outputFileLocation == "":
                return
            elif self.outputFileLocation == self.inputFileLocation:
                self.set_status("New file must have different name than first")
                return

            input_file = open(self.inputFileLocation, 'r')
            output_file = open(self.outputFileLocation, 'w')

            for line in input_file:
                contains = False
                for s in self.headers:
                    if s in line:
                        contains = True
                if not contains:
                    output_file.write(line)

            input_file.close()
            output_file.close()

            self.set_status("Headers successfully removed!")

        except Exception as e:
            self.set_status(f"Error: {e}")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("Remove MC Headers")
    user_interface = RMCHInterface()
    user_interface.show()
    sys.exit(app.exec_())
