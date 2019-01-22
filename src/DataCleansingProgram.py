import sys
import binascii
import collections
import datetime
from PyQt4 import QtGui, uic

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor


qtCreatorFile = r"C:\Python27\Lib\site-packages\Programs\DataReformer\v1.7\DataCleanser.ui" # Enter file here.
filename1 = ""
delimiter = ""

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pbtnBrowseFile.clicked.connect(self.getfile)
        self.pbtnGenPreview.clicked.connect(self.prevFile)
        self.pbtnClearPreview.clicked.connect(self.clearPreviewFile)
        self.pbtnProfile.clicked.connect(lambda: self.ProfileFile(filename1))
        self.pbtnClear.clicked.connect(self.clearProfileHistory)
        self.pbtnFixFile.clicked.connect(lambda: self.fixfile(filename1))
        self.pbtnExtractIssLines.clicked.connect(lambda: self.extractlines(filename1))
        self.pbtnExtractNonIssLines.clicked.connect(lambda: self.extractnonissuelines(filename1))
        self.lnedEnterDel.returnPressed.connect(self.pbtnProfile.setFocus)
        self.lnedEnterDelCount.returnPressed.connect(self.pbtnFixFile.setFocus)
        self.lnedEnterDel.setToolTip("Enter 'T' for tab delimited, 'S' for space delimited")
        self.lnedRowsOffset.setToolTip("Enter the line number data begins on")
        self.tbFileSelected.setText("<i>File Selected:</i>")
        self.tbInputFilePath.setText("<i>Input File:</i>")
        self.tbExtractPath.setText("<i>Extract File:</i>")
        self.tbExtractNoIssuePath.setText("<i>Extract No Issue Lines File:</i>")
        self.tbOutPutPath.setText("<i>Output File:</i>")
        self.tbLogPath.setText("<i>Log File:</i>")
        self.chkbHeaderOffset.stateChanged.connect(lambda: self.checkedSlot(self.chkbHeaderOffset.checkState()))



    def getfile(self):
        w = QtGui.QWidget()
        filename = QtGui.QFileDialog.getOpenFileName(w,'Open file','C:/')
        # Call the method to clear all information for previous files
        self.clearPreviousFileInfo()
        self.tbInputFilePath.setOpenExternalLinks(True)
        self.tbInputFilePath.setText(" <b>Input File: </b> <a href='"+ filename+"'>Open file</a> " + filename)
        self.tbFileSelected.setText("<b>File Selected: </b>"+ filename+"")

        global filename1
        filename1 = filename



    def prevFile(self):
        self.filepreview(filename1)



    def clearPreviewFile(self):
        self.ptxeFilePreview.clear()



    def filepreview(self,x):
        self.ptxeFilePreview.clear()
        try:
            file1 = open(x, 'r')
        except:
            QtGui.QMessageBox.information(self, 'No File Found', "Please select a file to preview from STEP 1", QtGui.QMessageBox.Ok)
            return
        for k in range(1,100):
            #self.ptxeFilePreview(file1.readline())
            self.ptxeFilePreview.insertPlainText(file1.readline())



    def checkedSlot(self, state):
        if state == 2:
            self.lnedRowsOffset.setEnabled(1)
        else:
            self.lnedRowsOffset.setDisabled(1)
            self.lnedRowsOffset.clear()



    def ProfileFile(self,infile):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #-----------------------------------------------------------------------------------------------------
        # This method profiles the full file and gives the statistics of delimiter counts in the file.
        # A file selection and delimiter are mandatory for this function. A recommendation is made to the user as to which is the
        # most probable true delimiter count, based on the fact that a delimiter is most commonly occurring.
        #-----------------------------------------------------------------------------------------------------
        #Exception check routine to ensure variable are defined properly
        chkcode = self.checkDelParameters()
        if chkcode==20:
            chkcode=10
        a= [0,11]
        if chkcode not in a:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(self, 'Invalid Data', self.checkDelErrorsMsgs(chkcode),QtGui.QMessageBox.Ok)
            return

        global delimiter
        delimiter = str(self.lnedEnterDel.text())
        delimiter = delimiter.strip()
        self.lblProfStatus.setText("")

        #Perform and transformation on delimiter
        delimiter = self.transformdelimiter(delimiter)

        h=0
        c= collections.Counter()
        f1=open(infile,'r')
        #self.lblProfStatus.setText("Profiling file in progress...")
        for line in f1:
            c[str(line.count(delimiter))] += 1
            h=h+1

        self.ptxeFileAnalysis.appendHtml("<b>Delimiter count profile :<br/>File: </b>"+ infile + "<br/><b>Date & Time: </b>"+str(datetime.datetime.now())+"<br/>")
        #self.ui.plainTextEdit_2.appendPlainText("Delimiter count profile \nFile: "+ infile + "\nDate & Time: "+str(datetime.datetime.now()))
        for key, value in c.items():
            self.ptxeFileAnalysis.appendPlainText("\t"+ key + " times in " + str(value) +" line(s)")
        # Print the most common delimiter count
        for  key1, val1 in c.most_common(1):
            if key1=="0" :
                self.ptxeFileAnalysis.appendPlainText("The selected delimiter does not exist in most of the lines.\n\nConsider a different delimiter.\n")
                #correct_del ='N'
            else:
                self.ptxeFileAnalysis.appendPlainText("\nThe most common delimiter count is " + key1 + ". In " + str(val1) + " line(s) of the total " +str(h) +" lines there occurred "  + key1 + " delimiters.\n\nThis indicates no LF/CR issues when the delimiter count is "+ key1 +".\n")

        #self.lblProfStatus.setText("Profiling complete")

        QApplication.restoreOverrideCursor()



    def clearProfileHistory(self) :
        self.ptxeFileAnalysis.clear()



    def clearPreviousFileInfo(self):
        self.tbInputFilePath.clear()
        self.tbExtractPath.clear()
        self.tbExtractNoIssuePath.clear()
        self.tbOutPutPath.clear()
        self.tbLogPath.clear()
        self.ptxeFileAnalysis.clear()
        self.ptxeFilePreview.clear()
        #self.lnedEnterDel.clear()
        #self.lnedEnterDelCount.clear()



    def replace_last(self, source_string, replace_what, replace_with):
        head, sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail



    def replace_last_all(self, source_string, replace_what, replace_with):
        head, sep, tail = source_string.rpartition(replace_what)
        return head + replace_with



    def extractlines(self,infile):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #-----------------------------------------------------------------------------------------------------
        # This method extract all lines from the selected file that does not have a delimiter count given by the user.
        # A file selection, delimiter and delimiter count are mandatory to this method.
        #-----------------------------------------------------------------------------------------------------

        #Exception check routine to ensure variable are defined properly
        chkcode = self.checkDelParameters()
        if chkcode != 0:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(self, 'Invalid Data', self.checkDelErrorsMsgs(chkcode),QtGui.QMessageBox.Ok)
            return

        #Assign variables
        global delimiter
        delimiter = str(self.lnedEnterDel.text())
        delimiter = delimiter.strip()
        true_del_count_in = self.lnedEnterDelCount.text()
        true_del_count = int(true_del_count_in)

        #Perform any transformation on delimiter
        delimiter = self.transformdelimiter(delimiter)

        #Add comment
        i_file_name= self.replace_last(str(infile).strip(), '.', "_ISSUE_LINES.")
        i_file = open(i_file_name, mode="w")
        f = open(infile,'r')

        #write the header to the file
        try:
            offset = int(self.lnedRowsOffset.text())-1 #User will enter the line the DATA starts on not when the header ends
        except:
            offset = 1 #Defaults to first line

        j=0
        #Add comments
        for line in f:
            # Grab the header rows from 1 to the offset number
            if j in range(0, offset):
                i_file.write(line)
            elif line.count(delimiter) != true_del_count :
                i_file.write(line)
            j=j+1

        self.tbExtractPath.setOpenExternalLinks(True)
        self.tbExtractPath.setText("<b>Extract File: </b> <a href='"+ i_file_name+"'>Open file</a> "+ i_file_name)
        QApplication.restoreOverrideCursor()

    def extractnonissuelines(self,infile):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #-----------------------------------------------------------------------------------------------------
        # This method extract all lines from the selected file that have a delimiter count given by the user.
        # A file selection, delimiter and delimiter count are mandatory to this method.
        #-----------------------------------------------------------------------------------------------------

        #Exception check routine to ensure variable are defined properly
        chkcode = self.checkDelParameters()
        if chkcode != 0:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(self, 'Invalid Data', self.checkDelErrorsMsgs(chkcode),QtGui.QMessageBox.Ok)
            return

        #Assign variables
        global delimiter
        delimiter = str(self.lnedEnterDel.text())
        delimiter = delimiter.strip()
        true_del_count_in = self.lnedEnterDelCount.text()
        true_del_count = int(true_del_count_in)

        #Perform any transformation on delimiter
        delimiter = self.transformdelimiter(delimiter)

        #Add comment
        i_file_name= self.replace_last(str(infile).strip(), '.', "_NONISSUE_LINES.")
        i_file = open(i_file_name, mode="w")
        f = open(infile,'r')

        #write the header to the file
        try:
            offset = int(self.lnedRowsOffset.text())-1 #User will enter the line the DATA starts on not when the header ends
        except:
            offset = 1 #Defaults to first line

        j=0
        #Add comments
        for line in f:
            # Grab the header rows from 1 to the offset number
            if j in range(0, offset):
                i_file.write(line)
            elif line.count(delimiter) == true_del_count :
                i_file.write(line)
            j=j+1

        self.tbExtractNoIssuePath.setOpenExternalLinks(True)
        self.tbExtractNoIssuePath.setText("<b>Extract No Issues File: </b> <a href='"+ i_file_name+"'>Open file</a> "+ i_file_name)
        QApplication.restoreOverrideCursor()

    def fixfile(self,infile):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #-----------------------------------------------------------------------------------------------------
        # The selected file is fixed based on the two inputs from user : Delimiter and Correct delimiter count.
        # The code loops through each line in the file, counts the number of delimiters, and compares it to the true delimiter count.
        # LF/CR characters are removed from the lines till the sum of the consecutive lines add up to the true delimiter count.
        # The out put  is written to a file with a filename as source filename + "_FIXED"
        #-----------------------------------------------------------------------------------------------------
        #Exception check routine to ensure variable are defined properly
        chkcode = self.checkDelParameters()
        if chkcode != 0:
            QApplication.restoreOverrideCursor()
            QtGui.QMessageBox.information(self, 'Invalid Data', self.checkDelErrorsMsgs(chkcode),QtGui.QMessageBox.Ok)
            return

        #Assign variables
        global delimiter
        delimiter = str(self.lnedEnterDel.text())
        delimiter = delimiter.strip()
        true_del_count_in = self.lnedEnterDelCount.text()
        true_del_count = int(true_del_count_in)
        logfilename = self.replace_last_all(str(infile).strip(), '.', "_LOG.txt")
        outfile = self.replace_last(str(infile).strip(), '.', "_FIXED.")

        #Assign variables for fix file sub routines actually fixing the files
        hex_enter = "0a"
        hex_cr = "0d"
        i = 0
        j = 0
        k = 0
        l_file = open(logfilename, mode="w")
        opfile = open(outfile, mode="w")
        f = open(infile,'r')
        true_count_check = 0

        l_file.write("Log for fixing the source file: "+ infile + " with delimiter '"+ delimiter +"' and delimiter count " +true_del_count_in+ ".\nDate & Time: "+str(datetime.datetime.now())+"\n")

        #Perform any transformation on delimiter
        delimiter = self.transformdelimiter(delimiter)

        #Convert delimiter ASCII characters to HEX
        hex_delimiter = binascii.hexlify(delimiter)

        #write the header to the file
        try:
            offset = int(self.lnedRowsOffset.text())-1 #User will enter the line the DATA starts on not when the header ends
        except:
            offset = 1 #Defaults to first line

        #Loop through the file line by line to find incorrect lines
        for line in f:
            #write the header lines first
            if k in range(0, offset):
                opfile.write(line)
                l_file.write("\nHeader row " + str(k+1) + " written to output file")
            else:
                hexline = binascii.hexlify(line)
                i=i+1
                if line.count(delimiter) != true_del_count:
                    if true_count_check==0:
                        first_line = True
                    else:
                        first_line =False

                    true_count_check=true_count_check + line.count(delimiter)
                    if true_count_check < true_del_count:
                        if first_line :
                            l_file.write("\nA fix is made starting in line " + str(i))
                        hexline = hexline.replace(hex_enter, "")
                        hexline = hexline.replace(hex_cr, "")
                    elif true_count_check > true_del_count:
                        true_count_check=0
                        l_file.write( "Line " + str(i) + " has extra delimiters. No fix has been made.")
                    else:
                        true_count_check=0
                        l_file.write(" and lines through " + str(i) + " were appended to it.")

                    j=j+1
                    #print binascii.unhexlify(hexline)

                else:
                    true_count_check=0

                opfile.write(binascii.unhexlify(hexline))
            k=k+1

        self.tbOutPutPath.setOpenExternalLinks(True)
        self.tbLogPath.setOpenExternalLinks(True)
        self.tbOutPutPath.setText("<b>Output File: </b> <a href='"+ outfile+"'>Open file</a> " + outfile)
        self.tbLogPath.setText("<b>Log File: </b> <a href='"+ logfilename+"'>Open file</a> "+ logfilename)

        print str(j) + " lines had LF/CR issue(s). The fixed file contents will be written to " + outfile +"\n"

        QApplication.restoreOverrideCursor()



    def checkDelParameters(self):
        #-----------------------------------------------------------------------------------------------------
        #Error handling to ensure proper delimiters and delimiter counts are added:
        #   Error Codes:
        #       0 = no issues with either the delimiter character field or delimiter count field
        #      11 = no issue with the delimiter character field, but delimiter count field is not an integer
        #      10 = delimiter character field is blank, but the delimiter count field is an integer
        #      20 = delimiter character field is blank, AND the delimiter count field is not an integer
        #      99 = an unknown issue
        #-----------------------------------------------------------------------------------------------------
        delstr = str(self.lnedEnterDel.text())
        try:
            delcnt = int(self.lnedEnterDelCount.text())
        except:
            delcnt = 9999

        #Exception for both delimiter value and counts being blank
        if delstr and delcnt != 9999:
            checkdel = 0
        elif delstr and delcnt == 9999:
            checkdel = 11
        elif not delstr and delcnt != 9999:
            checkdel = 10
        elif not delstr and delcnt == 9999:
            checkdel = 20
        else:
            checkdel = 99

        return checkdel



    def checkDelErrorsMsgs(self,chkcode):
        #-----------------------------------------------------------------------------------------------------
        #Error messages for the corresponding error codes
        #  Implicit is that code 0 will not call this function, as this function called only using
        #  the Try/Except catch
        #-----------------------------------------------------------------------------------------------------
        if chkcode == 10:
            errmsg = "Please type a delimiter within STEP 2."
        elif chkcode == 11:
            errmsg = "Please type a numerical value within STEP 3."
        elif chkcode == 20:
            errmsg = "Please type a delimiter within STEP 2 and numerical value within STEP 3."
        elif chkcode == 99:
            errmsg = "Unknown error 99 occurred. Process cancelled."
        else:
            errmsg = "Unknown error occurred. Process cancelled."

        return errmsg



    def transformdelimiter(self,delchar):
        #-----------------------------------------------------------------------------------------------------
        #Error messages for to transform delimiter to appropriate values so program can handle them
        #  currently only supporting Tab and Space.
        #
        #-----------------------------------------------------------------------------------------------------
        # #Transform characters T and S to values for tab and space bar
        if delchar.upper() == "T":
            delcharreturn = "\t"
        elif delchar.upper() == "S":
            delcharreturn = " "
        else:
            delcharreturn = delchar
        return delcharreturn



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
