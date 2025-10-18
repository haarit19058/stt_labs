
# semgrep 
need to login


# flawfinder
sudo pacman -S flawfinder
flawfinder --csv --columns --context ./OpenCC > flawfinder_OpenCC.csv 

# cpp check
sudo pacman -S cppcheck or use yay
cppcheck --enable=all --inconclusive --check-level=exhaustive --std=c++17 ./OpenCC --xml  2> cppcheck_OpenCC.xml


# code ql

First download tarball of codeql form this link https://github.com/github/codeql-action/releases

Then do whatever gpt says


step 01

#### create a DB named myproject-db, run the build command so CodeQL can extract info
codeql database create myproject-db --language=cpp 


Step 02
  ../codeql/codeql database analyze myproject-db ../codeql/qlpacks/codeql/cpp-queries/1.5.1/Security/CWE \
    --format=sarif-latest \
    --output=results.sarif


Step 03 
remove the conflicting ql files if any


Step 04 convert sarif to csv


rm -rf myproject-db/results     to remove cached data
