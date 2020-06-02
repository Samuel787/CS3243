@echo off
echo Process Starting with test input 2
echo ----------------------

echo ~~~~~~~~~~~~~~~AC3~~~~~~~~~~~~~~~~~
echo AC3 with MCV without LCV
python .\CS3243_P2_Sudoku_[AC3-MCV-noLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt

echo AC3 without MCV with LCV
del .\output_test2.txt
python .\CS3243_P2_Sudoku_[AC3-noMCV-haveLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt
del .\output_test2.txt

echo AC3 without MCV without LCV
python .\CS3243_P2_Sudoku_[AC3-noMCV-noLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt
del .\output_test2.txt

echo ~~~~~~~~~~~~~~~~~~FWD CHECKING~~~~~~~~~~
echo Fwd Checking with MCV without LCV
python .\CS3243_P2_Sudoku_[Fwd-Checking-MCV-noLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt
del .\output_test2.txt

echo Fwd Checking without MCV with LCV
python .\CS3243_P2_Sudoku_[Fwd-Checking-noMCV-haveLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt
del .\output_test2.txt

echo Fwd Checking without MCV without LCV
python .\CS3243_P2_Sudoku_[Fwd-Checking-noMCV-noLCV].py ..\public_tests_p2_sudoku\input2.txt .\output_test2.txt
FC ..\public_tests_p2_sudoku\output2.txt .\output_test2.txt
del .\output_test2.txt
